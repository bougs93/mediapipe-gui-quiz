
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from setup import *
from ui_quiz_ranking import Ui_ranking_widget
from ranking_table_view import RankingTableView, RankingTableView2


class RankWidget(QWidget, Ui_ranking_widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class RankView(QWidget):
    def __init__(self):
        super().__init__()
        self.graphicsview = QGraphicsView()
        self.scene = QGraphicsScene(self.graphicsview)
        self.graphicsview.setScene(self.scene) 

        self.graphicsview.setStyleSheet("background: transparent; ")

        self.graphicsview.setFrameShape(QGraphicsView.NoFrame)
        self.graphicsview.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphicsview.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.rankWidget = RankWidget()
        self.rankWidget.setStyleSheet("background-color: transparent; ")

        self.proxy = QGraphicsProxyWidget()
        self.proxy.setWidget(self.rankWidget)
    
        # 중앙을 변환 기준점으로 설정
        self.proxy.setTransformOriginPoint(self.proxy.boundingRect().center())
        # 하단 중앙을 변환 기준점으로 설정
        # self.proxy.setTransformOriginPoint(self.proxy.boundingRect().center().x(), self.proxy.boundingRect().bottom())
        self.scene.addItem(self.proxy)

        # 나머지 설정(1)
        layout = QVBoxLayout(self)
        layout.addWidget(self.graphicsview)
        #################################################
        if RANKING_EXHIBITION_MODE:
            # 전시관 모드 exhibition
            self.rankingTableView = RankingTableView2(self.rankWidget.tbw_ranking)
        else:
            # 일반 모드 general
            self.rankingTableView = RankingTableView(self.rankWidget.tbw_ranking)
        # self.rankingTableView.RankAllView()


