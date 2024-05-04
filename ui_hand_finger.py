# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_hand_finger.ui'
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

class Ui_hand_widget(object):
    def setupUi(self, hand_widget):
        if not hand_widget.objectName():
            hand_widget.setObjectName(u"hand_widget")
        hand_widget.resize(500, 500)
        self.wg_fingerText = QWidget(hand_widget)
        self.wg_fingerText.setObjectName(u"wg_fingerText")
        self.wg_fingerText.setGeometry(QRect(170, 170, 160, 160))
        self.wg_fingerText.setStyleSheet(u"")
        self.lb_circle = QLabel(self.wg_fingerText)
        self.lb_circle.setObjectName(u"lb_circle")
        self.lb_circle.setGeometry(QRect(24, 0, 120, 120))
        self.lb_circle.setStyleSheet(u"background-color: rgba(255, 255, 255, 200);\n"
"border-radius: 60px;")
        self.lb_fingerText = QLabel(self.wg_fingerText)
        self.lb_fingerText.setObjectName(u"lb_fingerText")
        self.lb_fingerText.setGeometry(QRect(29, 22, 111, 91))
        font = QFont()
        font.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font.setPointSize(72)
        font.setBold(True)
        self.lb_fingerText.setFont(font)
        self.lb_fingerText.setStyleSheet(u"selection-background-color: rgba(255, 255, 255, 0);")
        self.lb_fingerText.setAlignment(Qt.AlignCenter)
        self.pb_fingerText = QProgressBar(self.wg_fingerText)
        self.pb_fingerText.setObjectName(u"pb_fingerText")
        self.pb_fingerText.setGeometry(QRect(16, 126, 131, 26))
        self.pb_fingerText.setStyleSheet(u"QProgressBar {\n"
"            border: 2px solid grey;\n"
"            border-radius: 5px;\n"
"            text-align: center;\n"
"        }")
        self.pb_fingerText.setValue(24)

        self.retranslateUi(hand_widget)

        QMetaObject.connectSlotsByName(hand_widget)
    # setupUi

    def retranslateUi(self, hand_widget):
        hand_widget.setWindowTitle(QCoreApplication.translate("hand_widget", u"Form", None))
        self.lb_circle.setText("")
        self.lb_fingerText.setText(QCoreApplication.translate("hand_widget", u"5", None))
    # retranslateUi

