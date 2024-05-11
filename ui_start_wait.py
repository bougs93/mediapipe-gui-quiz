# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_start_wait.ui'
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

class Ui_startWait(object):
    def setupUi(self, startWait):
        if not startWait.objectName():
            startWait.setObjectName(u"startWait")
        startWait.resize(1280, 1026)
        self.lb_imageView = QLabel(startWait)
        self.lb_imageView.setObjectName(u"lb_imageView")
        self.lb_imageView.setGeometry(QRect(10, 110, 1261, 901))
        font = QFont()
        font.setPointSize(28)
        self.lb_imageView.setFont(font)
        self.lb_imageView.setStyleSheet(u"background-color: rgb(188, 188, 188);\n"
"border-radius: 30px;")
        self.lb_imageView.setAlignment(Qt.AlignCenter)
        self.lb_chAnswer = QLabel(startWait)
        self.lb_chAnswer.setObjectName(u"lb_chAnswer")
        self.lb_chAnswer.setGeometry(QRect(20, 790, 1241, 211))
        self.lb_chAnswer.setMinimumSize(QSize(110, 0))
        font1 = QFont()
        font1.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font1.setPointSize(19)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.lb_chAnswer.setFont(font1)
        self.lb_chAnswer.setStyleSheet(u"background-color: rgba(187, 222, 251,150);\n"
"border-radius: 30px;")
        self.lb_chAnswer.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_chAnswer.setWordWrap(True)
        self.fr_top = QFrame(startWait)
        self.fr_top.setObjectName(u"fr_top")
        self.fr_top.setGeometry(QRect(10, 10, 1261, 91))
        self.fr_top.setStyleSheet(u"background-color: rgb(209, 196, 233);\n"
"border-radius: 10px;")
        self.fr_top.setFrameShape(QFrame.StyledPanel)
        self.fr_top.setFrameShadow(QFrame.Raised)
        self.lb_fps = QLabel(startWait)
        self.lb_fps.setObjectName(u"lb_fps")
        self.lb_fps.setGeometry(QRect(1140, 1000, 131, 21))
        font2 = QFont()
        font2.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font2.setPointSize(11)
        self.lb_fps.setFont(font2)
        self.lb_fps.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgba(255, 255, 255, 150);")
        self.lb_fps.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.center_progress = QFrame(startWait)
        self.center_progress.setObjectName(u"center_progress")
        self.center_progress.setGeometry(QRect(490, 330, 350, 350))
        self.center_progress.setFrameShape(QFrame.StyledPanel)
        self.center_progress.setFrameShadow(QFrame.Raised)
        self.lb_challenge = QLabel(startWait)
        self.lb_challenge.setObjectName(u"lb_challenge")
        self.lb_challenge.setGeometry(QRect(390, 610, 461, 81))
        font3 = QFont()
        font3.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc ExtraBold"])
        font3.setPointSize(30)
        self.lb_challenge.setFont(font3)
        self.lb_challenge.setStyleSheet(u"background-color: rgb(63, 81, 181);\n"
"border-radius: 40px;\n"
"color: rgb(255, 255, 255);")
        self.lb_challenge.setAlignment(Qt.AlignCenter)
        self.lb_type2 = QLabel(startWait)
        self.lb_type2.setObjectName(u"lb_type2")
        self.lb_type2.setGeometry(QRect(150, 40, 211, 31))
        font4 = QFont()
        font4.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font4.setPointSize(23)
        self.lb_type2.setFont(font4)
        self.lb_face_icon = QLabel(startWait)
        self.lb_face_icon.setObjectName(u"lb_face_icon")
        self.lb_face_icon.setGeometry(QRect(1140, 860, 100, 100))
        self.lb_face_icon.setAlignment(Qt.AlignCenter)
        self.lb_verInfo = QLabel(startWait)
        self.lb_verInfo.setObjectName(u"lb_verInfo")
        self.lb_verInfo.setGeometry(QRect(10, 1000, 600, 21))
        self.lb_verInfo.setFont(font2)
        self.lb_verInfo.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgba(255, 255, 255, 150);")
        self.lb_verInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_hand_icon = QLabel(startWait)
        self.lb_hand_icon.setObjectName(u"lb_hand_icon")
        self.lb_hand_icon.setGeometry(QRect(630, 550, 75, 75))
        self.lb_hand_icon.setAlignment(Qt.AlignCenter)
        self.lb_cmdMsg = QLabel(startWait)
        self.lb_cmdMsg.setObjectName(u"lb_cmdMsg")
        self.lb_cmdMsg.setGeometry(QRect(730, 1000, 401, 21))
        self.lb_cmdMsg.setFont(font2)
        self.lb_cmdMsg.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgba(255, 255, 255, 150);")
        self.lb_cmdMsg.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_visitorTotalCount = QLabel(startWait)
        self.lb_visitorTotalCount.setObjectName(u"lb_visitorTotalCount")
        self.lb_visitorTotalCount.setGeometry(QRect(370, 20, 221, 41))
        font5 = QFont()
        font5.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font5.setPointSize(15)
        self.lb_visitorTotalCount.setFont(font5)
        self.lb_visitorTotalCount.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_visitorCount = QLabel(startWait)
        self.lb_visitorCount.setObjectName(u"lb_visitorCount")
        self.lb_visitorCount.setGeometry(QRect(370, 60, 221, 31))
        self.lb_visitorCount.setFont(font5)
        self.lb_visitorCount.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_title_img = QLabel(startWait)
        self.lb_title_img.setObjectName(u"lb_title_img")
        self.lb_title_img.setGeometry(QRect(20, 100, 571, 291))
        self.lb_quizArea = QLabel(startWait)
        self.lb_quizArea.setObjectName(u"lb_quizArea")
        self.lb_quizArea.setGeometry(QRect(570, 20, 411, 71))
        self.lb_quizArea.setMinimumSize(QSize(100, 0))
        font6 = QFont()
        font6.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font6.setPointSize(26)
        font6.setBold(True)
        self.lb_quizArea.setFont(font6)
        self.lb_quizArea.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(188, 1, 108);\n"
"border-radius: 20px;")
        self.lb_quizArea.setAlignment(Qt.AlignCenter)
        self.lb_quizTime = QLabel(startWait)
        self.lb_quizTime.setObjectName(u"lb_quizTime")
        self.lb_quizTime.setGeometry(QRect(960, 20, 271, 71))
        font7 = QFont()
        font7.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font7.setPointSize(25)
        self.lb_quizTime.setFont(font7)
        self.lb_quizTime.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.fr_ranking = QFrame(startWait)
        self.fr_ranking.setObjectName(u"fr_ranking")
        self.fr_ranking.setGeometry(QRect(840, 90, 451, 701))
        self.fr_ranking.setStyleSheet(u"background-color: rgb(170, 170, 255);")
        self.fr_ranking.setFrameShape(QFrame.StyledPanel)
        self.fr_ranking.setFrameShadow(QFrame.Raised)
        self.lb_chAnswer_2 = QLabel(startWait)
        self.lb_chAnswer_2.setObjectName(u"lb_chAnswer_2")
        self.lb_chAnswer_2.setGeometry(QRect(20, 790, 1241, 211))
        self.lb_chAnswer_2.setMinimumSize(QSize(110, 0))
        self.lb_chAnswer_2.setFont(font1)
        self.lb_chAnswer_2.setStyleSheet(u"background-color: rgba(187, 222, 251,150);\n"
"border-radius: 30px;")
        self.lb_chAnswer_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_chAnswer_2.setWordWrap(True)
        self.lb_mode_img = QLabel(startWait)
        self.lb_mode_img.setObjectName(u"lb_mode_img")
        self.lb_mode_img.setGeometry(QRect(13, 15, 80, 80))
        self.lb_mode_img.setAlignment(Qt.AlignCenter)
        self.fr_top.raise_()
        self.lb_imageView.raise_()
        self.lb_chAnswer.raise_()
        self.lb_fps.raise_()
        self.lb_challenge.raise_()
        self.lb_type2.raise_()
        self.lb_face_icon.raise_()
        self.lb_verInfo.raise_()
        self.center_progress.raise_()
        self.lb_cmdMsg.raise_()
        self.lb_visitorTotalCount.raise_()
        self.lb_visitorCount.raise_()
        self.lb_hand_icon.raise_()
        self.lb_title_img.raise_()
        self.lb_quizArea.raise_()
        self.lb_quizTime.raise_()
        self.fr_ranking.raise_()
        self.lb_chAnswer_2.raise_()
        self.lb_mode_img.raise_()

        self.retranslateUi(startWait)

        QMetaObject.connectSlotsByName(startWait)
    # setupUi

    def retranslateUi(self, startWait):
        startWait.setWindowTitle(QCoreApplication.translate("startWait", u"Form", None))
        self.lb_imageView.setText("")
        self.lb_chAnswer.setText(QCoreApplication.translate("startWait", u"<html><head/><body><p>- \uac1c\uc778\uc815\ubcf4 \ub3d9\uc758 \uc5c6\uc774 \uc190\ub2d8\uc73c\ub85c \ucc38\uc5ec \uac00\ub2a5\ud569\ub2c8\ub2e4. </p><p>- \uc601\uc0c1\ucc98\ub9ac(OpenCV), \uc778\uacf5\uc9c0\ub2a5 \ub3d9\uc791 \uc778\uc2dd \ud559\uc2b5 \uae30\uc220(Google MediaPipe)\uc744 \uc774\uc6a9\ud55c \ud034\uc988 \uac8c\uc784\uc785\ub2c8\ub2e4.</p><p>- \uc601\uc0c1\ucc98\ub9ac\uc5d0 \ub9ce\uc740 CPU, GPU \uc790\uc6d0\uc774 \uc0ac\uc6a9\ub418\ubbc0\ub85c \ub290\ub824\uc9d0\uacfc \uba48\ucda4 \ud604\uc0c1\uc774 \ubc1c\uc0dd\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.</p><p>- \ud034\uc988 \uc810\uc218 \ub7ad\ud0b9 \uae30\ub85d\uc744 \uc704\ud574\uc11c \ud559\uc0dd\uc758 \uac1c\uc778\uc815\ubcf4\ub97c \uc77c\ubd80 \uc870\ud68c \uc0ac\uc6a9\ud569\ub2c8\ub2e4. (\ud559\ub144,\ubc18, \uc774\ub984 2\uae00\uc790 \uc608: \ud64d*\ub3d9) </p><p>- \ubbf8\uc644\uc131 \uac1c\ubc1c \uc911\uc778 \ud14c\uc2a4\ud2b8 \ubc84\uc804\uc73c\ub85c \uc624\ub958\uac00 \uc788\uc744 \uc218 \uc788\uc2b5\ub2c8\ub2e4. \uc624\ub958\ub098 \uac1c"
                        "\uc120\uc0ac\ud56d\uc740 \uc815\uc6d0\uae38\uc0d8 \uc5d0\uac8c  \uc54c\ub824\uc8fc\uc138\uc694</p></body></html>", None))
        self.lb_fps.setText(QCoreApplication.translate("startWait", u" FPS", None))
        self.lb_challenge.setText(QCoreApplication.translate("startWait", u"\ud034\uc988\uc5d0 \ub3c4\uc804\ud574 \ubcf4\uc138\uc694!", None))
        self.lb_type2.setText(QCoreApplication.translate("startWait", u"\uc2a4\ud53c\ub4dc \ud034\uc988", None))
        self.lb_face_icon.setText(QCoreApplication.translate("startWait", u"face_icon", None))
        self.lb_verInfo.setText(QCoreApplication.translate("startWait", u"\ud504\ub85c\uadf8\ub7a8 v00  |  \ud034\uc988 v00  |  Program developer : 000", None))
        self.lb_hand_icon.setText(QCoreApplication.translate("startWait", u"hand_icon", None))
        self.lb_cmdMsg.setText(QCoreApplication.translate("startWait", u"CMD_MSG", None))
        self.lb_visitorTotalCount.setText(QCoreApplication.translate("startWait", u"\ub204\uc801 \ubc29\ubb38\uc790 : \uba85", None))
        self.lb_visitorCount.setText(QCoreApplication.translate("startWait", u"\uc624\ub298 \ubc29\ubb38\uc790 : \uba85", None))
        self.lb_title_img.setText(QCoreApplication.translate("startWait", u"__", None))
        self.lb_quizArea.setText(QCoreApplication.translate("startWait", u"-", None))
        self.lb_quizTime.setText(QCoreApplication.translate("startWait", u"\uc81c\ud55c\uc2dc\uac04 02:30", None))
        self.lb_chAnswer_2.setText(QCoreApplication.translate("startWait", u"<html><head/><body><p>- \uac1c\uc778\uc815\ubcf4 \ub3d9\uc758 \uc5c6\uc774 \uc190\ub2d8\uc73c\ub85c \ucc38\uc5ec \uac00\ub2a5\ud569\ub2c8\ub2e4. </p><p>- \uc601\uc0c1\ucc98\ub9ac(OpenCV), \uc778\uacf5\uc9c0\ub2a5 \ub3d9\uc791 \uc778\uc2dd \ud559\uc2b5 \uae30\uc220(Google MediaPipe)\uc744 \uc774\uc6a9\ud55c \ud034\uc988 \uac8c\uc784\uc785\ub2c8\ub2e4.</p><p>- \uc601\uc0c1\ucc98\ub9ac\uc5d0 \ub9ce\uc740 CPU, GPU \uc790\uc6d0\uc774 \uc0ac\uc6a9\ub418\ubbc0\ub85c \ub290\ub824\uc9d0\uacfc \uba48\ucda4 \ud604\uc0c1\uc774 \ubc1c\uc0dd\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.</p><p>- \ud034\uc988 \uc810\uc218 \ub7ad\ud0b9 \uae30\ub85d\uc744 \uc704\ud574\uc11c \ud559\uc0dd\uc758 \uac1c\uc778\uc815\ubcf4\ub97c \uc77c\ubd80 \uc870\ud68c \uc0ac\uc6a9\ud569\ub2c8\ub2e4. (\ud559\ub144,\ubc18, \uc774\ub984 2\uae00\uc790 \uc608: \ud64d*\ub3d9) </p><p>- \ubbf8\uc644\uc131 \uac1c\ubc1c \uc911\uc778 \ud14c\uc2a4\ud2b8 \ubc84\uc804\uc73c\ub85c \uc624\ub958\uac00 \uc788\uc744 \uc218 \uc788\uc2b5\ub2c8\ub2e4. \uc624\ub958\ub098 \uac1c"
                        "\uc120\uc0ac\ud56d\uc740 \uc815\uc6d0\uae38\uc0d8 \uc5d0\uac8c  \uc54c\ub824\uc8fc\uc138\uc694</p></body></html>", None))
        self.lb_mode_img.setText(QCoreApplication.translate("startWait", u"mode_img", None))
    # retranslateUi

