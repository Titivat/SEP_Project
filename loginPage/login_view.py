# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PySide2 import QtCore, QtGui, QtWidgets
import resources_rc

class Login_view(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1000, 500)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.usericon = QtWidgets.QLabel(self.centralwidget)
        self.usericon.setGeometry(QtCore.QRect(40, 190, 41, 41))
        self.usericon.setText("")
        self.usericon.setPixmap(QtGui.QPixmap(":/icon/small_user_icon.png"))
        self.usericon.setObjectName("usericon")
        self.passwordicon = QtWidgets.QLabel(self.centralwidget)
        self.passwordicon.setGeometry(QtCore.QRect(40, 240, 41, 41))
        self.passwordicon.setText("")
        self.passwordicon.setPixmap(QtGui.QPixmap(":/icon/password_icon.png"))
        self.passwordicon.setObjectName("passwordicon")

        self.loginicon = QtWidgets.QLabel(self.centralwidget)
        self.loginicon.setGeometry(QtCore.QRect(80, 60, 131, 121))
        self.loginicon.setText("")
        self.loginicon.setPixmap(QtGui.QPixmap(":/icon/user_icon.png"))
        self.loginicon.setObjectName("loginicon")
        
        self.logintext = QtWidgets.QLabel(self.centralwidget)
        self.logintext.setGeometry(QtCore.QRect( 90, 10, 81, 41))
        self.logintext.setObjectName("logintext")
        self.logintext.resize( 200 , 50 )
        self.logintext.setStyleSheet(" color: #FFFFFF; font-size: 30px;font-weight: bold;")
        
        self.useredit = QtWidgets.QLineEdit(self.centralwidget)
        self.useredit.setGeometry(QtCore.QRect(80, 190, 161, 41))
        self.useredit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.useredit.setInputMask("")
        self.useredit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.useredit.setObjectName("useredit")

        self.passwordedit = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordedit.setGeometry(QtCore.QRect(80, 240, 161, 41))
        self.passwordedit.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.passwordedit.setObjectName("passwordedit")

        self.wallpaper = QtWidgets.QLabel(self.centralwidget)
        self.wallpaper.setGeometry(QtCore.QRect(0, 0, 1000, 500))
        self.wallpaper.setStyleSheet("background-image: url(:/background/enterBackground - Copy.jpg);")
        self.wallpaper.setText("")
        self.wallpaper.setPixmap(QtGui.QPixmap(":/background/enterBackground - Copy.jpg"))
        self.wallpaper.setObjectName("wallpaper")
        
        self.registerbutton = QtWidgets.QPushButton(self.centralwidget)
        self.registerbutton.setObjectName("registerbutton")
        self.registerbutton.setGeometry( QtCore.QRect( 40 , 290 , 93, 28) )
        self.registerbutton.resize( 200 , 30 )

        self.loginbutton = QtWidgets.QPushButton(self.centralwidget)
        self.loginbutton.setGeometry(QtCore.QRect(40, 330, 93, 28))
        self.loginbutton.setObjectName("loginbutton")
        self.loginbutton.resize( 200 , 30 )
        
        self.wallpaper.raise_()
        self.usericon.raise_()
        self.passwordicon.raise_()
        self.loginicon.raise_()
        self.logintext.raise_()
        self.useredit.raise_()
        self.passwordedit.raise_()
        self.registerbutton.raise_()
        self.loginbutton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 26))
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
        self.logintext.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600; color:#ffffff;\">Login</span></p></body></html>"))
        self.useredit.setText(_translate("MainWindow", "Username"))
        self.passwordedit.setText(_translate("MainWindow", "Password"))
        self.registerbutton.setText(_translate("MainWindow", "Register"))
        self.loginbutton.setText(_translate("MainWindow", "Log in"))



# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
