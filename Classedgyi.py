import os
import random
import shutil
import subprocess

import sys
import time
import urllib.request
from tkinter import *
from tkinter import filedialog

import PySide2
import pyautogui

from PyQt5.QtCore import QPoint, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QMovie
from PyQt5.QtWidgets import *
from PySide2.QtCore import Qt
from pytube import YouTube

from threading import Thread

from caynak import *
from caynakerror import *

print ("Program loading...")

print ("Developer Mode On")

TIME_LIMIT = 100
class MainWindow (QMainWindow):
    def __init__(self):
        super (MainWindow, self).__init__ ( )
        self.ui = Ui_SplashScreen ( )
        self.ui.setupUi (self)

        fihrist = open (os.getcwd ( ) + r"\titleset.txt", "r")
        rl = fihrist.readline ( )

        _translate = QtCore.QCoreApplication.translate
        name, version = rl.split ("|")
        self.setWindowTitle (_translate ("SplashScreen", f"{name} {version}"))
        self.ui.label_2.setText (self.windowTitle ( ))

        self.ui.searchbar.setText ("https://www.youtube.com/watch?v=MhNzdYeBIVs")

        self.ui.stackedWidget.setCurrentIndex (0)



        movie = QMovie ("loading.gif")
        self.ui.loading.setMovie (movie)
        movie.start ( )
        self.ui.loading.hide()
        movie = QMovie ("loading.gif")
        self.ui.loading_2.setMovie (movie)
        movie.start ( )
        self.ui.loading_2.hide()



        self.setWindowFlags (QtCore.Qt.FramelessWindowHint)
        self.setAttribute (QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect (self)
        self.shadow.setBlurRadius (20)
        self.shadow.setXOffset (0)
        self.shadow.setYOffset (0)
        self.shadow.setColor (QColor (0, 0, 0, 60))
        self.ui.frame.setGraphicsEffect (self.shadow)

        self.ui.close.clicked.connect (lambda: self.close ( ))
        self.ui.icona.clicked.connect (lambda: self.showMinimized ( ))

        self.dragPos = self.pos ( )

        def mouseMoveEvent(event):
            delta = QPoint (self.pos ( ) + event.globalPos ( ) - self.dragPos)
            # print (self.pos ( ) + event.globalPos ( ) - self.dragPos)
            self.move (self.pos ( ) + event.globalPos ( ) - self.dragPos)
            self.dragPos = event.globalPos ( )
            event.accept ( )

        self.ui.titlebar.mouseMoveEvent = mouseMoveEvent
        self.ui.navibar.mouseMoveEvent = mouseMoveEvent

        self.timer = QtCore.QTimer (self)
        self.timer.timeout.connect (self.showTime)
        self.timer.start (1000)

        #########
        ##########ALL DEF##########
        #########
        # PAGE1
        def YtFinder():
            # ----> MAIN FINDER
            global yt
            link = self.ui.searchbar.text ( )
            yt = YouTube (link, on_progress_callback=progress)
            fillse = yt.streams.get_highest_resolution ( )
            try:

                global highsize
                global lowsize
                global highres
                global lowres
                highsize = yt.streams.get_highest_resolution ( ).filesize
                lowsize = yt.streams.get_lowest_resolution ( ).filesize
                highres = yt.streams.get_highest_resolution ( ).resolution
                lowres = yt.streams.get_lowest_resolution ( ).resolution

                print (r"\\\\\____Video algılandı____/////")
                global findstatus
                findstatus = "Yes"
                print ("")
                print (r"\\\\____Başlık____////")
                print (yt.title)
                print (r"\\\____Kanal____///")
                print (yt.author)
                print (r"\\____Süre____//")
                print (round (yt.length / 60), ":", yt.length % 60)  # Video Süresi Süre/60(Dakika) : Süre%60 (Saniye)
                print (r"\____Kapak Fotoğrafı____/")
                print (yt.thumbnail_url)  # Kapak Fotoğrafının Verisini Çekip Site Aracılığına dönüştürüyor.
                url = yt.thumbnail_url  # Site URL
                urllib.request.urlretrieve (url,
                                            os.getcwd ( ) + r'\thunbail.jpg')  # Kapak Fotoğrafını Belirtilen Yola kaydediyor. ( os.getcwd() projenin konumunu buluyor)
                print (os.getcwd ( ) + r'\thunbail.jpg', 'konumuna', 'thubail.jpg olarak kaydedildi.')

                self.ui.thumbnail.setPixmap (QtGui.QPixmap ("thunbail.jpg"))
                d = yt.length / 60
                s = yt.length % 60
                self.ui.ytime.setText (str (round (d)) + " : " + str (round (s)))
                self.ui.ytitle.setText (yt.title)
                # self.ui.ytitle.setText("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                self.ui.ytauthor.setText (yt.author)
                self.ui.finder.setText ("Find")

                self.ui.stackedWidget.setCurrentWidget (self.ui.page_2)

            except:
                print ("Geçersiz Link")
                pyautogui.alert ('Error 404', "SynMax")
                self.ui.finder.setText ("Find")



        def FIND():
            # ----> FINDER

            print ("Clicked: Find Button")

            self.ui.finder.setEnabled (False)
            self.ui.searchbar.setEnabled (False)

            self.ui.finder.setText ("...")

            self.ui.loading.show()
            self.ui.loading.setGeometry(100, 110, 411, 261)

            Thread (target=YtFinder, daemon=True).start ( )



            # YtFinder()



        def CLEAR():
            # ----> CLEAR FIND

            print ("Clicked: Clear Button")

            self.ui.thumbnail.hide ( )
            self.ui.ytime.hide ( )
            self.ui.ytime.setText ("<Time>")
            self.ui.ytitle.hide ( )
            self.ui.ytitle.setText ("<Title>")
            self.ui.ytauthor.hide ( )
            self.ui.ytauthor.setText ("<Author>")
            self.ui.clear.hide ( )
            self.ui.cnti.hide ( )
            self.ui.label_3.hide ( )

            self.ui.searchbar.setText ("")

        def CONITE():

            print ("Clicked: Continue Button(1)")
            self.ui.stackedWidget.setCurrentWidget (self.ui.page_3)
            self.ui.vidname_2.setText (self.ui.ytitle.text ( ))

            if self.ui.ytitle.text ( ) > r'64':
                self.ui.vidname_2.setFont (QFont ('MS UI Gothic', 13))


            self.ui.thumbnai2.setPixmap (QtGui.QPixmap ('thunbail.jpg'))




        # PAGE3(2)
        def PAGE3():
            highsize = yt.streams.get_highest_resolution().filesize
            lowsize = yt.streams.get_lowest_resolution().filesize
            self.ui.thumbnail_4.setPixmap (QtGui.QPixmap ("thunbail.jpg"))
            self.ui.vidname_3.setText (yt.title)
            self.ui.High.setText (yt.streams.get_highest_resolution ( ).resolution)
            self.ui.Low.setText (yt.streams.get_lowest_resolution ( ).resolution)

            self.ui.stackedWidget.setCurrentWidget (self.ui.page_4)


        def RANDOMS():
            # ----> RANDOM FILE NAME GENERATOR
            print ("Clicked: Random Button")
            sayi1 = random.randint (1000000000, 9999999999)
            sayi2 = random.randint (1000000000, 9999999999)
            self.ui.Filebar.setText (str (sayi1) + "_" + str (sayi2))

        def DEFLT():
            # ----> Default File Name Setter
            print ("Clicked: Defeult Name Button")
            self.ui.Filebar.setText (self.ui.ytitle.text ( ))

        def openFile():
            # ----> Folder dialog
            print ("Clicked: Folder Button")
            root = Tk ( )
            root.withdraw ( )
            filepath = filedialog.askdirectory ( )
            print (filepath)
            root.destroy ( )
            self.ui.FileLocName.setText (filepath)

        def DEFAULT():
            # ----> Default Folder Path
            print ("Clicked: Default Path Button")
            from pathlib import Path
            home = str (Path.home ( ))
            self.ui.FileLocName.setText (home + "\Downloads")

        def check():
            # ----> Format Checker

            print ("Clicked: Any Format Button")

            if self.ui.MP4.isChecked ( ):

                # ui.Custom.show()
                self.ui.Low.show ( )
                self.ui.High.show ( )
                self.ui.qts.setText (".mp4")

                if self.ui.Custom.isChecked ( ):
                    self.ui.CustomQ.show ( )


            elif self.ui.AVI.isChecked ( ):

                # ui.Custom.show()
                self.ui.Low.show ( )
                self.ui.High.show ( )
                self.ui.qts.setText (".avi")

                if self.ui.Custom.isChecked ( ):
                    self.ui.CustomQ.show ( )





            elif self.ui.MP3.isChecked ( ):
                self.ui.CustomQ.hide ( )
                self.ui.Custom.hide ( )
                self.ui.Low.hide ( )
                self.ui.High.hide ( )
                self.ui.qts.setText (".mp3")

            else:

                self.ui.CustomQ.hide ( )
                self.ui.Custom.hide ( )
                self.ui.Low.hide ( )
                self.ui.High.hide ( )

        def chenck():
            # link = self.ui.searchbar.text ( )
            # yt = YouTube (link, on_progress_callback=progress)
            # ----> Quality Checker
            print ("Clicked: Any Quality Button")
            if self.ui.Custom.isChecked ( ):
                self.ui.CustomQ.show ( )

            elif self.ui.High.isChecked ( ):
                self.ui.CustomQ.hide ( )
                self.ui.qts_2.setText (highres)
                self.ui.VideoSize_2.setText (str (round (highsize / (1024 * 1024))) + 'MB')

            elif self.ui.Low.isChecked ( ):
                self.ui.CustomQ.hide ( )
                self.ui.qts_2.setText (lowres)
                self.ui.VideoSize_2.setText (str (round (lowsize / (1024 * 1024))) + 'MB')
            else:
                self.ui.CustomQ.hide ( )

        def SCAN():
            # ----> Quality Scanner
            link = self.ui.searchbar.text ( )
            yt = YouTube (link, on_progress_callback=progress)
            fillse = yt.streams.get_highest_resolution ( )

            self.ui.High.setText (yt.streams.get_highest_resolution ( ).resolution)
            self.ui.Low.setText (yt.streams.get_lowest_resolution ( ).resolution)

            # ui.VideoSize.setText (str (round (yt.streams.get_highest_resolution ( ).filesize / (1024 * 1024))) + 'MB')
            vs = yt.streams.get_highest_resolution ( ).filesize / (1024 * 1024)

        def CANCEL():
            # ----> CANCEL TO PAGE1
            self.ui.stackedWidget.setCurrentWidget (self.ui.page)

        def NEXTY():
            link = self.ui.searchbar.text ( )
            yt = YouTube (link, on_progress_callback=progress_bar)
            fillse = yt.streams.get_highest_resolution ( )

            if self.ui.High.isChecked ( ):
                global vs
                vs = yt.streams.get_highest_resolution ( ).filesize / (1024 * 1024)
                vsd = yt.streams.get_highest_resolution ( ).filesize
            elif self.ui.Low.isChecked ( ):
                vs = yt.streams.get_highest_resolution ( ).filesize / (1024 * 1024)
                vsd = yt.streams.get_highest_resolution ( ).filesize
            elif self.ui.Custom.isChecked ( ):
                ...

            # \___________HATALAR___________/
            total, used, free = shutil.disk_usage ("/")
            nfree = free // (1024 * 1024)

            if self.ui.qts.text ( ) == "Format":
                rl = open ("error.txt", "w")
                rl.truncate (0)
                rl.write ("Select Format!|14", )
                rl.close ( )
                rl = open ("error.txt", "r")
                rlrd = rl.readline ( )
                print (len (rlrd))

                if len (rlrd) > 1:
                    MainError ( ).show ( )

            elif self.ui.qts_2.text ( ) == "Quality":
                rl = open ("error.txt", "w")
                rl.truncate (0)
                rl.write ("Select Quality!|14", )
                rl.close ( )
                rl = open ("error.txt", "r")
                rlrd = rl.readline ( )
                print (len (rlrd))

                if len (rlrd) > 1:
                    MainError ( ).show ( )

            #    elif nfree < vsd:
            #        rl = open ("error.txt", "w")
            #        rl.truncate (0)
            #        rl.write ("Not Enough Space Available On The Disk|10", )
            #        rl.close ( )
            #        rl = open ("error.txt", "r")
            #        rlrd = rl.readline ( )
            #        print (len (rlrd))

                if len (rlrd) > 1:
                    MainError ( ).show ( )

            else:

                self.ui.label_11.setText(f"{self.ui.Filebar.text()}{self.ui.qts.text()}")
                self.ui.label_12.setText(self.ui.qts_2.text())

                link = self.ui.searchbar.text ( )
                self.ui.stackedWidget.setCurrentWidget (self.ui.page_5)
                fillse = yt.streams.get_highest_resolution ( )
                self.ui.progressBar.setValue (10)

                Thread (target=DOWNLOAD, args=(fillse,), daemon=True).start ( )
                # DOWNLOAD()

        def DOWNLOAD(fillse):

            outpout = fillse.download (self.ui.FileLocName.text ( ))
            base, ext = os.path.splitext (outpout)
            new_file = base + f"{self.ui.qts.text()}"
            oldfile = self.ui.FileLocName.text ( ) + '\\' + self.ui.Filebar.text() + f"{self.ui.qts.text()}"
            print ("newfile", new_file)
            print("oldfile", oldfile)
            os.rename (outpout, oldfile)
            # if ui.High.isChecked():
            # fills = yt.streams.get_highest_resolution().filesize
            # vs = fills / (1024 * 1024)

            # yt.streams.get_highest_resolution().download()
            # elif ui.Low.isChecked():
            # fills = yt.streams.get_lowest_resolution().filesize
            # vs = fills / (1024 * 1024)
            # yt.streams.get_lowest_resolution().download()

        def progress(streams, chunk: bytes, bytes_remaining: int):  # Yükleme Barı
            vsd = yt.streams.get_highest_resolution ( ).filesize
            contentsize = vsd
            size = contentsize - bytes_remaining
            yuklenen = int(contentsize - bytes_remaining / (1024 * 1024))
            #yüklenen size
            #timer = 1
           # print (float (size / contentsize * 100))
           # global steer
           # steer = int (size / contentsize * 100)
           # print (int (size / contentsize * 100))
           # self.ui.progressBar.setValue (steer)

        def progress_bar(streams, chunk: bytes, bytes_remaining: int, ):
            contentsize = yt.streams.get_highest_resolution().filesize
            size = contentsize -  bytes_remaining
           # yuklenen = int(contentsize - bytes_remaining / (1024 * 1024))
            timer = 1
            steer = int (size / contentsize * 100)
            print(str(steer))
            if steer > 8:
                self.ui.progressBar.setValue (steer)
            self.ui.VideoSize_5.setText (str (self.ui.progressBar.value ( )) + "%")

            self.ui.VideoSize_4.setText(str(int(size / (1024 * 1024))) + "MB")
            self.ui.VideoSize_3.setText(self.ui.VideoSize_2.text())


        # PAGE4

        def openfiler():
            print(self.ui.FileLocName.text() + "\\" + self.ui.Filebar.text() + self.ui.qts.text())
            os.startfile(self.ui.FileLocName.text() + "\\" + self.ui.Filebar.text() + self.ui.qts.text())
        def openfolder():
            subprocess.Popen (f'explorer /open,{self.ui.FileLocName.text()}')
        def mainpage():
            self.ui.searchbar.setText("")
            self.ui.finder.setEnabled(True)
            self.ui.loading.hide()
        def closesynmax():
            self.close()
        #########
        ##########ALL BUTTONS##########
        #########

        # PAGE1
        self.ui.finder.clicked.connect (FIND)

        # PAGE3(2)
        self.ui.pushButton_7.clicked.connect (RANDOMS)
        self.ui.finder_p_2.clicked.connect(CONITE)
        self.ui.finder_p_5.clicked.connect(PAGE3)
        self.ui.defay.clicked.connect (DEFLT)
        self.ui.findfoldr.clicked.connect (openFile)
        self.ui.pushButton_8.clicked.connect (DEFAULT)
        self.ui.MP4.clicked.connect (check)
        self.ui.MP3.clicked.connect (check)
        self.ui.AVI.clicked.connect (check)
        self.ui.Low.clicked.connect (chenck)
        self.ui.High.clicked.connect (chenck)
        self.ui.Custom.clicked.connect (chenck)
        self.ui.pushButton_5.clicked.connect (CANCEL)
        self.ui.pushButton_6.clicked.connect (NEXTY)
        self.ui.openfilebutton.clicked.connect(openfiler)
        self.ui.openfilefolder.clicked.connect(openfolder)
        self.ui.retrunpage1.clicked.connect(mainpage)
        self.ui.closesynmax.clicked.connect(closesynmax)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos ( )

    def showTime(self):
        global link
        global yt
        link = self.ui.searchbar.text ( )

        if self.ui.progressBar.value() == 100:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_6)


class MainError (QMainWindow):
    def __init__(self):
        super (MainError, self).__init__ ( )
        self.ui = Ui_Dialog ( )
        self.ui.setupUi (self)
        rlf = open ("error.txt", "r")
        rl = rlf.readline ( )
        name, fsize = rl.split ("|")
        self.ui.error.setText (name)
        self.ui.error.setFont (QFont ("MS Shell Dlg 2", int (fsize)))
        self.setWindowFlags (QtCore.Qt.FramelessWindowHint)
        self.setAttribute (QtCore.Qt.WA_TranslucentBackground)

        self.ui.close.clicked.connect (lambda: self.close ( ))
        self.ui.Ok.clicked.connect (lambda: self.close ( ))
        self.ui.icona.clicked.connect (lambda: self.showMinimized ( ))

        self.dragPos = self.pos ( )

        def mouseMoveEvent(event):
            delta = QPoint (self.pos ( ) + event.globalPos ( ) - self.dragPos)
            # print (self.pos ( ) + event.globalPos ( ) - self.dragPos)
            self.move (self.pos ( ) + event.globalPos ( ) - self.dragPos)
            self.dragPos = event.globalPos ( )
            event.accept ( )

        # WIDGET HAREKETİ
        self.ui.titlebar.mouseMoveEvent = mouseMoveEvent
        ################

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos ( )


if __name__ == '__main__':
    app = QApplication (sys.argv)
    ex = MainWindow ( )
    ex.show ( )
    app.setWindowIcon (QtGui.QIcon ("icon.ico"))
    ex.setWindowIcon (QtGui.QIcon ("icon.ico"))
    sys.exit (app.exec_ ( ))