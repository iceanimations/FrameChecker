'''
Created on Jul 18, 2013

@author: qurban.ali
'''
from PyQt4 import uic
from PyQt4.QtGui import *
import utilities as util
import subprocess
import cui

rootPath = util.dirname(util.dirname(__file__))
uiPath = util.join(rootPath, 'ui')
iconPath = util.join(rootPath, 'icons')

form, base = uic.loadUiType(util.join(uiPath, 'mainWindow.ui'))
class Window(form, base):
    def __init__(self):
        '''
        Constructor
        '''
        super(Window, self).__init__()
        self.setupUi(self)
        self.show()
        icon = QIcon(util.join(iconPath, 'mainIcon64x64.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('frameChecker')
        # connections and mappings
        self.setConnections()
        self.initUI()
        #self.setSourcePathCaller(filePath)
        
    def initUI(self):
        '''
        Initializes the variables
        '''
        self.sourcePath = ''
        self.lowerBound = 0
        self.files = []
        
    def setConnections(self):
        '''
        sets the connections for the ui elements/widgets
        '''
        self.browseButton.clicked.connect(self.showFileDialog)
        self.filePathBox.returnPressed.connect(self.setSourcePath)
        self.badFramesLabel.linkActivated.connect(self.openBadFile)
        
    def setSourcePathCaller(self, path):
        if path:
            self.filePathBox.setText(path)
            self.setSourcePath()
    
    def showMessage(self, **kwargs):
        return cui.showMessage(self, title='Frame Checker', **kwargs)
        
    def setSourcePath(self):
        path = str(self.filePathBox.text())
        if not util.pathExists(path):
            self.showMessage(msg = 'The system can not find the path specified',
                       icon = QMessageBox.Warning)
            return
        if util.isfile(path):
            path = util.dirname(path)
        if self.sourcePath != path:
            self.clearWindow()
            self.sourcePath = path
            self.collectData()
                
    def collectData(self):
        '''
        collects the data to list the files
        '''
        self.files[:] = util.files(self.sourcePath)
        if not self.files:
            self.showMessage(msg = 'No file found in the specified path',
                       icon = QMessageBox.Warning)
            return
        sizes = [util.size(util.join(self.sourcePath,
                                     fileName)) for fileName in self.files]
        self.lowerBound = util.standardDeviation(sizes, lower = True)
        self.listFiles()
        self.listMissingFiles()

    def clearWindow(self):
        '''
        clears the window
        '''
        self.files[:] = []
        self.lowerBound = 0
        self.allFramesBox.clear()
        self.missingFramesBox.clear()
        
    def listFiles(self):
        '''
        lists all the files
        '''
        badFiles = []
        badLabelText = ''
        # add the files to the allFramesBox
        for fil in self.files:
            path = util.join(self.sourcePath, fil)
            size = util.size(path)
            path = path.replace('\\', '/')
            if size < self.lowerBound:
                badFiles.append(fil)
                badLabelText += "<a href ='"+path+"' style='color: lightGreen'>"+ fil +"</a><br>"
            self.allFramesBox.appendPlainText(fil)
        self.badFramesLabel.setText(badLabelText)
        self.allLabel.setText('Total: '+ str(len(self.files)))
        firstFrame = util.frameNumber(self.files[0])
        lastFrame = util.frameNumber(self.files[-1])
        if not firstFrame or not lastFrame:
            self.showMessage(msg='Frame numbers do not exist in all the files',
                       icon = QMessageBox.Warning)
            return
        self.allBox.setText( firstFrame+' - '+ lastFrame)
        if badFiles:
            self.badLabel.setText('Total: '+ str(len(badFiles)))
            badFiles = sorted(badFiles)
            bfiles = ''
            for f in badFiles:
                fn = util.frameNumber(f)
                bfiles += fn + ', '
            bfiles = util.chopStr(bfiles, 2)
            self.badBox.setText(bfiles)
        
    def listMissingFiles(self):
        '''
        lists the missing frames
        '''
        first = util.frameNumber(self.files[0])
        last = util.frameNumber(self.files[-1])
        if not first or not last:
            return
        fileName = self.files[0]
        frames = set([util.frameNumber(fName) for fName in self.files])
        frameNoLen = len(list(frames)[0])
        newFrames = set([str(x).zfill(frameNoLen) for x in range(int(first),
                                                                 int(last)+1)])
        diff = list(newFrames.difference(frames))
        if diff:
            for line in sorted(util.frameNumToName(diff, fileName)):
                self.missingFramesBox.appendPlainText(line)
            self.missingLabel.setText('Total: '+ str(len(diff)))
            mfiles = ''
            for f in diff:
                mfiles += f +', '
            mfiles = util.chopStr(mfiles, 2)
            self.missingBox.setText(mfiles)
        
    def openBadFile(self, path):
        subprocess.call(path, shell=True)
        
    def showFileDialog(self):
        '''
        Shows the file dialog to the user to select a file
        '''
        fileName = QFileDialog.getOpenFileName(self, 'Select File', '', '', None, QFileDialog.DontUseNativeDialog)
        if fileName:
            self.filePathBox.setText(fileName)
            self.setSourcePath()
        
    def closeEvent(self, event):
        self.deleteLater()