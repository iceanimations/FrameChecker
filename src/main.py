'''
Created on Jul 18, 2013

@author: qurban.ali
'''
import site
site.addsitedir(r'R:\Python_Scripts')
import interface.mainWindow as mWindow
from PyQt4.QtGui import QApplication, QStyleFactory
import sys

if __name__ == '__main__':
    filePath = None
    if len(sys.argv) > 1:
        filePath = sys.argv[1]
    app = QApplication([sys.argv[0]])
    win = mWindow.Window(filePath)
    sys.exit(app.exec_())