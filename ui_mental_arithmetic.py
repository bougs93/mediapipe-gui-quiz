# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mental_arithmetic.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QProgressBar, QSizePolicy,
    QWidget)

class Ui_widget(object):
    def setupUi(self, widget):
        if not widget.objectName():
            widget.setObjectName(u"widget")
        widget.resize(1000, 1000)
        self.wg_mental = QWidget(widget)
        self.wg_mental.setObjectName(u"wg_mental")
        self.wg_mental.setGeometry(QRect(150, 180, 700, 560))
        self.lb_m_question = QLabel(self.wg_mental)
        self.lb_m_question.setObjectName(u"lb_m_question")
        self.lb_m_question.setGeometry(QRect(90, 90, 521, 271))
        font = QFont()
        font.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc ExtraBold"])
        font.setPointSize(35)
        font.setBold(True)
        self.lb_m_question.setFont(font)
        self.lb_m_question.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"border-radius: 15px;\n"
"color: rgb(255, 255, 255);")
        self.lb_m_question.setAlignment(Qt.AlignCenter)
        self.lb_m_frame = QLabel(self.wg_mental)
        self.lb_m_frame.setObjectName(u"lb_m_frame")
        self.lb_m_frame.setGeometry(QRect(80, 80, 541, 331))
        self.lb_m_frame.setStyleSheet(u"background-color: rgb(232, 232, 232);\n"
"border-radius: 20px;")
        self.lb_m_answer3 = QLabel(self.wg_mental)
        self.lb_m_answer3.setObjectName(u"lb_m_answer3")
        self.lb_m_answer3.setGeometry(QRect(460, 440, 210, 90))
        font1 = QFont()
        font1.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font1.setPointSize(35)
        self.lb_m_answer3.setFont(font1)
        self.lb_m_answer3.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"border-radius: 45px;\n"
"border: 8px solid rgb(232, 232, 232);\n"
"color: rgb(255, 255, 255);")
        self.lb_m_answer3.setScaledContents(False)
        self.lb_m_answer3.setAlignment(Qt.AlignCenter)
        self.lb_m_score = QLabel(self.wg_mental)
        self.lb_m_score.setObjectName(u"lb_m_score")
        self.lb_m_score.setGeometry(QRect(260, 40, 171, 90))
        font2 = QFont()
        font2.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc ExtraBold"])
        font2.setPointSize(40)
        font2.setBold(True)
        self.lb_m_score.setFont(font2)
        self.lb_m_score.setStyleSheet(u"background-color: rgb(232, 232, 232);\n"
"border-radius: 45px;")
        self.lb_m_score.setAlignment(Qt.AlignCenter)
        self.pb_m_progressBar = QProgressBar(self.wg_mental)
        self.pb_m_progressBar.setObjectName(u"pb_m_progressBar")
        self.pb_m_progressBar.setGeometry(QRect(90, 370, 521, 31))
        self.pb_m_progressBar.setValue(24)
        self.pb_m_progressBar.setTextVisible(False)
        self.lb_m_answer1 = QLabel(self.wg_mental)
        self.lb_m_answer1.setObjectName(u"lb_m_answer1")
        self.lb_m_answer1.setGeometry(QRect(20, 440, 210, 90))
        self.lb_m_answer1.setFont(font1)
        self.lb_m_answer1.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"border-radius: 45px;\n"
"border: 8px solid rgb(232, 232, 232);\n"
"color: rgb(255, 255, 255);")
        self.lb_m_answer1.setScaledContents(False)
        self.lb_m_answer1.setAlignment(Qt.AlignCenter)
        self.lb_m_answer2 = QLabel(self.wg_mental)
        self.lb_m_answer2.setObjectName(u"lb_m_answer2")
        self.lb_m_answer2.setGeometry(QRect(240, 440, 210, 90))
        self.lb_m_answer2.setFont(font1)
        self.lb_m_answer2.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"border-radius: 45px;\n"
"border: 8px solid rgb(232, 232, 232);\n"
"color: rgb(255, 255, 255);")
        self.lb_m_answer2.setScaledContents(False)
        self.lb_m_answer2.setAlignment(Qt.AlignCenter)
        self.lb_m_name = QLabel(self.wg_mental)
        self.lb_m_name.setObjectName(u"lb_m_name")
        self.lb_m_name.setGeometry(QRect(430, 90, 171, 51))
        font3 = QFont()
        font3.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc ExtraBold"])
        font3.setPointSize(28)
        font3.setBold(True)
        self.lb_m_name.setFont(font3)
        self.lb_m_name.setStyleSheet(u"background-color: rgba(232, 232, 232, 0);\n"
"color: rgb(26, 232, 57);")
        self.lb_m_name.setAlignment(Qt.AlignCenter)
        self.lb_m_id = QLabel(self.wg_mental)
        self.lb_m_id.setObjectName(u"lb_m_id")
        self.lb_m_id.setGeometry(QRect(90, 90, 161, 51))
        self.lb_m_id.setFont(font3)
        self.lb_m_id.setStyleSheet(u"background-color: rgba(232, 232, 232, 0);\n"
"color: rgb(26, 232, 57);")
        self.lb_m_id.setAlignment(Qt.AlignCenter)
        self.lb_m_waring = QLabel(self.wg_mental)
        self.lb_m_waring.setObjectName(u"lb_m_waring")
        self.lb_m_waring.setGeometry(QRect(110, 310, 481, 51))
        font4 = QFont()
        font4.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font4.setPointSize(27)
        self.lb_m_waring.setFont(font4)
        self.lb_m_waring.setStyleSheet(u"color: rgb(255, 255, 0);")
        self.lb_m_waring.setScaledContents(False)
        self.lb_m_waring.setAlignment(Qt.AlignCenter)
        self.lb_m_frame.raise_()
        self.lb_m_answer3.raise_()
        self.pb_m_progressBar.raise_()
        self.lb_m_answer1.raise_()
        self.lb_m_question.raise_()
        self.lb_m_answer2.raise_()
        self.lb_m_score.raise_()
        self.lb_m_name.raise_()
        self.lb_m_id.raise_()
        self.lb_m_waring.raise_()
        self.lb_m_end_score = QLabel(widget)
        self.lb_m_end_score.setObjectName(u"lb_m_end_score")
        self.lb_m_end_score.setGeometry(QRect(400, 440, 200, 200))
        font5 = QFont()
        font5.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc ExtraBold"])
        font5.setPointSize(50)
        font5.setBold(True)
        self.lb_m_end_score.setFont(font5)
        self.lb_m_end_score.setStyleSheet(u"background-color: rgb(232, 232, 232);\n"
"border-radius: 100px;")
        self.lb_m_end_score.setAlignment(Qt.AlignCenter)

        self.retranslateUi(widget)

        QMetaObject.connectSlotsByName(widget)
    # setupUi

    def retranslateUi(self, widget):
        widget.setWindowTitle(QCoreApplication.translate("widget", u"Form", None))
        self.lb_m_question.setText(QCoreApplication.translate("widget", u"9999", None))
        self.lb_m_frame.setText("")
        self.lb_m_answer3.setText(QCoreApplication.translate("widget", u"9999", None))
        self.lb_m_score.setText(QCoreApplication.translate("widget", u"9999", None))
        self.lb_m_answer1.setText(QCoreApplication.translate("widget", u"9999", None))
        self.lb_m_answer2.setText(QCoreApplication.translate("widget", u"9999", None))
        self.lb_m_name.setText(QCoreApplication.translate("widget", u"\ud64d*\ub3d9", None))
        self.lb_m_id.setText(QCoreApplication.translate("widget", u"22**", None))
        self.lb_m_waring.setText(QCoreApplication.translate("widget", u"\u21d0 \ud654\uba74 \uc911\uc559\uc73c\ub85c \uc774\ub3d9\ud558\uc138\uc694 \u21d2", None))
        self.lb_m_end_score.setText(QCoreApplication.translate("widget", u"9999", None))
    # retranslateUi

