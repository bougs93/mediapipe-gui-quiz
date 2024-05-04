'''


'''


from PySide6 import QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
import sys

from PySide6.QtCore import *
import mediapipe as mp
import numpy as np
from openpyxl import Workbook, load_workbook
from rank_json_rw import RankJsonRW

from setup import *
import val

class RankingTableView():
    def __init__(self, rankingTable):
        

        self.rankingTable = rankingTable
        # Qt의 모델-뷰 아키텍처를 처음 사용하기 때문에 익숙해질 때까지 QStandardItemModel을 사용하는 것이 좋습니다. 
        #   https://stackoverflow.com/questions/15290932/qtablewidget-vs-qtableview
        #   https://doc.qt.io/qt-6/modelview.html
        # 
        # qtable color
        #   https://stackoverflow.com/questions/36196988/color-individual-horizontal-headers-of-qtablewidget-in-pyqt
        # qtable 함수
        #   https://wikidocs.net/35498
        # QTableWidget 생성, 항목 설정, 자동 줄 간격, 데이터 추가, 삭제, 정렬 하는 법
        #   https://bysik1109.tistory.com/24

        self.rankingTable.setRowCount(20)
        self.rankingTable.setColumnCount(6)

        # rankingTable.setStyleSheet('''border: none; background-color: #CCC''')

        # columnHeaders = ['RANK','SCORE','TOTAL', 'ID', 'NAME','TIME' ]
        columnHeaders = ['순위','점수','문제개수', '학번', '이 름','시간' ]
        self.rankingTable.setHorizontalHeaderLabels(columnHeaders)
        self.rankingTable.verticalHeader().setVisible(False)     # https://stackoverflow.com/questions/2942951/removing-index-numbers-in-qtablewidget


        # PyQt5, QtableWidget 컬럼 너비 자동 조정
        #   https://kwonkyo.tistory.com/370#gsc.tab=0
        table = self.rankingTable
        print('** self.size = ', table.width(), table.height())
        # t = 16
        # https://stackoverflow.com/questions/38098763/pyside-pyqt-how-to-make-set-qtablewidget-column-width-as-proportion-of-the-a
        #   Interactive = ... # type: QHeaderView.ResizeMode
        #   Fixed = ... # type: QHeaderView.ResizeMode
        #   Stretch = ... # type: QHeaderView.ResizeMode
        #   ResizeToContents = ... # type: QHeaderView.ResizeMode
        #   Custom = ... # type: QHeaderView.ResizeMode
        header = table.horizontalHeader() 
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents  )   #순위
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents  )   #점수
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents  )   #문제 6
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents  )   #학번 
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed )   #이름 6.12
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch )   #시간 5
        t = 16
        table.setColumnWidth(0, int(table.width()*2/t))   #순위
        table.setColumnWidth(1, int(table.width()*2/t))   #점수
        table.setColumnWidth(2, int(table.width()*2/t))   #문제 6
        table.setColumnWidth(3, int(table.width()*2/t))   #학번 
        table.setColumnWidth(4, int(table.width()*2/t))   #이름 6.12
        table.setColumnWidth(5, int(table.width()*4/t))   #시간 5

        # 높이 조절
        table.horizontalHeader().setMinimumHeight(table.height()/21)
        table.verticalHeader().setDefaultSectionSize(table.height()/21) # https://bmwe3.tistory.com/1742

        # https://m.blog.naver.com/browniz1004/221411876897
        table.horizontalHeader().setStyleSheet("QHeaderView::section { \
                                                background-color: rgba(0, 0, 0, 255); \
                                                color: rgba(255, 255, 255, 255); \
                                                font: 700 11pt '나눔스퀘어라운드 ExtraBold'; \
                                                border: 0px;}") 
        table.setShowGrid(False)            # 그리드 라인 지우기
        table.setFrameStyle(QFrame.NoFrame) # 프레임 라인 지우기
        table.setFocusPolicy(Qt.NoFocus)
        table.setStyleSheet('background-color: rgba(0, 0, 0, 0)')   # 테이블 전체를 투명하게
       
        # 
        self.rankJsonRW = RankJsonRW()

    #### quiz_end 후 랭킹 테이블에서 자신의 랭킹 확인용 #### 
    def myRankView(self, idx):

        # 랭킹뷰용 데이터 블러오기
        self.viewRank = self.rankJsonRW.viewLoad()
        total_row = len(self.viewRank)

        table_row = self.rankingTable.rowCount()        # 총 랭킹 갯수
        table_col = self.rankingTable.columnCount()     # 칼럼

        # 랭킹 개수보다 idx 큰 경우 마지막 페이지만 표시
        if idx > total_row:
            page_idx = None
            page = int(total_row / table_row)
        else:
            page_idx = idx % table_row      # 페이지 내의 인덱스
            page = int(idx / table_row)     # 페이지 계산

        start = page*table_row
        end = page*table_row + table_row

        # print( 'start=', start ,'total_row=', total_row, 'page_idx=', page_idx)

        # for i in range(rankingTable.rowCount()):
        for i in range(start, end):
            # table.columnCount() : column 개수 리턴
            for j in range(table_col):
                # 테이블 위젯에 아이템 생성
                item = QTableWidgetItem()
                #  아이템에 데이터 삽입
                try:
                    item.setText(str(self.viewRank[i][j]))     # index out of range
                    
                    ''' #### ID 정보 일부분 숨기기 #### '''
                    _id = str(self.viewRank[i][RA_ID])
                    _idList = list(_id)
                    try:
                        _idList[-1] = '*'
                        _idList[-2] = '*'
                    except IndexError:
                        pass
                    _id =''.join(_idList)
                    self.viewRank[i][RA_ID] = _id
                    ''' #### #################### #### '''

                except IndexError:
                    item.setText('')

                item.setTextAlignment(Qt.AlignCenter)

                # []--------첫칼럼
                if j == 0:
                    # item.setForeground(QColor(188, 1, 108))          # 글자 색상(자두색)
                    item.setForeground(QColor(255, 255, 255))          # 글자 색상(흰색)
                    item.setBackground(QColor(100, 100, 150, 200))   # 배경 색상
                # -[][][][][] 나머니 칼럼
                else:
                    # item.setForeground(QColor(255, 255, 255))  
                    item.setForeground(QColor(0, 0, 0))  
                    item.setBackground(QColor(255,255,255, 200))     # 배경색상

                # -----[5] 날짜 칼럼 - 부분 폰트 사이즈 조절
                if j == 5:
                    item.setFont(QFont('나눔스퀘어라운드 ExtraBold', 12))
                else:
                    item.setFont(QFont('나눔스퀘어라운드 ExtraBold', 14))

                # [][][][][][][] = idx 라인 색상 강조
                if i-start == page_idx:
                    # []------    첫칼럼
                    if j == 0:
                        item.setBackground(QColor(100,100,150, 255))    # 배경 색상
                    # -[][][][][][] 나머지 컬럼
                    else:
                        item.setBackground(QColor(255,255,255, 255))    # 배경색상
                    item.setForeground(Qt.red)

                # 아이템을 테이블에 세팅
                self.rankingTable.setItem(i-start, j, item)


    def RankAllView(self):
        self.viewRank = self.rankJsonRW.viewLoad()
        self.total_row = len(self.viewRank)
        
        self.tabletimer = QTimer()
        # self.timer_rem = QTime.fromString(REG_KEY_TIME_OUT, 'ss')
        self.tabletimer.setInterval(RANK_TABLE_VIEW_INTERVAL)
        self.tabletimer.timeout.connect(self.tabletimer_timeout)
        self.tabletimer.start()

        self.timer_idx = 0

    
    def tabletimer_timeout(self):
        self.myRankView(self.timer_idx)
        self.timer_idx += 1

        if self.timer_idx > self.total_row -1:
            self.timer_idx = 0

    def tabletimer_stop(self):
        self.tabletimer.stop()


class RankingTableView2(RankingTableView):
    def __init__(self, rankingTable):

        self.rankingTable = rankingTable

        self.rankingTable.setRowCount(20)
        self.rankingTable.setColumnCount(6)

        # 랭킹| 스코어 | 학교 | 학년반 | 이름 | 시간
        columnHeaders = ['순위','점수','학교', '학년반', '이름','시간' ]
        self.rankingTable.setHorizontalHeaderLabels(columnHeaders)
        self.rankingTable.verticalHeader().setVisible(False)     # https://stackoverflow.com/questions/2942951/removing-index-numbers-in-qtablewidget


        table = self.rankingTable
        print('** self.size = ', table.width(), table.height())

        header = table.horizontalHeader() 
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents  )   #순위
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents  )   #점수
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents  )   #문제 6
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents  )   #학번 
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed )   #이름 6.12
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch )   #시간 5
        t = 16
        table.setColumnWidth(0, int(table.width()*2/t))   #순위
        table.setColumnWidth(1, int(table.width()*2/t))   #점수
        table.setColumnWidth(2, int(table.width()*2/t))   #문제 6
        table.setColumnWidth(3, int(table.width()*2/t))   #학번 
        table.setColumnWidth(4, int(table.width()*2/t))   #이름 6.12
        table.setColumnWidth(5, int(table.width()*4/t))   #시간 5

        # 높이 조절
        table.horizontalHeader().setMinimumHeight(table.height()/21)
        table.verticalHeader().setDefaultSectionSize(table.height()/21) # https://bmwe3.tistory.com/1742

        # https://m.blog.naver.com/browniz1004/221411876897
        table.horizontalHeader().setStyleSheet("QHeaderView::section { \
                                                background-color: rgba(0, 0, 0, 255); \
                                                color: rgba(255, 255, 255, 255); \
                                                font: 700 11pt '나눔스퀘어라운드 ExtraBold'; \
                                                border: 0px;}") 
        table.setShowGrid(False)            # 그리드 라인 지우기
        table.setFrameStyle(QFrame.NoFrame) # 프레임 라인 지우기
        table.setFocusPolicy(Qt.NoFocus)
        table.setStyleSheet('background-color: rgba(0, 0, 0, 0)')   # 테이블 전체를 투명하게
       
        # 
        self.rankJsonRW = RankJsonRW()
