# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_quiz.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem, QWidget)

class Ui_quizView(object):
    def setupUi(self, quizView):
        if not quizView.objectName():
            quizView.setObjectName(u"quizView")
        quizView.resize(1280, 1024)
        self.fr_top_quiz = QFrame(quizView)
        self.fr_top_quiz.setObjectName(u"fr_top_quiz")
        self.fr_top_quiz.setEnabled(True)
        self.fr_top_quiz.setGeometry(QRect(10, 10, 1261, 91))
        self.fr_top_quiz.setStyleSheet(u"background-color: #E65100;\n"
"border-radius: 10px;")
        self.fr_top_quiz.setFrameShape(QFrame.StyledPanel)
        self.fr_top_quiz.setFrameShadow(QFrame.Raised)
        self.lb_code = QLabel(self.fr_top_quiz)
        self.lb_code.setObjectName(u"lb_code")
        self.lb_code.setGeometry(QRect(1050, 10, 181, 31))
        font = QFont()
        font.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font.setPointSize(20)
        self.lb_code.setFont(font)
        self.lb_code.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.gridLayoutWidget = QWidget(self.fr_top_quiz)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 38, 1241, 46))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lb_usrTitle = QLabel(self.gridLayoutWidget)
        self.lb_usrTitle.setObjectName(u"lb_usrTitle")
        self.lb_usrTitle.setMinimumSize(QSize(110, 0))
        font1 = QFont()
        font1.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font1.setPointSize(24)
        self.lb_usrTitle.setFont(font1)
        self.lb_usrTitle.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lb_usrTitle.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.lb_usrTitle)

        self.lb_usrName = QLabel(self.gridLayoutWidget)
        self.lb_usrName.setObjectName(u"lb_usrName")
        self.lb_usrName.setMinimumSize(QSize(200, 0))
        self.lb_usrName.setFont(font1)
        self.lb_usrName.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lb_usrName.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.lb_usrName)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lb_timeTitle = QLabel(self.gridLayoutWidget)
        self.lb_timeTitle.setObjectName(u"lb_timeTitle")
        self.lb_timeTitle.setMinimumSize(QSize(120, 0))
        self.lb_timeTitle.setFont(font1)
        self.lb_timeTitle.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lb_timeTitle.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.lb_timeTitle)

        self.lb_timeView = QLabel(self.gridLayoutWidget)
        self.lb_timeView.setObjectName(u"lb_timeView")
        self.lb_timeView.setMinimumSize(QSize(100, 0))
        self.lb_timeView.setFont(font1)
        self.lb_timeView.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lb_timeView.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.lb_timeView)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lb_correctTitle = QLabel(self.gridLayoutWidget)
        self.lb_correctTitle.setObjectName(u"lb_correctTitle")
        self.lb_correctTitle.setMinimumSize(QSize(70, 0))
        self.lb_correctTitle.setFont(font1)
        self.lb_correctTitle.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lb_correctTitle.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.lb_correctTitle)

        self.lb_correct = QLabel(self.gridLayoutWidget)
        self.lb_correct.setObjectName(u"lb_correct")
        self.lb_correct.setMinimumSize(QSize(60, 0))
        self.lb_correct.setFont(font1)
        self.lb_correct.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lb_correct.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.lb_correct)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lb_wrongpassTitle = QLabel(self.gridLayoutWidget)
        self.lb_wrongpassTitle.setObjectName(u"lb_wrongpassTitle")
        self.lb_wrongpassTitle.setMinimumSize(QSize(70, 0))
        self.lb_wrongpassTitle.setFont(font1)
        self.lb_wrongpassTitle.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lb_wrongpassTitle.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.lb_wrongpassTitle)

        self.lb_wrongpass = QLabel(self.gridLayoutWidget)
        self.lb_wrongpass.setObjectName(u"lb_wrongpass")
        self.lb_wrongpass.setMinimumSize(QSize(60, 0))
        font2 = QFont()
        font2.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font2.setPointSize(24)
        font2.setBold(True)
        self.lb_wrongpass.setFont(font2)
        self.lb_wrongpass.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lb_wrongpass.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.lb_wrongpass)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.lb_scoreTitle = QLabel(self.gridLayoutWidget)
        self.lb_scoreTitle.setObjectName(u"lb_scoreTitle")
        self.lb_scoreTitle.setMinimumSize(QSize(80, 0))
        self.lb_scoreTitle.setFont(font1)
        self.lb_scoreTitle.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lb_scoreTitle.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.lb_scoreTitle)

        self.lb_score = QLabel(self.gridLayoutWidget)
        self.lb_score.setObjectName(u"lb_score")
        self.lb_score.setMinimumSize(QSize(60, 0))
        self.lb_score.setFont(font1)
        self.lb_score.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lb_score.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.lb_score)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_4)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.lb_fps = QLabel(quizView)
        self.lb_fps.setObjectName(u"lb_fps")
        self.lb_fps.setGeometry(QRect(1140, 1000, 131, 21))
        font3 = QFont()
        font3.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font3.setPointSize(11)
        self.lb_fps.setFont(font3)
        self.lb_fps.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgba(255, 255, 255, 150);")
        self.lb_fps.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.fr_main_quiz = QFrame(quizView)
        self.fr_main_quiz.setObjectName(u"fr_main_quiz")
        self.fr_main_quiz.setGeometry(QRect(10, 120, 1251, 901))
        self.fr_main_quiz.setFrameShape(QFrame.StyledPanel)
        self.fr_main_quiz.setFrameShadow(QFrame.Raised)
        self.lb_chAnswer = QLabel(self.fr_main_quiz)
        self.lb_chAnswer.setObjectName(u"lb_chAnswer")
        self.lb_chAnswer.setGeometry(QRect(10, 490, 1241, 391))
        self.lb_chAnswer.setMinimumSize(QSize(110, 0))
        font4 = QFont()
        font4.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font4.setPointSize(25)
        font4.setBold(True)
        font4.setItalic(False)
        font4.setUnderline(False)
        font4.setStrikeOut(False)
        font4.setKerning(True)
        self.lb_chAnswer.setFont(font4)
        self.lb_chAnswer.setStyleSheet(u"background-color: rgba(255, 255, 255, 60);\n"
"border-radius: 30px;")
        self.lb_chAnswer.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_chAnswer.setWordWrap(True)
        self.lb_question2 = QLabel(self.fr_main_quiz)
        self.lb_question2.setObjectName(u"lb_question2")
        self.lb_question2.setGeometry(QRect(10, 0, 721, 331))
        self.lb_question2.setMinimumSize(QSize(110, 0))
        font5 = QFont()
        font5.setFamilies([u"NanumSquareRound"])
        font5.setPointSize(28)
        font5.setBold(True)
        self.lb_question2.setFont(font5)
        self.lb_question2.setAutoFillBackground(False)
        self.lb_question2.setStyleSheet(u"background-color: rgba(209, 196, 233, 120);\n"
"border-radius: 30px;")
        self.lb_question2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_question2.setWordWrap(True)
        self.lb_question2Img = QLabel(self.fr_main_quiz)
        self.lb_question2Img.setObjectName(u"lb_question2Img")
        self.lb_question2Img.setGeometry(QRect(740, 0, 511, 331))
        self.lb_question2Img.setMinimumSize(QSize(110, 0))
        self.lb_question2Img.setFont(font5)
        self.lb_question2Img.setAutoFillBackground(False)
        self.lb_question2Img.setStyleSheet(u"background-color: rgba(209, 196, 233, 120);\n"
"border-radius: 0px;")
        self.lb_question2Img.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_question2Img.setWordWrap(True)
        self.lb_question = QLabel(self.fr_main_quiz)
        self.lb_question.setObjectName(u"lb_question")
        self.lb_question.setGeometry(QRect(10, 0, 1241, 331))
        self.lb_question.setMinimumSize(QSize(110, 0))
        self.lb_question.setFont(font5)
        self.lb_question.setAutoFillBackground(False)
        self.lb_question.setStyleSheet(u"background-color: rgba(255, 224, 178, 120);\n"
"border-radius: 30px;")
        self.lb_question.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_question.setWordWrap(True)
        self.lb_waitMsg = QLabel(self.fr_main_quiz)
        self.lb_waitMsg.setObjectName(u"lb_waitMsg")
        self.lb_waitMsg.setGeometry(QRect(230, 340, 821, 141))
        self.lb_waitMsg.setMinimumSize(QSize(110, 0))
        self.lb_waitMsg.setFont(font5)
        self.lb_waitMsg.setAutoFillBackground(False)
        self.lb_waitMsg.setStyleSheet(u"background-color: rgba(255, 255, 255, 200);\n"
"border-radius: 30px;")
        self.lb_waitMsg.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_waitMsg.setWordWrap(True)
        self.lb_inputModeImg = QLabel(self.fr_main_quiz)
        self.lb_inputModeImg.setObjectName(u"lb_inputModeImg")
        self.lb_inputModeImg.setGeometry(QRect(40, 330, 1121, 161))
        font6 = QFont()
        font6.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font6.setPointSize(10)
        font6.setBold(True)
        self.lb_inputModeImg.setFont(font6)
        self.lb_inputModeImg.setStyleSheet(u"")
        self.lb_imageView = QLabel(quizView)
        self.lb_imageView.setObjectName(u"lb_imageView")
        self.lb_imageView.setGeometry(QRect(10, 110, 1261, 901))
        font7 = QFont()
        font7.setPointSize(28)
        self.lb_imageView.setFont(font7)
        self.lb_imageView.setStyleSheet(u"background-color: rgb(188, 188, 188);\n"
"border-radius: 30px;")
        self.lb_imageView.setAlignment(Qt.AlignCenter)
        self.lb_type = QLabel(quizView)
        self.lb_type.setObjectName(u"lb_type")
        self.lb_type.setGeometry(QRect(270, 20, 371, 31))
        self.lb_type.setFont(font)
        self.lb_no = QLabel(quizView)
        self.lb_no.setObjectName(u"lb_no")
        self.lb_no.setGeometry(QRect(80, 20, 151, 31))
        self.lb_no.setFont(font)
        self.lb_quizResult = QLabel(quizView)
        self.lb_quizResult.setObjectName(u"lb_quizResult")
        self.lb_quizResult.setGeometry(QRect(260, 330, 791, 381))
        font8 = QFont()
        font8.setFamilies([u"Atlanta"])
        font8.setPointSize(200)
        font8.setBold(True)
        font8.setItalic(False)
        self.lb_quizResult.setFont(font8)
        self.lb_quizResult.setStyleSheet(u"")
        self.lb_quizResult.setAlignment(Qt.AlignCenter)
        self.lb_type2 = QLabel(quizView)
        self.lb_type2.setObjectName(u"lb_type2")
        self.lb_type2.setGeometry(QRect(680, 20, 281, 31))
        self.lb_type2.setFont(font)
        self.center_progress = QFrame(quizView)
        self.center_progress.setObjectName(u"center_progress")
        self.center_progress.setGeometry(QRect(490, 330, 350, 350))
        self.center_progress.setFrameShape(QFrame.StyledPanel)
        self.center_progress.setFrameShadow(QFrame.Raised)
        self.lb_verInfo = QLabel(quizView)
        self.lb_verInfo.setObjectName(u"lb_verInfo")
        self.lb_verInfo.setGeometry(QRect(10, 1000, 600, 21))
        self.lb_verInfo.setFont(font3)
        self.lb_verInfo.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgba(255, 255, 255, 150);")
        self.lb_verInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_test_hint = QLabel(quizView)
        self.lb_test_hint.setObjectName(u"lb_test_hint")
        self.lb_test_hint.setGeometry(QRect(620, 1000, 81, 21))
        self.lb_test_hint.setFont(font3)
        self.lb_test_hint.setLayoutDirection(Qt.LeftToRight)
        self.lb_test_hint.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgba(255, 255, 255, 150);")
        self.lb_test_hint.setAlignment(Qt.AlignCenter)
        self.lb_mode_img = QLabel(quizView)
        self.lb_mode_img.setObjectName(u"lb_mode_img")
        self.lb_mode_img.setGeometry(QRect(20, 8, 45, 45))
        self.lb_mode_img.setAlignment(Qt.AlignCenter)
        self.lb_imageView.raise_()
        self.fr_top_quiz.raise_()
        self.lb_fps.raise_()
        self.fr_main_quiz.raise_()
        self.lb_type.raise_()
        self.lb_no.raise_()
        self.lb_quizResult.raise_()
        self.lb_type2.raise_()
        self.center_progress.raise_()
        self.lb_verInfo.raise_()
        self.lb_test_hint.raise_()
        self.lb_mode_img.raise_()

        self.retranslateUi(quizView)

        QMetaObject.connectSlotsByName(quizView)
    # setupUi

    def retranslateUi(self, quizView):
        quizView.setWindowTitle(QCoreApplication.translate("quizView", u"Form", None))
        self.lb_code.setText(QCoreApplication.translate("quizView", u"CODE:", None))
        self.lb_usrTitle.setText(QCoreApplication.translate("quizView", u"\ub3c4\uc804\uc790", None))
        self.lb_usrName.setText(QCoreApplication.translate("quizView", u"02928\ud64d\uae38\ub3d9", None))
        self.lb_timeTitle.setText(QCoreApplication.translate("quizView", u"\ub0a8\uc740\uc2dc\uac04", None))
        self.lb_timeView.setText(QCoreApplication.translate("quizView", u"03:00", None))
        self.lb_correctTitle.setText(QCoreApplication.translate("quizView", u"\uc815\ub2f5:", None))
        self.lb_correct.setText(QCoreApplication.translate("quizView", u"0", None))
        self.lb_wrongpassTitle.setText(QCoreApplication.translate("quizView", u"\uc624\ub2f5/PASS:", None))
        self.lb_wrongpass.setText(QCoreApplication.translate("quizView", u"0/0", None))
        self.lb_scoreTitle.setText(QCoreApplication.translate("quizView", u"\uc810\uc218:", None))
        self.lb_score.setText(QCoreApplication.translate("quizView", u"0", None))
        self.lb_fps.setText(QCoreApplication.translate("quizView", u"FPS", None))
        self.lb_chAnswer.setText(QCoreApplication.translate("quizView", u"<style type=text/\n"
"\n"
"css>\n"
"p.margin {\n"
"    margin-top: 15px;\n"
"    margin-bottom: 15px;\n"
"    margin-right: 30px;\n"
"    margin-left: 30px;\n"
"    line-height: 110%;\n"
"}\n"
"</style>\n"
"\n"
"<p class=\"margin\">1) \ub2f5\uc548 </p>\n"
"<p class=\"margin\">2) \ub2f5\uc548 </p>\n"
"<p class=\"margin\">3) \ub2f5\uc548 </p>\n"
"<p class=\"margin\">4) \ub2f5\uc548 </p>\n"
"<p class=\"margin\">5) \ub2f5\uc548 </p>\n"
"\n"
" \n"
"\n"
"", None))
        self.lb_question2.setText(QCoreApplication.translate("quizView", u"<style type=text/\n"
"\n"
"css>\n"
"p.margin {\n"
"    margin-top: 30px;\n"
"    margin-bottom: 30px;\n"
"    margin-right: 30px;\n"
"    margin-left: 30px;\n"
"    line-height: 110%;\n"
"}\n"
"</style>\n"
"\n"
"<p class=\"margin\"> \ubb38\uc81c \ud14c\uc2a4\ud2b8 ? </p>", None))
        self.lb_question2Img.setText(QCoreApplication.translate("quizView", u"<html><head/><body><p><br/></p></body></html>", None))
        self.lb_question.setText(QCoreApplication.translate("quizView", u"<style type=text/\n"
"\n"
"css>\n"
"p.margin {\n"
"    margin-top: 30px;\n"
"    margin-bottom: 30px;\n"
"    margin-right: 30px;\n"
"    margin-left: 30px;\n"
"    line-height: 110%;\n"
"}\n"
"</style>\n"
"\n"
"<p class=\"margin\"> \ubb38\uc81c \ud14c\uc2a4\ud2b8 </p>", None))
        self.lb_waitMsg.setText("")
        self.lb_inputModeImg.setText(QCoreApplication.translate("quizView", u"lb_imputModeImg", None))
        self.lb_imageView.setText("")
        self.lb_type.setText(QCoreApplication.translate("quizView", u"\uc601\uc5ed: \uc720\ud034\uc988 \ubb38\uc81c", None))
        self.lb_no.setText(QCoreApplication.translate("quizView", u"\ubb38\uc81c: 10", None))
        self.lb_quizResult.setText("")
        self.lb_type2.setText(QCoreApplication.translate("quizView", u"\ud034\uc988\uc720\ud615: \uc2a4\ud53c\ub4dc \ud034\uc988", None))
        self.lb_verInfo.setText(QCoreApplication.translate("quizView", u"\ud504\ub85c\uadf8\ub7a8 v00  |  \ud034\uc988 v00  |  Program developer : 000", None))
        self.lb_test_hint.setText("")
        self.lb_mode_img.setText(QCoreApplication.translate("quizView", u"mode_img", None))
    # retranslateUi

