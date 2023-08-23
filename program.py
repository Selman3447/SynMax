import os
import random
from pathlib import Path

from random import *
import shutil
import subprocess
from configparser import ConfigParser
import sqlite3
import pyperclip

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
config_object = ConfigParser()

f = open("config.ini", "r")

if len(f.read()) == 0:
    home = str(Path.home())
    down = home + "\Downloads"


    config_object["Settings"] = {
        "DefaultPath": f"{down}",
        "Autodownload": "0",
    }

    config_object["AD_Qualitys"] = {
        "High": "1",
        "Low": "0",
    }

    config_object["AD_FileName"] = {
        "Default": "1",
        "Random": "0",
    }

    config_object["AD_FileLoc"] = {
        "Default": "1",
        "Custom": "0",
    }

    with open('config.ini', 'w') as conf:
        config_object.write(conf)


f.close()


connect = sqlite3.connect("varaibles.db")
cursor = connect.cursor()
cursor.execute('DELETE FROM Varaibles;',)
connect.commit()


Developer_Mode = True

print ("Program loading...")

TIME_LIMIT = 100
class MainWindow (QMainWindow):
    def __init__(self):
        super (MainWindow, self).__init__ ( )
        self.ui = Ui_SplashScreen ( )
        self.ui.setupUi (self)

        fihrist = open(os.getcwd() + r"\titleset.txt", "r")
        rl = fihrist.readline()

        _translate = QtCore.QCoreApplication.translate
        name, version = rl.split("|")
        self.setWindowTitle(_translate("SplashScreen", f"{name} {version}"))
        self.ui.label_2.setText(self.windowTitle())

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.searchbar.setText("https://www.youtube.com/watch?v=MhNzdYeBIVs")

        movie = QMovie ("loading.gif")
        self.ui.loading.setMovie (movie)
        movie.start ( )
        self.ui.loading.hide()
        movie = QMovie ("loading.gif")
        self.ui.loading_2.setMovie (movie)
        movie.start ( )
        self.ui.loading_2.hide()


        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

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

        #########
        ##########ALL DEF##########
        #########
        # PAGE1

        def YtFinder():
            link = self.ui.searchbar.text()
            global yt
            yt = YouTube(link, on_progress_callback=progress_bar)
            fillse = yt.streams.first()
            try:
                highsize = yt.streams.get_highest_resolution ( ).filesize
                lowsize = yt.streams.get_lowest_resolution ( ).filesize
                highres = yt.streams.get_highest_resolution ( ).resolution
                lowres = yt.streams.get_lowest_resolution ( ).resolution
                connect = sqlite3.connect("varaibles.db")
                cursor = connect.cursor()
                cursor.execute(f"INSERT INTO Varaibles VALUES('highsize', '{yt.streams.get_highest_resolution ( ).filesize}')")
                cursor.execute(f"INSERT INTO Varaibles VALUES('lowsize', '{yt.streams.get_lowest_resolution ( ).filesize}')")
                cursor.execute(f"INSERT INTO Varaibles VALUES('highres', '{yt.streams.get_highest_resolution ( ).resolution}')")
                cursor.execute(f"INSERT INTO Varaibles VALUES('lowres', '{yt.streams.get_lowest_resolution ( ).resolution}')")

                cursor.execute(f"INSERT INTO Varaibles VALUES('findstatus', 'Yes')")
                connect.commit()
                findstatus = "Yes"
                url = yt.thumbnail_url
                urllib.request.urlretrieve (url,
                                            os.getcwd ( ) + r'\thunbail.jpg')  # Kapak Fotoğrafını Belirtilen Yola kaydediyor. ( os.getcwd() projenin konumunu buluyor)

                if Developer_Mode:
                    print("Video Algılandı:")
                    print(f"Başlık: {yt.title}")
                    print(f"Kanal: {yt.author}")
                    print(round(yt.length / 60), ":", yt.length % 60)  # Video Süresi Süre/60(Dakika) : Süre%60 (Saniye)
                    print(os.getcwd() + r'\thunbail.jpg', 'konumuna', 'thubail.jpg olarak kaydedildi.')
                self.ui.thumbnail.setPixmap(QtGui.QPixmap("thunbail.jpg"))
                self.ui.ytitle.setText(yt.title)
                self.ui.ytauthor.setText(yt.author)
                d = yt.length / 60
                s = yt.length % 60
                self.ui.ytime.setText(str (round (d)) + " : " + str (round (s)))
                self.ui.description.setText(yt.description)
                if len(yt.description) == 0:
                    self.ui.description.setText("No Description")
                self.ui.stackedWidget.setCurrentWidget (self.ui.page_2)

            except:
                pass
        def Finder():
            self.ui.finder.setEnabled (False)
            self.ui.searchbar.setEnabled (False)

            self.ui.frame_4.hide()
            self.ui.searchbar.hide()
            self.ui.url.hide()
            self.ui.finder.hide()
            self.ui.frame_5.hide()
            self.ui.urlplaylist.hide()
            self.ui.finder_p.hide()
            self.ui.searchbar_p.hide()

            self.ui.loading.show()
            self.ui.loading.setGeometry(100, 110, 411, 261)
            if Developer_Mode:
                print("Clicked: Find Button")
            Thread (target=YtFinder, daemon=True).start ( )
        def Nexto2():
            self.ui.thumbnai2.setPixmap(QtGui.QPixmap('thunbail.jpg'))
            self.ui.vidname_2.setText(self.ui.ytitle.text())
            self.ui.stackedWidget.setCurrentIndex(2)
        # PAGE2
        def random():
            try:
                sayi1 = Random().randint(1000000000, 9999999999)
                sayi2 = Random().randint(1000000000, 9999999999)
            except Exception as e:
                print(e)

            self.ui.Filebar.setText (str (sayi1) + "_" + str (sayi2))

        def default():
            fname = self.ui.ytitle.text()
            self.ui.Filebar.setText(fname)
        def defaloc():
            config_object.read("config.ini")
            default = config_object["Settings"]["defaultpath"]
            self.ui.FileLocName.setText(default)
        def openFile():
            # ----> Folder dialog
            root = Tk ( )
            root.withdraw ( )
            filepath = filedialog.askdirectory ( )
            filepath = filepath.replace("/", "\\")
            print (filepath)
            root.destroy ( )
            self.ui.FileLocName.setText (filepath)
        def nexto3():
            if not Developer_Mode:
                self.ui.qts.hide()
                self.ui.qts_2.hide()
            self.ui.thumbnai2_2.setPixmap(QtGui.QPixmap("thunbail.jpg"))
            self.ui.vidname_3.setText(self.ui.ytitle.text())
            self.ui.VideoSize_2.setText("Waiting...")

            self.ui.High.setText (yt.streams.get_highest_resolution ( ).resolution)
            self.ui.Low.setText (yt.streams.get_lowest_resolution ( ).resolution)
            self.ui.stackedWidget.setCurrentIndex(3)

            self.ui.Custom.hide()
            self.ui.CustomQ.hide()
            self.ui.Low.hide()
            self.ui.High.hide()
        # PAGE 3

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

                def get_highest_audio():
                    best_audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
                    return best_audio_stream

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
                cursor.execute(f"""SELECT * FROM Varaibles WHERE NAME = 'highres'""")
                highres = cursor.fetchone()[1]
                cursor.execute(f"""SELECT * FROM Varaibles WHERE NAME = 'highsize'""")
                highsize = cursor.fetchone()[1]
                self.ui.qts_2.setText (highres)
                self.ui.VideoSize_2.setText (str (round (highsize / (1024 * 1024))) + 'MB')

            elif self.ui.Low.isChecked ( ):
                cursor.execute(f"""SELECT * FROM Varaibles WHERE NAME = 'lowres'""")
                lowres = cursor.fetchone()[1]
                self.ui.CustomQ.hide ( )
                self.ui.qts_2.setText (lowres)
                cursor.execute(f"""SELECT * FROM Varaibles WHERE NAME = 'lowsize'""")
                lowsize = cursor.fetchone()[1]
                self.ui.VideoSize_2.setText (str (round (lowsize / (1024 * 1024))) + 'MB')
            else:
                self.ui.CustomQ.hide ( )

        def nexto4():
            link = self.ui.searchbar.text()
            yt = YouTube(link, on_progress_callback=progress_bar)
            if self.ui.MP3.isChecked():
                fillse = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
                self.ui.label_12.setText(fillse.abr)
            elif self.ui.Low.isChecked():
                fillse = yt.streams.get_lowest_resolution()
                self.ui.label_12.setText(fillse.resolution)
            elif self.ui.High.isChecked():
                fillse = yt.streams.get_highest_resolution()
                self.ui.label_12.setText(fillse.resolution)
            else:
                fillse = yt.streams.get_highest_resolution()
                self.ui.label_12.setText("(Auto) " + fillse.resolution)

            self.ui.progressBar.setValue(10)
            self.ui.VideoSize_5.setText("%0")
            self.ui.label_11.setText(f"{self.ui.Filebar.text()}.{self.ui.qts.text()}")
            self.ui.VideoSize_3.setText(self.ui.VideoSize_2.text())
            self.ui.VideoSize_4.setText("0 MB")
            self.ui.stackedWidget.setCurrentIndex(4)


            Thread(target=DOWNLOAD, args=(fillse,), daemon=True).start()

        def DOWNLOAD(fillse):
            link = self.ui.searchbar.text()
            yt = YouTube(link, on_progress_callback=progress_bar)

            outpout = fillse.download (self.ui.FileLocName.text ( ))
            base, ext = os.path.splitext (outpout)
            new_file = base + f"{self.ui.qts.text()}"
            oldfile = self.ui.FileLocName.text ( ) + '\\' + self.ui.Filebar.text() + f"{self.ui.qts.text()}"
            print ("newfile", new_file)
            print("oldfile", oldfile)
            os.rename (outpout, oldfile)
            self.ui.stackedWidget.setCurrentIndex(5)
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

        def progress_bar(bytes_remaining: int, ):
            contentsize = yt.streams.get_highest_resolution().filesize
            size = contentsize -  bytes_remaining
           # yuklenen = int(contentsize - bytes_remaining / (1024 * 1024))
            steer = int (size / contentsize * 100)
            if Developer_Mode:
                print(str(steer))
            if steer > 8:
                self.ui.progressBar.setValue (steer)
                self.ui.VideoSize_4.setText(str(int(size / (1024 * 1024))) + "MB")
            self.ui.VideoSize_5.setText (str (self.ui.progressBar.value ( )) + "%")

            self.ui.VideoSize_4.setText(str(int(size / (1024 * 1024))) + "MB")

        #########
        ##########ALL BUTTONS##########
        #########
        # PAGE1
        self.ui.finder.clicked.connect(Finder)
        self.ui.paster.clicked.connect(lambda: self.ui.searchbar.setText(pyperclip.paste() ))
        self.ui.paster_2.clicked.connect(lambda: self.ui.searchbar_p.setText(pyperclip.paste() ))
        # PAGE2
        self.ui.finder_p_2.clicked.connect(Nexto2)
        # PAGE3
        self.ui.pushButton_7.clicked.connect(random)
        self.ui.defay.clicked.connect(default)
        self.ui.pushButton_8.clicked.connect(defaloc)
        self.ui.findfoldr.clicked.connect(openFile)
        self.ui.finder_p_5.clicked.connect(nexto3)
        # PAGE4
        self.ui.MP4.clicked.connect (check)
        self.ui.MP3.clicked.connect (check)
        self.ui.AVI.clicked.connect (check)
        self.ui.Low.clicked.connect (chenck)
        self.ui.High.clicked.connect (chenck)
        self.ui.Custom.clicked.connect (chenck)
        self.ui.pushButton_6.clicked.connect(nexto4)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos ( )


if __name__ == '__main__':
    app = QApplication (sys.argv)
    ex = MainWindow ( )
    ex.show ( )
    app.setWindowIcon (QtGui.QIcon ("icon.ico"))
    ex.setWindowIcon (QtGui.QIcon ("icon.ico"))
    sys.exit (app.exec_ ( ))