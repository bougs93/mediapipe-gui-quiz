# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_quiz_end.ui'
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

class Ui_quizEndView(object):
    def setupUi(self, quizEndView):
        if not quizEndView.objectName():
            quizEndView.setObjectName(u"quizEndView")
        quizEndView.resize(1280, 1024)
        self.fr_top_quiz = QFrame(quizEndView)
        self.fr_top_quiz.setObjectName(u"fr_top_quiz")
        self.fr_top_quiz.setEnabled(True)
        self.fr_top_quiz.setGeometry(QRect(10, 10, 1261, 91))
        self.fr_top_quiz.setStyleSheet(u"background-color:rgb(142, 198, 63);\n"
"border-radius: 10px;")
        self.fr_top_quiz.setFrameShape(QFrame.StyledPanel)
        self.fr_top_quiz.setFrameShadow(QFrame.Raised)
        self.lb_type2 = QLabel(self.fr_top_quiz)
        self.lb_type2.setObjectName(u"lb_type2")
        self.lb_type2.setGeometry(QRect(160, 20, 391, 61))
        font = QFont()
        font.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font.setPointSize(30)
        self.lb_type2.setFont(font)
        self.lb_type2.setAlignment(Qt.AlignCenter)
        self.lb_quizTime = QLabel(self.fr_top_quiz)
        self.lb_quizTime.setObjectName(u"lb_quizTime")
        self.lb_quizTime.setGeometry(QRect(960, 10, 271, 71))
        font1 = QFont()
        font1.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font1.setPointSize(25)
        self.lb_quizTime.setFont(font1)
        self.lb_quizTime.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lb_fps = QLabel(quizEndView)
        self.lb_fps.setObjectName(u"lb_fps")
        self.lb_fps.setGeometry(QRect(1140, 1000, 141, 21))
        font2 = QFont()
        font2.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font2.setPointSize(11)
        self.lb_fps.setFont(font2)
        self.lb_fps.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgba(255, 255, 255, 150);")
        self.lb_fps.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.fr_main_quiz = QFrame(quizEndView)
        self.fr_main_quiz.setObjectName(u"fr_main_quiz")
        self.fr_main_quiz.setGeometry(QRect(10, 120, 1251, 901))
        self.fr_main_quiz.setStyleSheet(u"")
        self.fr_main_quiz.setFrameShape(QFrame.StyledPanel)
        self.fr_main_quiz.setFrameShadow(QFrame.Raised)
        self.lb_countDown = QLabel(self.fr_main_quiz)
        self.lb_countDown.setObjectName(u"lb_countDown")
        self.lb_countDown.setGeometry(QRect(595, 450, 100, 61))
        self.lb_countDown.setMinimumSize(QSize(100, 0))
        font3 = QFont()
        font3.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font3.setPointSize(35)
        self.lb_countDown.setFont(font3)
        self.lb_countDown.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lb_countDown.setAlignment(Qt.AlignCenter)
        self.lb_imageView = QLabel(quizEndView)
        self.lb_imageView.setObjectName(u"lb_imageView")
        self.lb_imageView.setGeometry(QRect(10, 110, 1261, 901))
        font4 = QFont()
        font4.setPointSize(28)
        self.lb_imageView.setFont(font4)
        self.lb_imageView.setStyleSheet(u"background-color: rgb(188, 188, 188);\n"
"border-radius: 30px;")
        self.lb_imageView.setAlignment(Qt.AlignCenter)
        self.lb_no = QLabel(quizEndView)
        self.lb_no.setObjectName(u"lb_no")
        self.lb_no.setGeometry(QRect(30, 20, 201, 71))
        self.lb_no.setFont(font1)
        self.center_progress = QFrame(quizEndView)
        self.center_progress.setObjectName(u"center_progress")
        self.center_progress.setGeometry(QRect(490, 330, 350, 350))
        self.center_progress.setFrameShape(QFrame.StyledPanel)
        self.center_progress.setFrameShadow(QFrame.Raised)
        self.lb_verInfo = QLabel(quizEndView)
        self.lb_verInfo.setObjectName(u"lb_verInfo")
        self.lb_verInfo.setGeometry(QRect(10, 1000, 600, 21))
        self.lb_verInfo.setFont(font2)
        self.lb_verInfo.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgba(255, 255, 255, 150);")
        self.lb_verInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_quizArea = QLabel(quizEndView)
        self.lb_quizArea.setObjectName(u"lb_quizArea")
        self.lb_quizArea.setGeometry(QRect(550, 20, 411, 71))
        self.lb_quizArea.setMinimumSize(QSize(100, 0))
        font5 = QFont()
        font5.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font5.setPointSize(26)
        font5.setBold(True)
        self.lb_quizArea.setFont(font5)
        self.lb_quizArea.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(188, 1, 108);\n"
"border-radius: 35px;")
        self.lb_quizArea.setAlignment(Qt.AlignCenter)
        self.fr_ranking = QFrame(quizEndView)
        self.fr_ranking.setObjectName(u"fr_ranking")
        self.fr_ranking.setGeometry(QRect(830, 170, 451, 701))
        self.fr_ranking.setStyleSheet(u"background-color: rgb(170, 170, 255);")
        self.fr_ranking.setFrameShape(QFrame.StyledPanel)
        self.fr_ranking.setFrameShadow(QFrame.Raised)
        self.fr_info = QFrame(quizEndView)
        self.fr_info.setObjectName(u"fr_info")
        self.fr_info.setGeometry(QRect(0, 170, 741, 301))
        self.fr_info.setStyleSheet(u"background-color: rgba(43, 43, 43, 180);")
        self.fr_info.setFrameShape(QFrame.StyledPanel)
        self.fr_info.setFrameShadow(QFrame.Raised)
        self.lb_score = QLabel(self.fr_info)
        self.lb_score.setObjectName(u"lb_score")
        self.lb_score.setGeometry(QRect(510, 40, 211, 171))
        self.lb_score.setMinimumSize(QSize(110, 0))
        font6 = QFont()
        font6.setFamilies([u"NanumSquareRound"])
        font6.setPointSize(50)
        font6.setBold(True)
        self.lb_score.setFont(font6)
        self.lb_score.setAutoFillBackground(False)
        self.lb_score.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.lb_score.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lb_score.setWordWrap(True)
        self.lb_info = QLabel(self.fr_info)
        self.lb_info.setObjectName(u"lb_info")
        self.lb_info.setGeometry(QRect(20, 30, 491, 191))
        self.lb_info.setMinimumSize(QSize(110, 0))
        font7 = QFont()
        font7.setFamilies([u"NanumSquareRound"])
        font7.setPointSize(24)
        font7.setBold(True)
        self.lb_info.setFont(font7)
        self.lb_info.setAutoFillBackground(False)
        self.lb_info.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.lb_info.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lb_info.setWordWrap(True)
        self.lb_info2 = QLabel(self.fr_info)
        self.lb_info2.setObjectName(u"lb_info2")
        self.lb_info2.setGeometry(QRect(40, 210, 661, 71))
        self.lb_info2.setMinimumSize(QSize(110, 0))
        font8 = QFont()
        font8.setFamilies([u"NanumSquareRound"])
        font8.setPointSize(19)
        font8.setBold(True)
        self.lb_info2.setFont(font8)
        self.lb_info2.setAutoFillBackground(False)
        self.lb_info2.setStyleSheet(u"color: rgb(255, 255, 0);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.lb_info2.setAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)
        self.lb_info2.setWordWrap(True)
        self.lb_imageView.raise_()
        self.fr_top_quiz.raise_()
        self.lb_fps.raise_()
        self.fr_main_quiz.raise_()
        self.lb_no.raise_()
        self.center_progress.raise_()
        self.lb_verInfo.raise_()
        self.lb_quizArea.raise_()
        self.fr_ranking.raise_()
        self.fr_info.raise_()

        self.retranslateUi(quizEndView)

        QMetaObject.connectSlotsByName(quizEndView)
    # setupUi

    def retranslateUi(self, quizEndView):
        quizEndView.setWindowTitle(QCoreApplication.translate("quizEndView", u"Form", None))
        self.lb_type2.setText(QCoreApplication.translate("quizEndView", u"--- \ud034\uc988 \uacb0\uacfc", None))
        self.lb_quizTime.setText(QCoreApplication.translate("quizEndView", u"\uc81c\ud55c\uc2dc\uac04 02:30", None))
        self.lb_fps.setText(QCoreApplication.translate("quizEndView", u"FPS", None))
        self.lb_countDown.setText(QCoreApplication.translate("quizEndView", u"0", None))
        self.lb_imageView.setText("")
        self.lb_no.setText(QCoreApplication.translate("quizEndView", u"\ubb38\uc81c: 10", None))
        self.lb_verInfo.setText(QCoreApplication.translate("quizEndView", u"\ud504\ub85c\uadf8\ub7a8 v00  |  \ud034\uc988 v00  |  Program developer : 000", None))
        self.lb_quizArea.setText(QCoreApplication.translate("quizEndView", u"-", None))
        self.lb_score.setText(QCoreApplication.translate("quizEndView", u"<p>100\uc810 </p>\n"
"<p>100\uc704 </p>", None))
        self.lb_info.setText(QCoreApplication.translate("quizEndView", u"<style type=text/css>\n"
"p.line1 {\n"
"    color: rgb(142, 198, 63);\n"
"    font-weight: bold;\n"
"    font-size: 40px;\n"
"}\n"
"</style>\n"
"\n"
"<p class=\"line1\">\ub3c4\uc804\uc790: 0203 \ud64d\uae38\ub3d9</p>\n"
"<p>\ubb38\uc81c:00 \uc815\ub2f5:00 \uc624\ub2f5:00 \ud1b5\uacfc:00</p>\n"
"<p>2023.05.14 AM 11:23</p>", None))
        self.lb_info2.setText(QCoreApplication.translate("quizEndView", u"0203 \ud64d\uae38\ub3d9 \ub2d8\uc758 \uc774\uc804 \ucd5c\uace0 \uae30\ub85d\uc740 00\uc704 00\uc810 00\ubb38\uc81c \uc785\ub2c8\ub2e4.", None))
    # retranslateUi

