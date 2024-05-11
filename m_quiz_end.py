# OpenCV(Python) + PyQt
#  https://blog.xcoda.net/104


'''
디자인 참고
    https://github.com/MariyaSha/TriviaGame

'''

####### 사용자 퀴즈 데이터 형식 지정 #######
# user_quiz_data =[]
# [0]학번 /사용자명 / 시작 시간 / 풀이시간
# [1]순번     :
# [2]문항번호  :
# [3]답       :
# [4]Y/N/P    :
# [5]응답     :

# SEQ = 1; QNO = 2; ANS = 3; YNP = 4; REQ = 5; 

# self.quiz_line[]
# Q_NO = 0            # 문항 번호
# Q_TYPE = 1          # 문제타입 OX, C
# Q_TYPE_CHOICE = 'C'
# Q_TYPE_OX = 'OX'
# Q_SUBJECT = 2       # 과목(영역)
# Q_QUESTION = 3      # 문제
# Q_ANSWER = 4        # 정답
# Q_CHOICE = 5        # 선택1~
# Q_START_ROW = 3  # 데이터 시작줄


######################################
# 카메라 OpenCV -> QImage 로 뛰우기
######################################
import sqlite3
from PySide6 import QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
import sys

from PySide6.QtCore import *
import mediapipe as mp
import numpy as np
from openpyxl import Workbook, load_workbook
from ranking_table_view import RankingTableView
from circular_progress import CircularProgress
from key_press_timer import Key3PressTimer
from rank_json_rw import RankJsonRW

import val

from rank_widget import *

###############
from thread_video import *

## .ui -> .py ##
from pyside6_uic import PySide6Ui
from ui_quiz_end import Ui_quizEndView


class QuizEndDisplay(QWidget, Ui_quizEndView):

    sound_play_signal = Signal(str)
    main_to_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Ui_quizView

        self.setWindowTitle("퀴즈 결과")
        self.lb_info2.setText('')

        # https://www.geeksforgeeks.org/pyqt5-access-the-size-of-the-label/
        imageView_width, imageView_height = self.lb_imageView.size().width(), self.lb_imageView.size().height()
        print('frameView Size:',imageView_width, imageView_height)

        # self.lb_chAnswer.setStyleSheet("border : 8px solid black")
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(3)
        shadow.setColor(Qt.black)
        self.lb_quizArea.setGraphicsEffect(shadow)

        # shadow1 = QGraphicsDropShadowEffect(self)
        # shadow1.setBlurRadius(5)
        # shadow1.setOffset(2)
        # shadow1.setColor(Qt.white)
        # # self.lb_question.setGraphicsEffect(shadow1)

        ##### 버전 정보 표시 #####
        try:
            self.lb_verInfo.setText( f'프로그램 {PROGRAM_VER}  |  퀴즈 {QUIZ_VER}  |  Program developer : {PROGRAM_DEVELOPER}')
        except:
            pass

        self.keyOneInput = True   # 퀴즈 중 다른 키 입력되어 연속 동작 방지
        
        # 랭킹파일 모듈 로딩
        self.rankJsonRW = RankJsonRW()

        # 랭킹 테이블 위젯 초기화
        #   테이블 지정 : self.tbw_ranking
        # self.rankingTableView = RankingTableView(self.tbw_ranking)

        ##### Create Circular Progress
        self.progress = CircularProgress()
        self.progress.value = 0
        self.progress.suffix = "%"
        self.progress.font_size = 35
        self.progress.text_color = 0xffffff
        self.progress.width = 300
        self.progress.height = 300
        self.progress.progress_width = 20
        self.progress.progress_color = 0xffffff
        self.progress.progress_rounded_cap = True
        self.progress.add_shadow(True)
        self.progress.text = 'OK'

        self.fr_ranking.setStyleSheet('')

        # Center CircularProgress
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.progress)
        self.center_progress.setLayout(self.vlayout)

        ## Key Press Timer 생성 ( timer: 2000ms)
        self.progress.hide()
        self.startPressKeyTimer = Key3PressTimer(KEY3_TIMER_INTERVAL, KEY3_PUSH_TIME, KEY3_VIEW_DELAY, self.progress)

        # # NEW
        self.createRankWidget()

        # 터치 연속 입력 제한
        self.key_repeat_ready = True    

        # ###### 퀴즈 모드 이미지 ######
        self.lb_mode_img.setScaledContents(False)   # False 상태에서, 스케일 동작함.
        if EXHIBITION_MODE:
            pixmap_mode = QPixmap(f'{IMG_PATH}{IMG_MODE_EXHIBITION}')
        else:
            pixmap_mode = QPixmap(f'{IMG_PATH}{IMG_MODE_SCHOOL}')
        pixmap_mode = pixmap_mode.scaled(self.lb_mode_img.size().width(), self.lb_mode_img.size().height(), Qt.KeepAspectRatio) 
        self.lb_mode_img.setPixmap(pixmap_mode)


    def displayStart(self):
        ### 테스트용 ###################
        # val.st_id = '123'
        # val.st_name = '손님'

        # val.st_score = 30
        # val.st_quiz_cnt = 22
        # val.st_right_cnt = 24
        # val.st_wrong_cnt = 2
        # val.st_pass_cnt = 1
        # val.st_quizStartTime = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        # val.st_rank = None
        ##############################
        self.sound_play_signal.emit('stop') # 틱톡 소리 중지
        QTimer.singleShot( 1000, lambda: self.sound_play_signal.emit('Q_END'))

        self.quizEndTimer_start()
        self.rankingCalculate()         # 랭킹 계산 / self.userIndex 결과
        self.quizEnd_resultView()

        self.db_visit_update()          # 퀴즈 결과 DB 업데이트

        self.rankView.rankingTableView.myRankView(self.userIndex)    # 랭킹 테이블 출력
        # self.rankingTableView.myRankView(999)
        
        if MENU_ANIMATION:
            self.animation_start()
        self.key_repeat_ready = True

        #############################################################
        # view
    def quizEnd_resultView(self):
        self.lb_no.setText('문제 :' + str(val.st_quiz_cnt))

        if QUIZ_TYPE == 'speed':
            self.lb_type2.setText('스피드 퀴즈 결과')
        elif QUIZ_TYPE == 'golden':
            self.lb_type2.setText('골든벨 퀴즈 결과')

        # self.lb_quizTime.setText('제한시간 '+ QTime.fromString(val.speedQuizTime, 'm:s').toString('mm:ss'))

        line1 = f'도전자: {val.st_id} {val.st_name}'
        line2 = f'문제:{str(val.st_quiz_cnt)} 정답:{str(val.st_right_cnt)} 오답:{str(val.st_wrong_cnt)} 통과:{str(val.st_pass_cnt)}'
        line3 = f'{val.st_quizStartTime}'
        info_view = info_format.replace('_line1', line1).replace('_line2', line2).replace('_line3', line3)
        self.lb_info.setText(info_view)
        if val.st_rank == None or val.st_rank == 0: 
            self.lb_score.setText(f'<p>{str(val.st_score)}점</p><p> </p>')
        else:
            self.lb_score.setText(f'<p>{str(val.st_score)}점</p><p>{str(val.st_rank)}위</p>')


    def quizEndTimer_start(self):
        #############################################################
        # TIMER
        self.timer = QTimer()
        self.timer_rem = QTime.fromString(QUIZ_END_VIEW_TIME, 's')
        self.timer.setInterval(QTIMER_INTERVAL)
        self.timer.timeout.connect(self.timer_timeout)
        self.timer.start()
        print(" >> timer start : ", self.timer_rem)
        #############################################################


    def rankingCalculate(self):
        self.rankRead = self.rankJsonRW.read()

        # RANK_RANK = 0; RANK_SCORE=1; RANK_TOTAL=2; RANK_ID=3; RANK_SCHOOL=4; RANK_GRADE=5 ;RANK_NAME=6; RANK_DTIME=7

        # 테스트시 에러 방지 목적
        if val.st_quizStartTime == None:
            val.st_quizStartTime = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")

        ### 새로운 랭킹 데이터 생성 ###
        #         newUser = [val.st_rank, val.st_score,  val.st_quiz_cnt, val.st_id, val.st_name, val.st_quizStartTime]

                #  순위          점수           퀴즈갯수         아이디     학교                 학년        이름           시간
        newUser = [val.st_rank, val.st_score, val.st_quiz_cnt, val.st_id, val.st_school, val.st_grade, val.st_name, val.st_quizStartTime ]
        print( f'일반 모드 newUser = {newUser}')

        if val.st_score <= 0 or val.st_id == '' or val.st_name == '손님':
            # 점수가 0 이하 또는 id가 없는 손님인 경우
            findTag = 'not'
        else:
            # 1) id 찾기 / 점수,문제수 비교하여 => 추가 여부 결정
            findTag = None
            _findUser = []
            for idx, user in  enumerate(self.rankRead):
                if user[RANK_ID] == val.st_id:
                    # id 를 찾은 경우
                    _findUser = user
                    findTag = 'find'
                    # 기록된 점수 비교 if(현점수>기록된 점수 and 총문제<기록된 총문제)
                    # if val.st_score > user[RANK_SCORE] and val.st_quiz_cnt < user[RANK_TOTAL]:
                    if val.st_score > user[RANK_SCORE]:        # 점수 초과
                        self.rankRead[idx] = newUser         #   덮어 쓰기
                        findTag = 'find_write'
                    elif  val.st_score == user[RANK_SCORE]:    # 점수 같은경우,
                        if val.st_quiz_cnt < user[RANK_TOTAL]: #   문제수가 작은 경우
                            self.rankRead[idx] = newUser
                            findTag = 'find_write'
                        elif val.st_quiz_cnt == user[RANK_TOTAL]:
                            self.rankRead[idx] = newUser
                            findTag = 'find_same'
                    else:
                        findTag = 'find_NotWrite'

        # print('>> ', findTag)
        if findTag == None:
            self.rankRead.append(newUser)   # 랭킹 리스트 추가
            self.lb_info2.setText(f'처음 참여한 기록입니다.')
        elif findTag == 'find_same':
            self.lb_info2.setText(f'이전 기록과 동일합니다.')
        elif findTag == 'find_write':
            self.lb_info2.setText(f'<p> 축하합니다. 이전 기록을 갱신했습니다.</p>\
                                  <p> 이전 기록은 {_findUser[RANK_RANK]}위 {_findUser[RANK_SCORE]}점 {_findUser[RANK_TOTAL]}문제 입니다.</p>')
        elif findTag == 'find_NotWrite':
            self.lb_info2.setText(f'<p> 아쉽네요. 이전 기록을 갱신 못했습니다.</p>\
                                  <p> 이전 기록은 {_findUser[RANK_RANK]}위 {_findUser[RANK_SCORE]}점 {_findUser[RANK_TOTAL]}문제 입니다.</p>')
        
        elif findTag == 'not':
            # 종료
            self.lb_info2.setText(f'0점 이하 또는 손님의 경우 랭킹에 기록되지 않습니다.')
            self.userIndex = 9999
            return

        # 2) 리스트 정렬하기 / 2차원 배열 정렬하기 https://haesoo9410.tistory.com/193
        #   (1) 최근 날짜순
        self.rankRead.sort(reverse = True, key=lambda x:x[RANK_DTIME])

        #   (2) 문제수 적은순
        if EXHIBITION_MODE:
            pass
        else:
            self.rankRead.sort(key=lambda x:x[RANK_TOTAL])

        #   (3) 높은 점수순
        self.rankRead.sort(reverse = True, key=lambda x:x[RANK_SCORE])
        
        #   (4) 순위 구하기 https://wakaranaiyo.tistory.com/72?category=910751
        _rank = 0
        temp = 10000
        for idx, user in enumerate(self.rankRead):
            if user[RANK_SCORE] < temp:
                _rank += 1
                self.rankRead[idx][RANK_RANK] = _rank
                temp = user[RANK_SCORE]
            else:
                self.rankRead[idx][RANK_RANK] = _rank

        print(f'T3 : {val.st_id}, {type(val.st_id)}, {self.rankRead}')
        #   (5) 순위 index 구하기
        self.userIndex = 0
        for idx, user in  enumerate(self.rankRead):
            if user[RANK_ID] == val.st_id:
                self.userIndex = idx
                userRank = user[RANK_RANK]

        # 현재 순위 변수에 저장
        val.st_rank = userRank
        # File SAVE 저장하기
        self.rankJsonRW.write(self.rankRead)

        # 출력 테스트
        for i in range(len(self.rankRead)):
            print(self.rankRead[i])

        print('self.userIndex =', self.userIndex, 'userRank =', userRank)
        # <추가> 자신의 최고 기록보다 적을 경우, 순위 기록을 하지 안는다.


    def rankingTableAllView(self):
        # self.rankingTableView.RankAllView()
        self.rankView.rankingTableView.RankAllView()
        # self.rankView.move(30,30)

        # 애니메이션 효과
        #   https://www.pythonguis.com/tutorials/qpropertyanimation/
        #   https://zetcode.com/pyqt/qpropertyanimation/
        #   https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QGraphicsItemAnimation.html
        #   https://www.pythonguis.com/tutorials/qpropertyanimation/

        #   https://zetcode.com/pyqt/qpropertyanimation/
        #   https://doc.qt.io/qt-6/qeasingcurve.html

        # print('**** type :', type(self.fr_ranking))

        self.rankView.show()
        if MENU_ANIMATION:
            self.rankView.move(451, 0)
            self.anim = QPropertyAnimation(self.rankView, b"pos")
            self.anim.setStartValue(QPoint(451,0))
            self.anim.setEndValue(QPoint(0,0))
            self.anim.setDuration(3000)
            self.anim.setEasingCurve(QEasingCurve.InOutCubic)
            # QTimer.singleShot(1000, lambda :self.anim.start )
            self.anim.start()


    def rankingTableAllView_stop(self):
        # self.rankingTableView.tabletimer_stop()
        try:
            self.rankView.rankingTableView.tabletimer_stop()
        except:
            pass
        self.rankView.hide()


    def createRankWidget(self):
        #################################################
        # [중요] 위젯에 다른 위젯 넣기
        #################################################
        self.rankView = RankView()
        # Ui "self.fr_main_quiz" QFrame 안에 "self.mentalGView" 위젯 넣기
        self.rankView.setParent(self.fr_ranking)
        self.rankView.lower()
        # self.handCountView.hide()   # 손가락 레이블


    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    '''
    #############################################################################################
    '''

        

    def animation_start(self):
        self.ani_rankView()
        self.ani_infoView()
        # self.ani_chAnswerView()
        print(" display_QuizEnd | animation_start")

    def animation_stop(self):
        try:
            # self.ani_title.finished.disconnect()
            # self.ani_pos_chAnser.finished.disconnect()
            print(" display_QuizEnd | animation_stop")
        except:
            pass
    
    ########################################################################################
    def ani_rankView(self):
        self.rankView.move(451, 0)
        self.anim = QPropertyAnimation(self.rankView, b"pos")
        self.anim.setStartValue(QPoint(451,0))
        self.anim.setEndValue(QPoint(0,0))
        self.anim.setDuration(3000)
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        # QTimer.singleShot(1000, lambda :self.anim.start )
        self.anim.start()

    def ani_infoView(self):
        self.fr_info.move(-741, 170)
        self.ani_info = QPropertyAnimation(self.fr_info, b"pos")
        self.ani_info.setStartValue(QPoint(-741, 170))
        self.ani_info.setEndValue(QPoint(0, 170))
        self.ani_info.setDuration(2000)
        self.ani_info.setEasingCurve(QEasingCurve.InOutCubic)
        self.ani_info.start()


    def timer_timeout(self):
        # <주의> QTime 은 Qtime과 연산이 되지 않음
        #   self.timerSpeedRemainingTime = QTime.currentTime() - self.timerSpeedStartTime
        # 대신 addsec(), addMSec() 가능
        #   https://doc.qt.io/qtforpython-5/PySide2/QtCore/QTime.html#PySide2.QtCore.PySide2.QtCore.QTime.addMSecs
        self.timer_rem = self.timer_rem.addMSecs(-QTIMER_INTERVAL)
        self.lb_countDown.setText(self.timer_rem.toString('s'))
        
        # qtime 비교 연산
        #   https://doc.qt.io/qtforpython-6/PySide6/QtCore/QTime.html
        # print( self.timer_rem.__eq__(QTime.fromString('0:0', 'm:s')) or
        #       self.timer_rem.__ge__(QTime.fromString(SPEED_QUIZ_TIME, 'm:s')) )
        
        # 남은 시간을 가지고 타이머 색상 변경하기
        # if self.timer_rem.__le__(QTime.fromString(QUIZ_TIME_RED, 'm:s')):
        #     self.lb_countDown.setStyleSheet('background-color: rgb(255, 170, 127); color: rgb(170, 0, 127);')
        # else:
        #     self.lb_countDown.setStyleSheet('color : white;')

        timeOverChk = self.timer_rem.__eq__(QTime.fromString('0:0', 'm:s'))

        if timeOverChk :
            # self.lb_countDown.setStyleSheet('color : white;')    # 타이머 색상 복원
            self.timer.stop()
            self.main_to_signal.emit('quiz_start_wait')
            print(" >> timer stop ")




    def db_visit_update(self):
        # 퀴즈 결과 DB 업데이트 작업.

        ### 테스트용 ###################
        # val.st_id = '123'
        # val.st_name = '손님'

        # val.st_quiz_cnt = 22
        # val.st_right_cnt = 24
        # val.st_wrong_cnt = 2
        # val.st_pass_cnt = 1
        # val.st_score = 30
        # val.st_quizStartTime = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        # val.st_rank = None
        # val.quizFileNum = 0
        if val.st_id != '':
        # ##############################
            self.conn = sqlite3.connect(f'{DB_PATH}{DB_BASE_FILE}') 
            self.cursor = self.conn.cursor()  # db 처음 시작 지점

            visitDb = VisitDAO(self.conn)
    
            #########  quiz_visit DB 처리 #########
            quiz_file = val.quizFileList[val.quizFileNum]
            visit_vo1 = VisitData(None, int(val.st_id), quiz_file)

            file_name_quiz_count = visitDb.read_file_name_quiz_count(visit_vo1) + 1

            quiz_count = val.st_right_cnt + val.st_wrong_cnt + val.st_pass_cnt
            #                visit_id, user_id,        file_name, file_name_quiz_count, quiz_count,      right_count,      wrong_count,      pass_count,      score,       date_time
            visit_vo2 = VisitData(None, int(val.st_id), quiz_file, file_name_quiz_count, quiz_count, val.st_right_cnt, val.st_wrong_cnt, val.st_pass_cnt, val.st_score)
            # 퀴즈 결과값 DB 에 추가하기
            visitDb.insert(visit_vo2)

            ######### user DB 처리 #########
            visit_vo3 = VisitData(None, int(val.st_id))
            total_count = visitDb.read_visit(visit_vo3)
            visitDb.update_userdb_visit_count(int(val.st_id), total_count)

            self.cursor.close()
            self.conn.close()


    @Slot(np.ndarray)
    def update_image_slot(self, qt_img):
        """ X:주의 슬롯에 넣으면, 처리 못함.가상 키보드 """
        # self.vr_keyboard(cv_img)

        """Updates the image_label with a new opencv image"""
        # qt_img = self.convert_cv2qt(cv_img) -> thread 에서 처리하는 것으로 변경함.
        self.lb_imageView.setPixmap(qt_img)
    

    @Slot(str)
    def key_one_slot(self, key):
        pass
    
    @Slot(str)
    def finger_repeat_slot(self, finger):
        pass

    @Slot(list)
    def hand_position_slot(self, dataList):
        pass
    
    @Slot(str)
    def key_repeat_slot(self, key):
        if self.key_repeat_ready == False:
            return  
        if key == "OK":
            keyState = True
        else:
            keyState = False

        # 누르는 시간(KEY3_PUSH_TIME)을 넘는 경우
        if self.startPressKeyTimer.state(keyState):
            self.sound_play_signal.emit("OK")
            self.key_repeat_ready = False  
            self.main_to_signal.emit("quiz_start_wait")    # 메인 에 신호를 보낸다.
    
    @Slot(str)
    def fps_signal_slot(self, fps_str):
        self.lb_fps.setText(fps_str)


class VisitData:
    def __init__(self, visit_id=None, user_id=None, file_name=None, file_name_quiz_count=None, quiz_count=None, right_count=None, wrong_count=None, pass_count=None, score=None, date_time=None):
        self.visit_id    = visit_id     # 0
        self.user_id     = user_id      # 1
        self.file_name   = file_name    # 2
        self.file_name_quiz_count = file_name_quiz_count  # 3
        self.quiz_count  = quiz_count   # 4
        self.right_count = right_count  # 5
        self.wrong_count = wrong_count  # 6
        self.pass_count  = pass_count   # 7
        self.score       = score        # 8
        self.date_time   = date_time    # 9
    def __str__(self):
        return f"VisitData(visit_id={self.visit_id}, user_id={self.user_id}, file_name={self.file_name}, file_name_quiz_count={self.file_name_quiz_count}, quiz_count={self.quiz_count}, right_count={self.right_count}, wrong_count={self.wrong_count}, pass_count={self.pass_count}, score={self.score}, date_time={self.date_time})"

class VisitDAO:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        # self.file_name = file_name

    def insert(self, vo):
        _datetime = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
        try:
            self.cursor.execute("INSERT INTO quiz_visit(user_id, file_name, file_name_quiz_count, quiz_count, right_count, wrong_count, pass_count, score, date_time) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (vo.user_id, vo.file_name, vo.file_name_quiz_count, vo.quiz_count, vo.right_count, vo.wrong_count, vo.pass_count, vo.score, _datetime))
            self.conn.commit()
        except Exception as e:
            print(f'ERR quiz_visit insert : {e}')
    
    # 전체 퀴즈파일에 참여한 횟수
    def read_visit(self, vo):
        try:
            self.cursor.execute("SELECT * FROM quiz_visit WHERE user_id=?",
                                 (vo.user_id, ))
            rows = self.cursor.fetchall()
            return len(rows)
        except Exception as e:
            print(f'ERR read_repeat : {e}')
            return 0
        
    # "엑셀파일이름" 퀴즈 파일에 참여한 횟수
    def read_file_name_quiz_count(self, vo):
        try:
            self.cursor.execute("SELECT * FROM quiz_visit WHERE user_id=? AND file_name=?",
                                 (vo.user_id, vo.file_name))
            rows = self.cursor.fetchall()
            return len(rows)
        except Exception as e:
            print(f'ERR read_repeat : {e}')
            return 0
    
    # user DB에 전체 퀴즈파일에 참여한 횟수 update
    def update_userdb_visit_count(self, user_id, total_count):
        try:
            self.cursor.execute("UPDATE user SET visit_count=? WHERE id=?",
                                (total_count, user_id))
            self.conn.commit()
        except Exception as e:
            print(f'ERR update user visit_count: {e}')
        
        


#######################################################################
# 퀴즈 텍스트 형식 지정 | quiz_format.replace('_quiz', '안녕하세요')

info_format = '<style type=text/css> \
p.line1 { \
    color: rgb(142, 198, 63); \
    font-weight: bold; \
    font-size: 40px; \
}  \
</style> \
<p class="line1">_line1</p> \
<p>_line2</p> \
<p>_line3</p>'
# _line1 = 도전자: 0203 홍길동
# _line2 = 문제:00 정답:00 오답:00 통과:00
# _line3 = 2023.05.14 AM 11:23
#######################################################################

if __name__=="__main__":
    from _main import *
    # PySide6Ui('ui_quiz_end.ui').toPy()

    app = QApplication(sys.argv)
    a = QuizEndDisplay()
    a.show()
    a.animation_start()
    val.quizFileList = ['quiz04_beginner_english_vocabulary.xlsx']
    print('val.quizFileList =', val.quizFileList)
    print('val.quizFileNum = ', val.quizFileNum)
    a.db_visit_update()
    sys.exit(app.exec())

