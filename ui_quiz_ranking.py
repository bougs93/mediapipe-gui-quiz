# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_quiz_ranking.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QSizePolicy,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_ranking_widget(object):
    def setupUi(self, ranking_widget):
        if not ranking_widget.objectName():
            ranking_widget.setObjectName(u"ranking_widget")
        ranking_widget.resize(438, 718)
        self.lb_rankTitle = QLabel(ranking_widget)
        self.lb_rankTitle.setObjectName(u"lb_rankTitle")
        self.lb_rankTitle.setGeometry(QRect(0, 0, 431, 41))
        self.lb_rankTitle.setMinimumSize(QSize(100, 0))
        font = QFont()
        font.setFamilies([u"\ub098\ub214\uc2a4\ud018\uc5b4\ub77c\uc6b4\ub4dc Bold"])
        font.setPointSize(16)
        font.setBold(True)
        self.lb_rankTitle.setFont(font)
        self.lb_rankTitle.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(55, 71, 158);\n"
"border-radius: 0px;")
        self.lb_rankTitle.setAlignment(Qt.AlignCenter)
        self.tbw_ranking = QTableWidget(ranking_widget)
        self.tbw_ranking.setObjectName(u"tbw_ranking")
        self.tbw_ranking.setGeometry(QRect(0, 40, 431, 671))

        self.retranslateUi(ranking_widget)

        QMetaObject.connectSlotsByName(ranking_widget)
    # setupUi

    def retranslateUi(self, ranking_widget):
        ranking_widget.setWindowTitle(QCoreApplication.translate("ranking_widget", u"Form", None))
        self.lb_rankTitle.setText(QCoreApplication.translate("ranking_widget", u"QUIZ RANKING", None))
    # retranslateUi

