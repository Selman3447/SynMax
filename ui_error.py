import os
import random
import shutil

import sys
import urllib.request
from tkinter import *
from tkinter import filedialog

import PySide2
import pyautogui

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor, QFont, QMovie
from PyQt5.QtWidgets import *
from PySide2.QtCore import Qt
from pytube import YouTube
from caynakerror import *

class MainError(QMainWindow):
    def __init__(self):

        super (MainError, self).__init__ ( )
        self.ui = Ui_Dialog()
        self.ui.setupUi (self)
        rlf = open("error.txt", "r")
        rl = rlf.readline()
        name, fsize = rl.split ("|")
        self.ui.error.setText(name)
        self.ui.error.setFont(QFont("MS Shell Dlg 2", int(fsize)))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ui.close.clicked.connect(lambda: self.close())
        self.ui.Ok.clicked.connect(lambda: self.close())
        self.ui.icona.clicked.connect(lambda: self.showMinimized())

        self.dragPos = self.pos()

        def mouseMoveEvent(event):
            delta = QPoint (self.pos ( ) + event.globalPos ( ) - self.dragPos)
            #print (self.pos ( ) + event.globalPos ( ) - self.dragPos)
            self.move (self.pos ( ) + event.globalPos ( ) - self.dragPos)
            self.dragPos = event.globalPos ( )
            event.accept ( )

        # WIDGET HAREKETİ
        self.ui.titlebar.mouseMoveEvent = mouseMoveEvent
        ################

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()







if __name__=='__main__':
        app=QApplication(sys.argv)
        ex=MainError()

        ex.show()
        sys.exit(app.exec_())