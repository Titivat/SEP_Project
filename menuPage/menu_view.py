# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Menu_ui2.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets
import resources_rc

class Menu_view(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.wallpaper = QtWidgets.QLabel(self.centralwidget)
        self.wallpaper.setGeometry(QtCore.QRect(0, -10, 1000, 500))
        self.wallpaper.setText("")
        self.wallpaper.setPixmap(QtGui.QPixmap(":/background/menuBackground.png"))
        self.wallpaper.setObjectName("wallpaper")
        
        self.menupic = QtWidgets.QLabel(self.centralwidget)
        self.menupic.setGeometry(QtCore.QRect(60, 30, 151, 141))
        self.menupic.setText("")
        self.menupic.setPixmap(QtGui.QPixmap(":/icon/menu_user_icon.png"))
        self.menupic.setObjectName("menupic")

        self.adddrivepic = QtWidgets.QLabel(self.centralwidget)
        self.adddrivepic.setGeometry(QtCore.QRect(30, 220, 41, 41))
        self.adddrivepic.setText("")
        self.adddrivepic.setPixmap(QtGui.QPixmap(":/icon/add_icon.png"))
        self.adddrivepic.setObjectName("adddrivepic")

        self.mydrivepic = QtWidgets.QLabel(self.centralwidget)
        self.mydrivepic.setGeometry(QtCore.QRect(30, 280, 41, 41))
        self.mydrivepic.setText("")
        self.mydrivepic.setPixmap(QtGui.QPixmap(":/icon/myDirveIcon.jpg"))
        self.mydrivepic.setObjectName("mydrivepic")

        self.sharedrivepic = QtWidgets.QLabel(self.centralwidget)
        self.sharedrivepic.setGeometry(QtCore.QRect(30, 340, 41, 41))
        self.sharedrivepic.setText("")
        self.sharedrivepic.setPixmap(QtGui.QPixmap(":/icon/shareIcon.png"))
        self.sharedrivepic.setObjectName("sharedrivepic")

        self.adddocbutton = QtWidgets.QPushButton(self.centralwidget)
        self.adddocbutton.setGeometry(QtCore.QRect(72, 227, 121, 31))
        self.adddocbutton.setStyleSheet("\n"
"background-color: rgb(255, 255, 255);")
        self.adddocbutton.setCheckable(False)
        self.adddocbutton.setAutoRepeat(False)
        self.adddocbutton.setObjectName("adddocbutton")
        
        self.mydrivebutton = QtWidgets.QPushButton(self.centralwidget)
        self.mydrivebutton.setGeometry(QtCore.QRect(72, 287, 121, 31))
        self.mydrivebutton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.mydrivebutton.setObjectName("mydrivebutton")
        self.sharedrivebutton = QtWidgets.QPushButton(self.centralwidget)
        self.sharedrivebutton.setGeometry(QtCore.QRect(70, 347, 121, 31))
        self.sharedrivebutton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.sharedrivebutton.setObjectName("sharedrivebutton")
        self.logoutbutton = QtWidgets.QPushButton(self.centralwidget)
        self.logoutbutton.setGeometry(QtCore.QRect(70, 407, 121, 31))
        self.logoutbutton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.logoutbutton.setObjectName("logoutbutton")
        self.logoutpic = QtWidgets.QLabel(self.centralwidget)
        self.logoutpic.setGeometry(QtCore.QRect(30, 400, 41, 41))
        self.logoutpic.setText("")
        self.logoutpic.setPixmap(QtGui.QPixmap(":/icon/logoutIcon.png"))
        self.logoutpic.setObjectName("logoutpic")

        self.pagestatus = QtWidgets.QLabel(self.centralwidget)
        self.pagestatus.setGeometry(QtCore.QRect( 390 , 10, 360, 80 ))
        self.pagestatus.setObjectName("pagestatus")
        self.pagestatus.resize( 460 , 100 )

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(300, 120, 671, 311))
        self.listWidget.setObjectName("listWidget")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.adddocbutton.setText(_translate("MainWindow", "Add Document"))
        self.mydrivebutton.setText(_translate("MainWindow", "My Drive"))
        self.sharedrivebutton.setText(_translate("MainWindow", "Share Drive"))
        self.logoutbutton.setText(_translate("MainWindow", "Log Out"))
        self.pagestatus.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; font-weight:600;\">My Drive</span></p></body></html>"))

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Menu_view()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
