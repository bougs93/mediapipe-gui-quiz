# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_user_reg.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,
    QWidget)

class Ui_user_reg(object):
    def setupUi(self, user_reg):
        if not user_reg.objectName():
            user_reg.setObjectName(u"user_reg")
        user_reg.resize(1280, 1024)
        self.fr_top_quiz = QFrame(user_reg)
        self.fr_top_quiz.setObjectName(u"fr_top_quiz")
        self.fr_top_quiz.setEnabled(True)
        self.fr_top_quiz.setGeometry(QRect(10, 10, 1261, 91))
        self.fr_top_quiz.setStyleSheet(u"background-color: #E65100;\n"
"border-radius: 10px;")
        self.fr_top_quiz.setFrameShape(QFrame.StyledPanel)
        self.fr_top_quiz.setFrameShadow(QFrame.Raised)
        self.lb_fps = QLabel(user_reg)
        self.lb_fps.setObjectName(u"lb_fps")
        self.lb_fps.setGeometry(QRect(1140, 1000, 131, 21))
        font = QFont()
        font.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font.setPointSize(11)
        self.lb_fps.setFont(font)
        self.lb_fps.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgba(255, 255, 255, 150);")
        self.lb_fps.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.fr_main_quiz = QFrame(user_reg)
        self.fr_main_quiz.setObjectName(u"fr_main_quiz")
        self.fr_main_quiz.setGeometry(QRect(10, 120, 1251, 881))
        self.fr_main_quiz.setFrameShape(QFrame.StyledPanel)
        self.fr_main_quiz.setFrameShadow(QFrame.Raised)
        self.lb_chAnswer = QLabel(self.fr_main_quiz)
        self.lb_chAnswer.setObjectName(u"lb_chAnswer")
        self.lb_chAnswer.setGeometry(QRect(220, 660, 801, 81))
        self.lb_chAnswer.setMinimumSize(QSize(110, 0))
        font1 = QFont()
        font1.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc ExtraBold"])
        font1.setPointSize(28)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.lb_chAnswer.setFont(font1)
        self.lb_chAnswer.setStyleSheet(u"background-color: rgba(255, 255, 255, 150);\n"
"border-radius: 30px;")
        self.lb_chAnswer.setAlignment(Qt.AlignCenter)
        self.lb_chAnswer.setWordWrap(True)
        self.lb_question = QLabel(self.fr_main_quiz)
        self.lb_question.setObjectName(u"lb_question")
        self.lb_question.setGeometry(QRect(10, 0, 1241, 361))
        self.lb_question.setMinimumSize(QSize(110, 0))
        font2 = QFont()
        font2.setFamilies([u"NanumSquareRound"])
        font2.setPointSize(25)
        font2.setBold(True)
        self.lb_question.setFont(font2)
        self.lb_question.setAutoFillBackground(False)
        self.lb_question.setStyleSheet(u"background-color: rgba(255, 224, 178, 180);\n"
"border-radius: 30px;")
        self.lb_question.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_question.setWordWrap(True)
        self.lb_msg = QLabel(self.fr_main_quiz)
        self.lb_msg.setObjectName(u"lb_msg")
        self.lb_msg.setGeometry(QRect(50, 0, 1181, 361))
        font3 = QFont()
        font3.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc ExtraBold"])
        font3.setPointSize(25)
        font3.setBold(True)
        self.lb_msg.setFont(font3)
        self.lb_msg.setStyleSheet(u"")
        self.lb_id = QLabel(self.fr_main_quiz)
        self.lb_id.setObjectName(u"lb_id")
        self.lb_id.setGeometry(QRect(480, 560, 241, 81))
        font4 = QFont()
        font4.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc ExtraBold"])
        font4.setPointSize(30)
        self.lb_id.setFont(font4)
        self.lb_id.setStyleSheet(u"background-color: rgb(63, 81, 181);\n"
"border-radius: 30px;\n"
"color: rgb(255, 255, 255);")
        self.lb_id.setAlignment(Qt.AlignCenter)
        self.lb_name = QLabel(self.fr_main_quiz)
        self.lb_name.setObjectName(u"lb_name")
        self.lb_name.setGeometry(QRect(730, 560, 331, 81))
        self.lb_name.setFont(font4)
        self.lb_name.setStyleSheet(u"background-color: rgb(63, 81, 181);\n"
"border-radius: 30px;\n"
"color: rgb(255, 255, 255);")
        self.lb_name.setAlignment(Qt.AlignCenter)
        self.lb_chAnswer_2 = QLabel(self.fr_main_quiz)
        self.lb_chAnswer_2.setObjectName(u"lb_chAnswer_2")
        self.lb_chAnswer_2.setGeometry(QRect(270, 560, 201, 81))
        self.lb_chAnswer_2.setMinimumSize(QSize(110, 0))
        font5 = QFont()
        font5.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc ExtraBold"])
        font5.setPointSize(30)
        font5.setBold(True)
        font5.setItalic(False)
        font5.setUnderline(False)
        font5.setStrikeOut(False)
        font5.setKerning(True)
        self.lb_chAnswer_2.setFont(font5)
        self.lb_chAnswer_2.setStyleSheet(u"background-color: rgba(255, 255, 255, 60);\n"
"border-radius: 30px;")
        self.lb_chAnswer_2.setAlignment(Qt.AlignCenter)
        self.lb_chAnswer_2.setWordWrap(True)
        self.lb_grade = QLabel(self.fr_main_quiz)
        self.lb_grade.setObjectName(u"lb_grade")
        self.lb_grade.setGeometry(QRect(820, 470, 241, 81))
        self.lb_grade.setFont(font4)
        self.lb_grade.setStyleSheet(u"background-color: rgb(63, 81, 181);\n"
"border-radius: 30px;\n"
"color: rgb(255, 255, 255);")
        self.lb_grade.setAlignment(Qt.AlignCenter)
        self.lb_school = QLabel(self.fr_main_quiz)
        self.lb_school.setObjectName(u"lb_school")
        self.lb_school.setGeometry(QRect(480, 470, 331, 81))
        self.lb_school.setFont(font4)
        self.lb_school.setStyleSheet(u"background-color: rgb(63, 81, 181);\n"
"border-radius: 30px;\n"
"color: rgb(255, 255, 255);")
        self.lb_school.setAlignment(Qt.AlignCenter)
        self.lb_quiz_name = QLabel(self.fr_main_quiz)
        self.lb_quiz_name.setObjectName(u"lb_quiz_name")
        self.lb_quiz_name.setGeometry(QRect(20, 470, 451, 81))
        self.lb_quiz_name.setFont(font4)
        self.lb_quiz_name.setStyleSheet(u"background-color: #E65100;\n"
"border-radius: 30px;\n"
"color: rgb(255, 255, 255);")
        self.lb_quiz_name.setAlignment(Qt.AlignCenter)
        self.lb_imageView = QLabel(user_reg)
        self.lb_imageView.setObjectName(u"lb_imageView")
        self.lb_imageView.setGeometry(QRect(10, 110, 1261, 901))
        font6 = QFont()
        font6.setPointSize(28)
        self.lb_imageView.setFont(font6)
        self.lb_imageView.setStyleSheet(u"background-color: rgb(188, 188, 188);\n"
"border-radius: 30px;")
        self.lb_imageView.setAlignment(Qt.AlignCenter)
        self.label = QLabel(user_reg)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(300, 30, 711, 51))
        font7 = QFont()
        font7.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc ExtraBold"])
        font7.setPointSize(35)
        font7.setBold(True)
        self.label.setFont(font7)
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label.setAlignment(Qt.AlignCenter)
        self.lb_keytime = QLabel(user_reg)
        self.lb_keytime.setObjectName(u"lb_keytime")
        self.lb_keytime.setGeometry(QRect(22, 16, 231, 31))
        font8 = QFont()
        font8.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc ExtraBold"])
        font8.setPointSize(15)
        font8.setBold(True)
        self.lb_keytime.setFont(font8)
        self.center_progress = QFrame(user_reg)
        self.center_progress.setObjectName(u"center_progress")
        self.center_progress.setGeometry(QRect(460, 330, 350, 350))
        self.center_progress.setFrameShape(QFrame.StyledPanel)
        self.center_progress.setFrameShadow(QFrame.Raised)
        self.lb_verInfo = QLabel(user_reg)
        self.lb_verInfo.setObjectName(u"lb_verInfo")
        self.lb_verInfo.setGeometry(QRect(10, 1000, 600, 21))
        self.lb_verInfo.setFont(font)
        self.lb_verInfo.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgba(255, 255, 255, 150);")
        self.lb_verInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_imageView.raise_()
        self.fr_top_quiz.raise_()
        self.lb_fps.raise_()
        self.fr_main_quiz.raise_()
        self.label.raise_()
        self.lb_keytime.raise_()
        self.center_progress.raise_()
        self.lb_verInfo.raise_()

        self.retranslateUi(user_reg)

        QMetaObject.connectSlotsByName(user_reg)
    # setupUi

    def retranslateUi(self, user_reg):
        user_reg.setWindowTitle(QCoreApplication.translate("user_reg", u"Form", None))
        self.lb_fps.setText(QCoreApplication.translate("user_reg", u"FPS", None))
        self.lb_chAnswer.setText(QCoreApplication.translate("user_reg", u"[OK]\ub204\ub974\uace0 \uc788\uc73c\uba74 \ud034\uc988\ub97c \uc2dc\uc791\ud569\ub2c8\ub2e4.", None))
        self.lb_question.setText("")
        self.lb_msg.setText(QCoreApplication.translate("user_reg", u"<html><head/><body><p>- <span style=\" color:#0055ff;\">\uac1c\uc778\uc815\ubcf4 \uc870\ud68c</span> \ub3d9\uc758\ud558\uace0 \uc2dc\uc791</p><p>&nbsp;&nbsp;<span style=\" color:#ff0000;\">\ud559\uc0dd \uc810\uc218 \uae30\ub85d</span>\uc744 \uc704\ud574 \uc815\ubcf4 \uc870\ud68c\ub97c \ub3d9\uc758 \ud558\ub294 \uacbd\uc6b0 <span style=\" color:#0055ff;\">\ud559\ub144, \ubc18, \ubc88\ud638</span>\uc744 \uc5f0\uc18d\uc73c\ub85c \uc785\ub825\ud6c4</p><p>&nbsp;&nbsp;[OK] \ub97c \ub20c\ub824\uc8fc\uc138\uc694. (\uc608\uc2dc) 2\ud559\ub144 9\ubc18 2\ubc88 -&gt; 2902[OK] </p><p>- \uc815\ubcf4 \uc870\ud68c \uc5c6\uc774 <span style=\" color:#ff0000;\">\uc190\ub2d8</span>\uc73c\ub85c \uc2dc\uc791</p><p>&nbsp;&nbsp;\ud559\ubc88 \uc870\ud68c\uc5c6\uc774 [OK]\uc120\ud0dd\ud558\uba74 \u2018\uc190\ub2d8\u2019 \uc73c\ub85c\ub9cc \ucc38\uc5ec\ud558\uace0 \uc810\uc218\ub294 \uae30\ub85d\ub418\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4.</p></body></html>", None))
        self.lb_id.setText(QCoreApplication.translate("user_reg", u"283_", None))
        self.lb_name.setText(QCoreApplication.translate("user_reg", u"\ud64d*\ub3d9", None))
        self.lb_chAnswer_2.setText(QCoreApplication.translate("user_reg", u"<html><head/><body><p>\uc870\ud68c\uacb0\uacfc:</p></body></html>", None))
        self.lb_grade.setText(QCoreApplication.translate("user_reg", u"2\ud559\ub144", None))
        self.lb_school.setText(QCoreApplication.translate("user_reg", u"\uace0\uc2e4\uc911\ud559\uad50", None))
        self.lb_quiz_name.setText(QCoreApplication.translate("user_reg", u"\ud034\uc988 \uc120\ud0dd", None))
        self.lb_imageView.setText("")
        self.label.setText(QCoreApplication.translate("user_reg", u"\uc0ac\uc6a9\uc790 \ub4f1\ub85d / \uc815\ubcf4\uc870\ud68c \ub3d9\uc758", None))
        self.lb_keytime.setText(QCoreApplication.translate("user_reg", u"\uc785\ub825\ub300\uae30:", None))
        self.lb_verInfo.setText(QCoreApplication.translate("user_reg", u"\ud504\ub85c\uadf8\ub7a8 v00  |  \ud034\uc988 v00  |  Program developer : 000", None))
    # retranslateUi

