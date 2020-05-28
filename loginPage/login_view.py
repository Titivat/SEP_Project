# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'finalLogin.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Ui_Form(object):
    def setupUi(self, Form):
        if Form.objectName():
            Form.setObjectName(u"Login page")
        Form.resize(1000, 500)
        self.logintext = QLabel(Form)
        self.logintext.setObjectName(u"logintext")
        self.logintext.setGeometry( QRect( 125  , 60, 150, 41))
        self.logintext.setStyleSheet(" color: #FFFFFF; font-size: 30px;font-weight: bold;")

        self.usericon = QLabel(Form)
        self.usericon.setObjectName(u"usericon")
        self.usericon.setGeometry(QRect(70, 250, 41, 41))
        self.usericon.setPixmap(QPixmap(u"loginPage/images/small_user_icon.png"))

        self.passwordicon = QLabel(Form)
        self.passwordicon.setObjectName(u"passwordicon")
        self.passwordicon.setGeometry(QRect(70, 300, 41, 41))
        self.passwordicon.setPixmap(QPixmap(u"loginPage/images/password_icon.png"))

        self.loginicon = QLabel(Form)
        self.loginicon.setObjectName(u"loginicon")
        self.loginicon.setGeometry(QRect(110, 120, 131, 121))
        self.loginicon.setPixmap(QPixmap(u"loginPage/images/user_icon.png"))

        self.registerbutton = QPushButton(Form)
        self.registerbutton.setObjectName(u"registerbutton")
        self.registerbutton.setGeometry(QRect( 70 , 360, 50, 30))
        self.registerbutton.resize( 200 , 30 )

        self.loginbutton = QPushButton( Form )
        self.loginbutton.setGeometry( QRect( 70 , 400, 50, 30 ))
        self.loginbutton.setObjectName("loginbutton")
        self.loginbutton.resize( 200 , 30 )
           
        self.useredit = QLineEdit(Form)
        self.useredit.setObjectName(u"")
        self.useredit.setGeometry(QRect(110, 250, 161, 41))
        self.useredit.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.useredit.setEchoMode(QLineEdit.Normal)

        self.passwordedit = QLineEdit(Form)
        self.passwordedit.setObjectName(u"")
        self.passwordedit.setGeometry(QRect(110, 300, 161, 41))
        self.passwordedit.setEchoMode(QLineEdit.PasswordEchoOnEdit)  

        self.wallpaper = QLabel(Form)
        self.wallpaper.setObjectName(u"wallpaper")
        self.wallpaper.setGeometry(QRect(0, 0, 1000, 500))
        self.wallpaper.setStyleSheet(u"background-image: url(loginPage/images/enterBackground - Copy.jpg);")
        self.wallpaper.setPixmap(QPixmap(u":/background/enterBackground - Copy.jpg"))
        
        self.wallpaper.raise_()
        self.logintext.raise_()
        self.usericon.raise_()
        self.passwordicon.raise_()
        self.registerbutton.raise_()
        self.useredit.raise_()
        self.loginbutton.raise_()
        self.loginicon.raise_()
        self.passwordedit.raise_()

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.logintext.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:20pt; font-weight:600; color:#ffffff;\">Login</span></p></body></html>", None))
        self.usericon.setText("")
        self.passwordicon.setText("")
        self.registerbutton.setText(QCoreApplication.translate("Form", u"Register", None))
        self.useredit.setInputMask("")
        self.useredit.setText(QCoreApplication.translate("Form", u"", None))
        self.loginbutton.setText(QCoreApplication.translate("Form", u"Log in", None))
        self.loginicon.setText("")
        self.passwordedit.setText(QCoreApplication.translate("Form", u"", None))
        self.wallpaper.setText("")
    # retranslateUi

