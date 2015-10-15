'''
Created on Jul 18, 2013

@author: qurban.ali
'''
from PyQt4.QtGui import QApplication, QStyleFactory
import src.mainWindow as mW
import sys

if __name__ == '__main__':
    app = QApplication([sys.argv[0]])
    win = mw.Window()
    win.setStyleSheet('Background-color: #4D4D4D; color: #D6D6D6; border-color: gray;')
    sys.exit(app.exec_())