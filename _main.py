'''
스택 위젯 (QStakedWidget)
    https://wikidocs.net/162838

'''

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
import sys, os, time

from PySide6.QtCore import *
import mediapipe as mp
import numpy as np

from m_start_wait import StartWaitDisplay
from m_user_reg import UserRegDisplay
from m_quiz import QuizDisplay
from m_quiz_end import QuizEndDisplay
from m_quiz_mental import QuizMentalDisplay

from thread_video import ThreadVideo
from thread_face_tilt import ThreadFaceTilt

from thread_sound import ThreadSound
from thread_scheduler import ThreadScheduler
# from thread_qr_scanner import ThreadQRScanner
from thread_qr_scanner import QRScanner


from xlsx_quiz_load import *
# 학생 id 화일 읽어 오기
from xlsx_id_load import *
from m_user_reg import *

import val, random
from setup import *

# from xlsx_quiz_load import *

# from PySide6 import QtGui

from pyside6_uic import PySide6Ui

# DATA : ad/del, id, school, grade, class, number, name, gender, etc (,:8개)
# DATA_SPLIT_CHAR_CNT = 8
SCAN_HEADER = 0
SCAN_ID = 1
SCAN_SCHOOL = 2
SCAN_GRADE = 3
SCAN_CLASS = 4
SCAN_NUMBER = 5
SCAN_NAME = 6
SCAN_GENDER = 7
SCAN_ETC = 8



def st_clear():
    print('st_clear : 학생 초기화')
    print(val.st_id, val.st_name)
    val.st_id = ''
    val.st_name = '손님'
    val.st_grade = ''
    val.st_school = ''

def st_state_clear():
    print('st_state_clear : 기록 초기화')
    print(val.st_score, val.st_right_cnt, val.st_wrong_cnt, val.st_pass_cnt, val.st_quizStartTime, val.st_rank)
    val.st_score = 0
    val.st_right_cnt = 0
    val.st_wrong_cnt = 0
    val.st_pass_cnt = 0
    val.st_quizStartTime = None
    val.st_rank = None


# QMainWindows https://wikidocs.net/156100
# 위젯 접근 https://wikidocs.net/166559
class MyWidonws(QMainWindow):
    def __init__(self):
        super().__init__()

        self.quiz_test = False      # 'quiz_test'
        self.e_menu_item = None     # 애니메이션 효과 중지를 위해서 
        self.befor_menu = None              # qr_scan 시 메뉴 전환을 위해서
        self.qr_scan_available = True       # 퀴즈 진행중 qr 스캔 금지
        self.qr_select_quiz_num = None      # qr_scan 에서 퀴즈 선택여부

        ########################################################################
        # 스택 위젯 (QStakedWidget) https://wikidocs.net/162838
        #  1) QStackedWidget 생성
        self.stack = QStackedWidget()

        #  2) 레이아웃 인스턴스 생성
        self.startWaitDisplay = StartWaitDisplay()
        self.userRegDisplay = UserRegDisplay()
        self.quizDisplay = QuizDisplay()
        self.quizEndDisplay = QuizEndDisplay()
        self.quizMentalDisplay = QuizMentalDisplay()    # 멘탈 위젯

        #   사이즈 가져오기(self.startWaitDisplay)
        size = self.startWaitDisplay.size()
        self.stack.setFixedSize(size.width(), size.height())

        #  3) Widget 추가
        self.stack.addWidget(self.startWaitDisplay)
        self.stack.addWidget(self.userRegDisplay)
        self.stack.addWidget(self.quizDisplay)
        self.stack.addWidget(self.quizEndDisplay)
        self.stack.addWidget(self.quizMentalDisplay)    # 멘탈 위젯 추가

        #  4) setCentralWidget <- self.stack
        self.setCentralWidget(self.stack)

        # <> 윈도우 센터에 뛰우기 / PYSIDE6 CENTER WINDOW. 
        #   https://www.loekvandenouweland.com/content/pyside6-center-window.html
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.stack.frameGeometry()
        geo.moveCenter(center)
        # self.move(geo.topLeft())

        # 작업표시줄 때문에 -y 위치가 되는 것을 해결
        #   윈도우 위치 https://flower0.tistory.com/301
        winPos = geo.topLeft()
        if winPos.__pos__().y() < 0:
            self.move(winPos.__pos__().x(), 0)
        else:
            self.move(geo.topLeft())


        #  5) 스택 디스틀레이 하기
        self.stack.show()

        ########################################################################
        # Video Thread 실행하기
        #   이미지 표시 영역의 사이즈 가져오기 
        #       https://www.geeksforgeeks.org/pyqt5-access-the-size-of-the-label/
        self.imageView_width, self.imageView_height = self.startWaitDisplay.lb_imageView.size().width(), self.startWaitDisplay.lb_imageView.size().height()
        print('imageView Size:',self.imageView_width, self.imageView_height)

        #    (1) create the video capture thread
        #     https://stackoverflow.com/questions/7864664/passing-an-argument-when-starting-new-qthread-in-pyqt
        self.threadVideo = ThreadVideo( self.imageView_width, self.imageView_height )
        self.threadSound = ThreadSound()

        #    (2) start the thread
        self.threadVideo.start()
        self.threadSound.start()

        self.threadSound.music_play_signal.connect(self.startWaitDisplay.music_play_slot)

        # 6) state.in 파일 전체 내용 로드
        stateIni_load('all')


        # 타이머 시작
        self.previous_qdate = QDateTime.currentDateTime().date()
        self.mainTimerStart()


        # 최대화 버튼 비활성화
        # https://bskyvision.com/entry/pyside6-창-타이틀바에서-닫기-버튼-최소화-버튼-최대화-버튼-등을-비활성화-되게-하려면
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        # 상단바 숨기기
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # 탑 윈도우
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)


        ## new 화살표 키보드 keyPressEvent 발생하지 않는 문제
        # -> 소스 https://stackoverflow.com/questions/25438616/pyqt-not-recognizing-arrow-keys
        # https://stackoverflow.com/questions/39807858/handle-arrow-key-events-by-setting-the-focus-policy
        self.setChildrenFocusPolicy(Qt.NoFocus)

        ########################################################################
        # 빔프로젝터 스케쥴 컨드롤
        if PROJ_CONTROL:
            #  1) create the video capture thread
            self.threadScheduler = ThreadScheduler()

            #  2) signal connect
            self.threadScheduler.message_signal.connect(self.startWaitDisplay.scheduer_Msg_slot)
            self.threadScheduler.music_signal.connect(self.threadSound.sound_play_slot)
            #    날짜가 변경된 경우
            # self.threadScheduler.daychange_signal.connect(self.daychange_slot)

            #  3) start the thread
            self.threadScheduler.start()

        ''' 
        ########################################################################
          Display - START
        ######################################################################## '''
        self.display_StartWait()
        # self.display_UserReg()
        # self.display_Quiz()
        # self.display_QuizEnd()

        val.how_to_reset_ranking = HOW_TO_RESET_RANKING
        self.ranking_file_reset_ckeck()
        '''
        ######################################################################## '''


        '''
        [Serial Thread 시작하기]
        ########################################################################
        아래 Thread 방식:
           개별실행시 Serial수신되지만,
           Thread 에서 실생시 Serail 데이터 receive 않됨. 
        ######################################################################## '''
        # QR CODE SCANNER
        # # self.threadQRScanner = ThreadQRScanner()
        # self.threadQRScanner.qrScanner_signal.connect(self.qrScanner_slot)
        # self.threadQRScanner.qrSerial_signal.connect(self.qrSerial_slot)
        # self.threadQRScanner.start()

        '''
        [Serial Thread 시작하기]
        ########################################################################
        위 문제 해결한 Thread 방식: Thread 내에서 Serial 데이터 수신 성공
        ######################################################################## '''
        # Step 2: Create a QThread object
        self.workerThread = QThread()

        # Step 3: Create a worker object
        self.threadQRScanner = QRScanner()

        # Step 4: Move worker to the thread
        self.threadQRScanner.moveToThread(self.workerThread)

        # Step 5: Connect signals and slots
        self.threadQRScanner.qrScanner_signal.connect(self.qrScanner_slot)

        # Step 6: Start the thread
        self.workerThread.start()

        # <주의> pyside6의 .moveToThread()방식 에서는 .start() 시작되지 않음
        self.threadQRScanner.open()  

        #################################################################################


    ## new 화살표 키보드 keyPressEvent 발생하지 않는 문제 해결책
    ##   소스 https://stackoverflow.com/questions/25438616/pyqt-not-recognizing-arrow-keys
    def setChildrenFocusPolicy(self, policy):
        def recursiveSetChildFocusPolicy (parentQWidget):
            for childQWidget in parentQWidget.findChildren(QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)
        recursiveSetChildFocusPolicy(self)


    def keyPressEvent(self, e): #키가 눌러졌을 때 실행됨
        # print('debug key :', e)
        # https://newbie-developer.tistory.com/96
        if e.key() == Qt.Key_T:
            # https://bskyvision.com/entry//pyqt5-윈도우-항상-가장-위에-있게-하면서-타이틀-바도-없게-하려면
            # https://www.geeksforgeeks.org/pyqt5-how-to-hide-the-title-bar-of-window/
            
            # https://8bitscoding.github.io/qt/ui/windowflag/
            # # 기존의 Flag에 추가 할때
            # self.setWindowFlags( self.windowFlags() | Qt.WindowStaysOnTopHint)
            # # 기존의 Flag에서 빼고싶을때
            # self.setWindowFlags( self.windowFlags() ^ Qt.WindowStaysOnTopHint)
            # # 중요한 것은 새로 show 해 주어야 한다.

            # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            # self.show()


            # https://doc.qt.io/qtforpython-6/overviews/qtwidgets-widgets-windowflags-example.html

            # https://stackoverflow.com/questions/4850584/pyqt4-how-can-i-toggle-the-stay-on-top-behavior
            # disable it:
            #   self.setWindowFlags(self.windowFlags() & Qt.WindowStaysOnTopHint)
            # # enable it:
            # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            # 탑 윈도우
            # togle it:
            self.setWindowFlags(self.windowFlags() ^ Qt.WindowStaysOnTopHint)
            self.startWaitDisplay.lb_cmdMsg.setText(f'윈도우 : 창 항상위로/항상위로 취소')
            QTimer.singleShot(MSG_CMD_TIME, lambda :self.startWaitDisplay.lb_cmdMsg.setText('') )
            self.show()

        elif e.key() == Qt.Key_W:
            # 상단 메뉴 숨기기
            self.setWindowFlags(self.windowFlags() ^ Qt.FramelessWindowHint)
            self.startWaitDisplay.lb_cmdMsg.setText(f'윈도우 : 상단 메뉴 숨기기/보이기')
            QTimer.singleShot(MSG_CMD_TIME, lambda :self.startWaitDisplay.lb_cmdMsg.setText('') )
            self.show()

        # 빔 프로젝터 ON
        elif (e.key() == Qt.Key_O) and  (self.quiz_test == False):
            if PROJ_CONTROL:
                print('단축키: 빔 프로젝터 ON ')
                self.threadScheduler.now_On()
        
        # 빔 프로젝터 OFF
        elif (e.key() == Qt.Key_F) and  (self.quiz_test == False):
            if PROJ_CONTROL:
                print('단축키: 빔 프로젝터 OFF ')
                self.threadScheduler.now_Off()


        ###### 방향키 : 일반모드 ############
        elif (e.key() == Qt.Key_Up) and (self.quiz_test == False):
            val.musicVolume = round(val.musicVolume + 0.05, 2)
            if val.musicVolume > 1: val.musicVolume = 1.0
            self.threadSound.audio_output.setVolume(val.musicVolume)
            if val.musicVolume < 0: val.musicVolume = 0.0
            print('val.musicVolume = ', val.musicVolume)
            self.startWaitDisplay.lb_cmdMsg.setText(f'음악볼륨 : {int(val.musicVolume*100)}')
            QTimer.singleShot(MSG_CMD_TIME, lambda :self.startWaitDisplay.lb_cmdMsg.setText('') )

        elif (e.key() == Qt.Key_Down) and (self.quiz_test == False):
            val.musicVolume = round(val.musicVolume - 0.05, 2)
            self.threadSound.audio_output.setVolume(val.musicVolume)
            print('val.musicVolume = ', val.musicVolume)
            self.startWaitDisplay.lb_cmdMsg.setText(f'음악볼륨 : {int(val.musicVolume*100)}')
            QTimer.singleShot(MSG_CMD_TIME, lambda :self.startWaitDisplay.lb_cmdMsg.setText('') )

        # 음악 재생.
        elif (e.key() == Qt.Key_Right) and (self.quiz_test == False):
            # 다음 곡 재생
            self.threadSound.musicPlayer.stop()
            # self.threadSound.musicAllPlay() # stop 후 바로 play 시 시스템 다운 현상 발생 
            QTimer.singleShot(MUSIC_NEXT_DELAY_TIME, lambda :self.threadSound.musicAllPlay() )  # MUSIC_NEXT_DELAY_TIME 시간 만큼 지연후 재생(시스템 다운 방지)
            self.startWaitDisplay.lb_cmdMsg.setText(f'음악 : 다음 곡 {val.musicFileName}')
            QTimer.singleShot(MUSIC_NEXT_DELAY_TIME + MSG_CMD_TIME, lambda :self.startWaitDisplay.lb_cmdMsg.setText('') )

        elif (e.key() == Qt.Key_Left) and  (self.quiz_test == False):
            # 이전 곡 재생
            self.threadSound.musicPlayer.stop()
            val.playlist_index = val.playlist_index - 2
            if val.playlist_index < 0:
                val.playlist_index = len(self.threadSound.playlist) -1
                
            # self.threadSound.musicAllPlay() # stop 후 바로 play 시 시스템 다운 현상 발생 
            QTimer.singleShot(MUSIC_NEXT_DELAY_TIME, lambda :self.threadSound.musicAllPlay() )  # MUSIC_NEXT_DELAY_TIME 시간 만큼 지연후 재생(시스템 다운 방지)
            self.startWaitDisplay.lb_cmdMsg.setText(f'음악 : 이전 곡 {val.musicFileName}')
            QTimer.singleShot(MUSIC_NEXT_DELAY_TIME + MSG_CMD_TIME, lambda :self.startWaitDisplay.lb_cmdMsg.setText('') )


        ####### 방향키 : 테스트 모드 ############
        elif (e.key() == Qt.Key_Up) and (self.quiz_test == True):
            val.st_quiz_cnt += 10
            if val.st_quiz_cnt > val.quiz_total:
                val.st_quiz_cnt = val.quiz_total
            # 문제() 퀴즈 보여주기
            # self.quizDisplay.sound_play_signal.emit('Q_START')
            self.quizDisplay.quizLoadNo(val.st_quiz_cnt)

        elif (e.key() == Qt.Key_Down) and (self.quiz_test == True):
            val.st_quiz_cnt -= 10
            if val.st_quiz_cnt < 1: val.st_quiz_cnt = 1
            # 문제() 퀴즈 보여주기
            # self.quizDisplay.sound_play_signal.emit('Q_START')
            self.quizDisplay.quizLoadNo(val.st_quiz_cnt)

        elif (e.key() == Qt.Key_Right) and (self.quiz_test == True):
            val.st_quiz_cnt += 1
            if val.st_quiz_cnt > val.quiz_total:
                val.st_quiz_cnt = val.quiz_total
            # 문제() 퀴즈 보여주기
            # self.quizDisplay.sound_play_signal.emit('Q_START')
            print(f'DEBUG2 st_quiz_cnt : {val.st_quiz_cnt}')
            self.quizDisplay.quizLoadNo(val.st_quiz_cnt)

        elif (e.key() == Qt.Key_Left) and (self.quiz_test == True):
            val.st_quiz_cnt -= 1
            if val.st_quiz_cnt < 1: val.st_quiz_cnt = 1
            
            # 문제() 퀴즈 보여주기
            # self.quizDisplay.sound_play_signal.emit('Q_START')
            self.quizDisplay.quizLoadNo(val.st_quiz_cnt)


        # Ctrl 키
        elif e.modifiers() & Qt.ControlModifier:
            # Ctrl+Q
            # https://gis.stackexchange.com/questions/417355/capturing-ctrlkey-in-keypressevent-in-pyqgis-qgsmaptool
            if e.key() == Qt.Key_Q:
                print('Quiz Quit')
                # https://wikidocs.net/21927
                QCoreApplication.instance().quit()
                self.startWaitDisplay.lb_cmdMsg.setText('프로그램 : 종료')

            elif e.key() == Qt.Key_0:
                self.threadVideo.stop()
                self.threadVideo.captureDevice = CAPTURE_DEVICE0
                self.threadVideo.start()
                print('cam devie 0')
                self.startWaitDisplay.lb_cmdMsg.setText('카메라 : 0번 선택')
                QTimer.singleShot(MSG_CMD_TIME, lambda :self.startWaitDisplay.lb_cmdMsg.setText('') )
                
            elif e.key() == Qt.Key_1:
                self.threadVideo.stop()
                self.threadVideo.captureDevice = CAPTURE_DEVICE1
                self.threadVideo.start()
                print('cam devie 1')
                self.startWaitDisplay.lb_cmdMsg.setText('카메라 : 1번 선택')
                QTimer.singleShot(MSG_CMD_TIME, lambda :self.startWaitDisplay.lb_cmdMsg.setText('') )
            
            elif e.key() == Qt.Key_M:
                # 연속재생/ 단독 재생 Togle
                if val.music_all_play == True:
                    val.music_all_play = False
                    print('음악 : 1회 재생 ', val.music_all_play)
                    self.startWaitDisplay.lb_cmdMsg.setText('음악 : 1회 재생')
                    QTimer.singleShot(MSG_CMD_TIME, lambda :self.startWaitDisplay.lb_cmdMsg.setText('') )
                else : 
                    val.music_all_play = True
                    print('음악 : 연속 재생', val.music_all_play)
                    self.startWaitDisplay.lb_cmdMsg.setText('음악 : 연속 재생')
                    QTimer.singleShot(MSG_CMD_TIME, lambda :self.startWaitDisplay.lb_cmdMsg.setText('') )
            
            elif e.key() == Qt.Key_D:
                if PROJ_CONTROL:
                    print('단축키:  PC 종료 타이머')
                    self.threadScheduler.now_Down_Togle()

            elif e.key() == Qt.Key_5:
                ## 암산 퀴즈모드의 경우 xlsx 파일을 로드하지 않으므로, 중단.
                if val.quizMode == '':
                    return
                
                if self.quiz_test == False:
                    self.quiz_test = True
                    self.threadVideo.button_clear()
                    self.display_QuizTest()
                else:
                    self.main_to_slot('quiz_start_wait')
                    self.quiz_test = False

            elif e.key() == Qt.Key_6:
                if self.quiz_test == False:
                    self.quiz_test = True
                    self.display_QuizMentalTest()
                else:
                    self.display_QuizMentalTestEnd()
                    self.quiz_test = False


    def display_StartWait(self):
        #
        self.qr_scan_available = True

        # 2 손가락 터치
        # 상태파일 불러오기 : 날짜, 카운트, , 볼륨, 퀴즈 파일 번호, 음악인덱스
        stateIni_load('date')

        # if val.previous_quiz_load_date != QDate.currentDate().toString("yyyy-MM-dd"):

        self.display_ConnectChange(self.startWaitDisplay, 1500, self.threadVideo.button_start_create )
        QTimer.singleShot( 1500, self.startWaitDisplay.rankingTableAllView) # 랭킹 테이블 처음부터
        if PROJ_CONTROL:
            self.threadScheduler.sch_quiz_progress_set = False
            
            if self.threadScheduler.sch_prev == 'ON':
                self.startWaitDisplay.sound_play_signal.emit('music_allPlay')
            else:   # self.threadScheduler.sch_prev == 'None' or 'OFF'
                pass
        else:
            self.startWaitDisplay.sound_play_signal.emit('music_allPlay')
        print(f' 오늘 방문자 : {val.visitor_DayCount} 명')
        if val.visitor_DayCount > 0:
            self.startWaitDisplay.lb_visitorCount.setText(f'오늘 방문자 : {val.visitor_DayCount}명')
        if val.visitor_TotalCount > 0:
            self.startWaitDisplay.lb_visitorTotalCount.setText(f'누적 방문자 : {val.visitor_TotalCount}명')
        
        #################################################################
        # 1. 퀴즈 파일 선택
        # val.quizFileCount = ?
        # 방문시 마다 퀴즈 바꾸기

        if PROJ_CONTROL:
            # 쓰레드에서 스케쥴 로딩할때 까지 대기 
            r = True
            while (r):
                try:
                    print(f' 스케쥴 데이터 로딩 {len(self.threadScheduler.daySchedule_data)} 개.', )
                    r = False
                except:
                    print(f' 스케쥴 데이터 로딩 대기중....')
                    time.sleep(1)
            # print(f' 스케쥴 데이터 로딩 {len(self.threadScheduler.daySchedule_data)} 개.', )
        else:
            ### 음악 재생 ######
            QTimer.singleShot(NOT_PROJ_CONTROL_TIME, lambda :self.threadSound.musicAllPlay() )  # MUSIC_NEXT_DELAY_TIME 시간 만큼 지연후 재생(시스템 다운 방지)


        print(f' 퀴즈 파일 : {val.quizFileList}')
        print(f' 퀴즈 선택 모드 : {QUIZ_SELECT_MODE}')
        # print("*** val.previous_quiz_load_date :", val.previous_quiz_load_date)

        if QUIZ_SELECT_MODE == 'seq':
            # print('> a')
            val.quizFileNum += 1
            
        # 방문시 랜덤으로
        elif QUIZ_SELECT_MODE == 'random':
            # print('> b')
            val.quizFileNum = random.randint(0, len(val.quizFileList)-1)

        # 날짜 마다 퀴즈 순서대로 변경하기
        elif (QUIZ_SELECT_MODE == 'day_seq' and val.quiz_in_progress_date_change == True):   # 퀴즈 중 날짜 변경
            # 스케쥴 갯수 확인하여, 퀴즈 변경 여부 결정
            
            if PROJ_CONTROL == True :
                if len(self.threadScheduler.daySchedule_data) == 0:    # 프로젝터 스케쥴 활성화 and 스케쥴이 없는 경우 (다음날 문제 변경없음.)
                    print(f' 스케줄 {len(self.threadScheduler.daySchedule_data)}개로 퀴즈 변경하지 않음')
                else:
                    print(' 다음 퀴즈로 변경')
                    val.quizFileNum += 1    # 다음 퀴즈로 변경
            else:
                print(' 다음 퀴즈로 변경')
                val.quizFileNum += 1    # 다음 퀴즈로 변경

           
        # 날짜 마다 랜덤으로
        elif QUIZ_SELECT_MODE == 'day_random' and val.previous_quiz_load_date != QDate.currentDate().toString("yyyy-MM-dd"):
            # print('> e')
            val.quizFileNum = random.randint(0, len(val.quizFileList)-1)

        # 숫자 오버시 
        if val.quizFileNum > len(val.quizFileList)-1 or val.quizFileNum < 0:
            # print('> f')
            val.quizFileNum = 0
            print(f' 퀴즈 파일 : {val.quizFileNum}')

        print(f' 파일 선택 mode={QUIZ_SELECT_MODE}, fileNum={val.quizFileNum} :', val.quizFileList[val.quizFileNum])
        
        # TEST Log
        # self.threadScheduler.sch_Log_Save(f'QUIZ_SELECT_MODE:{QUIZ_SELECT_MODE}, val.quizFileNum:{val.quizFileNum}, quizFile:{val.quizFileList[val.quizFileNum]}')


        ## grade ##
        ''' 작업하지 않음. '''

        #################################################################
        # 2. 퀴즈파일의 영역이름 불려오기
        qArea =''
        qArea, val.speedQuizTime, val.quizTitleImage, val.quizMode, val.quizOption1, val.quizOption2 = self.quizDisplay.xlsxQuizPreLoad.getQuizInfo(val.quizFileNum)

        # 3. 화면 디스플레이 갱신
        #    1)영역, 문제
        if qArea == None:
            self.startWaitDisplay.lb_quizArea.hide()
            self.quizEndDisplay.lb_quizArea.hide()
        else:
            self.startWaitDisplay.lb_quizArea.setText(qArea)
            self.startWaitDisplay.lb_quizArea.show()
            self.quizEndDisplay.lb_quizArea.setText(qArea)
            self.quizEndDisplay.lb_quizArea.show()
        
        # if qArea != '': 
        #     self.startWaitDisplay.lb_rankTitle.setText(f'{qArea} : RANKING')
        #     self.quizEndDisplay.lb_rankTitle.setText(f'{qArea} : RANKING')

        #    2)퀴즈 시간
        if val.speedQuizTime == 'None':     # str 영역
            val.speedQuizTime = SPEED_QUIZ_DEFAULT_TIME
        else:
            self.startWaitDisplay.lb_quizTime.setText(f"제한 시간 {QTime.fromString(val.speedQuizTime, 'm:s').toString('mm:ss')}")
            self.quizEndDisplay.lb_quizTime.setText(f"제한 시간 {QTime.fromString(val.speedQuizTime, 'm:s').toString('mm:ss')}")
        print(' 파일 영역2 :', qArea)

        #    3)타이틀 이미지
        if val.quizTitleImage != None:
            self.titleImageView(val.quizTitleImage)
        else:
            self.titleImageView(IMG_TITLE_DEFALUT_FILE)

        #    4)퀴즈 로드 날짜 저장
        # val.previous_quiz_load_date = QDate.currentDate().toString("yyyy-MM-dd")

        # 상태파일 저장 : 날짜, 카운트, , 볼륨, 퀴즈 파일 번호, 음악인덱스
        stateIni_save()
        # 스케쥴 갯수 확인하여, 퀴즈 변경 여부 결정
        val.quiz_in_progress_date_change = False


        ############################
        self.startWaitDisplay.displayStart()



    def titleImageView(self, imgFile):
        file_path = f"{IMG_PATH}{imgFile}"
        if os.path.exists(file_path):
            pass
        else:
            file_path = f"{IMG_PATH}{IMG_TITLE_DEFALUT_FILE}"
        self.startWaitDisplay.lb_title_img.move(IMG_TITLE_XY[0], IMG_TITLE_XY[1])
        pixmap_title = QPixmap(file_path)
        pixmap_title = pixmap_title.scaled(IMG_TITLE_SIZE, IMG_TITLE_SIZE,  Qt.KeepAspectRatio)
        self.startWaitDisplay.lb_title_img.resize(IMG_TITLE_SIZE, IMG_TITLE_SIZE)
        self.startWaitDisplay.lb_title_img.setPixmap(pixmap_title)
        self.startWaitDisplay.lb_imageView


    def display_UserReg(self):
        print('[debug] display_UserReg')
        # 2 손가락 터치
        # 상태파일 저장 : 날짜, 카운트, 볼륨, 퀴즈 파일 번호, 음악 인덱스
        stateIni_save()

        if PROJ_CONTROL:
            self.threadScheduler.sch_quiz_progress_set = True

        self.startWaitDisplay.sound_play_signal.emit('music_stop')

        self.display_ConnectChange(self.userRegDisplay,  1500, self.threadVideo.button_user_create)
        ######### qr scan quiz select ##############
        # 테스트 수정이 필요함.
        if self.qr_select_quiz_num != None:
            try:
                self.userRegDisplay.lb_quiz_name.show()
                self.userRegDisplay.lb_quiz_name.setText(val.quizNameList[self.qr_select_quiz_num])
            except IndexError:
                self.qr_select_quiz_num = None
                self.userRegDisplay.lb_quiz_name.hide()

        else:
            self.userRegDisplay.lb_quiz_name.hide()
            self.userRegDisplay.lb_quiz_name.setText('')
        #############################################

        self.userRegDisplay.lb_id.setText('')
        self.userRegDisplay.lb_name.setText('손님')
        QTimer.singleShot( 1000, self.threadVideo.input_touchMode)   # REG_KEY_TIME_OUT
        QTimer.singleShot( 1500, self.userRegDisplay.timerKeyTouch_start)   # REG_KEY_TIME_OUT

        # self.quizDisplay.quizFileLoad('quiz_random')    # 퀴즈 파일 미리 로딩
    
    def display_UserReg_Scan(self):
        stateIni_save()

        if PROJ_CONTROL:
            self.threadScheduler.sch_quiz_progress_set = True

        self.startWaitDisplay.sound_play_signal.emit('music_stop')

        self.display_ConnectChange(self.userRegDisplay,  1000, self.threadVideo.button_user_create)
        ######### qr scan quiz select ##############
        if self.qr_select_quiz_num != None:
            try:
                self.userRegDisplay.lb_quiz_name.show()
                self.userRegDisplay.lb_quiz_name.setText(val.quizNameList[self.qr_select_quiz_num])
            except IndexError:
                self.qr_select_quiz_num = None
                self.userRegDisplay.lb_quiz_name.hide()
                self.userRegDisplay.lb_quiz_name.setText('')
        else:
            self.userRegDisplay.lb_quiz_name.hide()
            self.userRegDisplay.lb_quiz_name.setText('')
        #############################################
        self.userRegDisplay.lb_id.setText(str(val.st_id))
        self.userRegDisplay.lb_school.setText(val.st_school)
        self.userRegDisplay.lb_grade.setText(f'{str(val.st_grade)}학년')
        self.userRegDisplay.lb_name.setText(val.st_name)
        QTimer.singleShot( 1000, self.threadVideo.input_touchMode)   # REG_KEY_TIME_OUT
        QTimer.singleShot( 1500, self.userRegDisplay.timerKeyTouch_start)   # REG_KEY_TIME_OUT
    
    def display_UserReg_Scan_Repeat(self):
        print('[debug] display_UserReg_Scan_Repeat')
        ######### qr scan quiz select ##############
        if self.qr_select_quiz_num != None:
            try:
                self.userRegDisplay.lb_quiz_name.show()
                self.userRegDisplay.lb_quiz_name.setText(val.quizNameList[self.qr_select_quiz_num])
            except IndexError:
                self.qr_select_quiz_num = None
                self.userRegDisplay.lb_quiz_name.hide()
                self.userRegDisplay.lb_quiz_name.setText('')
        else:
            self.userRegDisplay.lb_quiz_name.hide()
            self.userRegDisplay.lb_quiz_name.setText('')
        #############################################
        self.userRegDisplay.lb_id.setText(str(val.st_id))
        self.userRegDisplay.lb_school.setText(val.st_school)
        self.userRegDisplay.lb_grade.setText(f'{str(val.st_grade)}학년')
        self.userRegDisplay.lb_name.setText(val.st_name)
    
    ###########################################################################
    def display_Quiz(self):
        if PROJ_CONTROL:
            self.threadScheduler.sch_quiz_progress_set = True
        self.display_ConnectChange(self.quizDisplay, 0, self.threadVideo.button_clear)
        self.quizDisplay.displayInt()

        self.quizDisplay.quiz1_CreatePreView()
        self.quizDisplay.quiz2_loadReady_finished.connect(self.display_Quiz_slot)
        self.quizDisplay.quiz2_FileLoadSave('quiz_random')
        self.quizDisplay.handCountView.hide()

        # quiz2_FileLoadSave 완료된 이후 실행되어야 한다.
    def display_Quiz_slot(self):
        self.quizDisplay.quiz2_loadReady_finished.disconnect()
        # self.quizDisplay.quiz3_ReadyCount_Start()
        QTimer.singleShot(DISPLAY_CHANGE_DELAY, self.quizDisplay.quiz3_ReadyCount_Start )
    ###########################################################################


    ###########################################################################
    def display_QuizEnd(self):
        # 2 손가락 터치
        # 퀴즈 종료 시점에 QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg(??)) 경우 이미지가 남아 있음.
        QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.threadVideo.input_touchMode)
        QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY+1000, lambda : self.quizDisplay.viewInputModImg(None))
        if PROJ_CONTROL:
            self.threadScheduler.sch_quiz_progress_set = False
        # self.display_ConnectChange(self.quizEndDisplay, 0, self.threadVideo.button_clear)
        self.display_ConnectChange(self.quizEndDisplay, 5000, self.threadVideo.button_ok_create)

        self.quizEndDisplay.displayStart()    #  종료화면 표시 시간 타이머 시작

        ############################
        self.quizEndDisplay.displayStart()


    ###########################################################################
    def display_QuizTest(self):
        # 2 손가락 터치
        # 상태파일 저장 : 날짜, 카운트, , 볼륨, 퀴즈 파일 번호, 음악인덱스
        stateIni_save()

        if PROJ_CONTROL:
            self.threadScheduler.sch_quiz_progress_set = True
        self.threadSound.sound_play_slot('music_stop')
        self.display_ConnectChange(self.quizDisplay, 0, self.threadVideo.button_clear)
        self.quizDisplay.displayInt()

        self.quizDisplay.quiz1_CreatePreView()
        self.quizDisplay.quiz2_loadReady_finished.connect(self.display_QuizTest_slot)
        self.quizDisplay.quiz2_FileLoadSave('quiz_seq')    # 순서대로 로딩
        if MENU_ANIMATION:
            QTimer.singleShot(1000, self.startWaitDisplay.animation_stop)
        else:
            QTimer.singleShot(1000, self.startWaitDisplay.change_chAnswerView_stop)

        # quiz2_FileLoadSave 완료된 이후 실행되어야 한다.
    def display_QuizTest_slot(self):
        self.quizMentalDisplay.quiz_in_progress = 'stop' # 'stop' : 중지, 'quiz_progress': 퀴즈중, 'quiz_end' 퀴즈 종료

        self.quizDisplay.quiz2_loadReady_finished.disconnect()
        QTimer.singleShot(DISPLAY_CHANGE_DELAY, self.quizDisplay.quiz4_Test_Start )
        self.quizDisplay.lb_usrName.setText("QUIZ TEST")
    ###########################################################################


    ###########################################################################
    def display_QuizMental(self):
        # 상태파일 저장 : 날짜, 카운트, , 볼륨, 퀴즈 파일 번호, 음악인덱스
        stateIni_save()

        if PROJ_CONTROL:
            self.threadScheduler.sch_quiz_progress_set = True

        self.quizMentalDisplay.lb_imageView.clear()

        app.processEvents() # 대기 중인 이벤트를 처리하고 반환합니다. 이를 통해 화면이 갱신되기를 기다릴 수 있습니다.
        self.threadVideo.stop()

        #  1) create the video capture thread
        self.threadFaceTitle = ThreadFaceTilt(self.quizMentalDisplay.imageView_width, self.quizMentalDisplay.imageView_height)
        #  2) connect
        self.display_2ConnectChange(self.quizMentalDisplay) 
        #  3) start the thread
        self.threadFaceTitle.start()
        self.quizMentalDisplay.displayInt()

        self.quizMentalDisplay.quiz1_CreatePreView("start")
        self.threadFaceTitle._started_signal.connect(self.display_QuizMental_slot)


    #  쓰레드 시작하는 동안 화면 전환시 대기 메시지 필요함.
    def display_QuizMental_slot(self):
        self.threadFaceTitle._started_signal.disconnect()
        # self.quizMentalDisplay.quiz3_ReadyCount_Start()
        QTimer.singleShot(DISPLAY_CHANGE_DELAY, self.quizMentalDisplay.quiz3_ReadyCount_Start )

    
    ###########################################################################
    def display_QuizMentalEnd(self):
        if PROJ_CONTROL:
            self.threadScheduler.sch_quiz_progress_set = False

        # stop() 시 화면에 기존 이미지가 보여 지는 것을 방지 : stop 중에도 신호가 발생
        # self.threadFaceTitle.change_pixmap_signal.disconnect()
        # self.threadFaceTitle.foreheadxy_angle_signal.disconnect()
        self.all_disconnect()

        self.quizMentalDisplay.mentalGView.hide()
        self.quizMentalDisplay.lb_imageView.clear()
        self.quizMentalDisplay.quiz1_CreatePreView("end")


        app.processEvents() # 대기 중인 이벤트를 처리하고 반환합니다. 이를 통해 화면이 갱신되기를 기다릴 수 있습니다.
        self.threadFaceTitle.stop()
        print('thread FaceTitle : STOP')

        #  1) create the video capture thread
        self.threadVideo = ThreadVideo( self.imageView_width, self.imageView_height )
        #  3) start the threadtimer_timeout
        self.threadVideo._started_signal.connect(self.display_QuizMentalEnd_slot)
        self.threadVideo.start()        # < 숨기고, 지운 화면이 간헐적으로 보이는 부분 >
        print('thread Video : START') 
        self.quizMentalDisplay.mentalGView.hide()   # 다시 한번 숨기고
        self.quizMentalDisplay.lb_imageView.clear() # 다시 한번 지우기

    def display_QuizMentalEnd_slot(self):
        self.quizMentalDisplay.quiz_in_progress = 'stop' # 'stop' : 중지, 'quiz_progress': 퀴즈중, 'quiz_end' 퀴즈 종료

        print('thread Video : Stared_signal')
        self.threadVideo._started_signal.disconnect()
        self.display_ConnectChange(self.quizEndDisplay, 5000, self.threadVideo.button_ok_create)
        self.quizEndDisplay.displayStart()    #  종료화면 표시 시간 타이머 시작


    ###########################################################################
    # 테스트 화면
    def display_QuizMentalTest(self):
        if PROJ_CONTROL:
            self.threadScheduler.sch_quiz_progress_set = True

        self.quizMentalDisplay.lb_imageView.clear()
        # self.quizMentalDisplay.quiz1_CreatePreView("얼굴 인식을 위한 영상처리 준비중 입니다.")

        app.processEvents() # 대기 중인 이벤트를 처리하고 반환합니다. 이를 통해 화면이 갱신되기를 기다릴 수 있습니다.
        self.threadVideo.stop()

        self.threadSound.sound_play_slot('music_stop')
        #  1) create the video capture thread
        self.threadFaceTitle = ThreadFaceTilt(self.quizMentalDisplay.imageView_width, self.quizMentalDisplay.imageView_height)
        #  2) connect
        self.display_2ConnectChange(self.quizMentalDisplay) 
        #  3) start the thread
        self.threadFaceTitle.start()
        self.quizMentalDisplay.displayInt()

        self.quizMentalDisplay.quiz1_CreatePreView("start")
        self.threadFaceTitle._started_signal.connect(self.display_QuizMentalTest_slot)

        if MENU_ANIMATION:
            QTimer.singleShot(1000, self.startWaitDisplay.animation_stop)
        else:
            QTimer.singleShot(1000, self.startWaitDisplay.change_chAnswerView_stop)

    def display_QuizMentalTest_slot(self):
        self.threadFaceTitle._started_signal.disconnect()
        self.quizMentalDisplay.quiz41_Init('test')
        self.quizMentalDisplay.quiz42_Next()
        self.quizMentalDisplay.lb_usrName.setText("QUIZ TEST")
    ###########################################################################

    ###########################################################################
    # 테트트 중지 : 대기화면으로 복귀
    def display_QuizMentalTestEnd(self):
        if PROJ_CONTROL:
            self.threadScheduler.sch_quiz_progress_set = False

        # stop() 시 화면에 기존 이미지가 보여 지는 것을 방지 : stop 중에도 신호가 발생
        # self.threadFaceTitle.change_pixmap_signal.disconnect()
        # self.threadFaceTitle.foreheadxy_angle_signal.disconnect()
        self.all_disconnect()

        self.quizMentalDisplay.mentalGView.hide()
        self.quizMentalDisplay.lb_imageView.clear()
        self.quizMentalDisplay.quiz1_CreatePreView("end")

        app.processEvents() # 대기 중인 이벤트를 처리하고 반환합니다. 이를 통해 화면이 갱신되기를 기다릴 수 있습니다.
        self.threadFaceTitle.stop()
        print('thread FaceTitle : STOP')

        #  1) create the video capture thread
        self.threadVideo = ThreadVideo( self.imageView_width, self.imageView_height )
        #  3) start the threadtimer_timeout
        self.threadVideo._started_signal.connect(self.display_QuizMentalTestEnd_slot)
        self.threadVideo.start()        # < 숨기고, 지운 화면이 간헐적으로 보이는 부분 >
        print('thread Video : START')
        self.quizMentalDisplay.mentalGView.hide()   # 다시 한번 숨기고
        self.quizMentalDisplay.lb_imageView.clear() # 다시 한번 지우기

        # 종료시 변경되어야 함. / 정상퀴즈에서는 time_out에서 이루어짐
        self.quizMentalDisplay.quiz_in_progress = None # None: 중지(미시작), True: 퀴즈중, False : 종료후 대기

    def display_QuizMentalTestEnd_slot(self):
        print('thread Video : Stared_signal')
        self.threadVideo._started_signal.disconnect()
        self.main_to_slot('quiz_start_wait')
    ###########################################################################
        
    ################################################################
    # self.threadVideo.
    # 디스플레이 전환(  화면이름, 키보드 지연시간, 키보드 생성)
    #                  self.- ,  ms          , self.threadVideo.-
    ################################################################
    def display_ConnectChange(self, _target, _delay_time, _target_button ):
        # **<경고|주의>반드시 기존의 signal-connect 를 disconnect 하지 않으면
        #   중복 반복 동작하는 문제 발생함.

        self.all_disconnect()

        # 버튼 바로 지우기
        self.threadVideo.button_clear()
        self.stack.setCurrentWidget(_target)
        QTimer.singleShot(DISPLAY_CHANGE_DELAY, lambda :self.display_ConnectChange_2(_target, _delay_time, _target_button))

    def display_ConnectChange_2(self, _target, _delay_time, _target_button):
        #  2) signal connect
        #    VIDEO SIGNAL
        self.threadVideo.change_pixmap_signal.connect(_target.update_image_slot)
        #     KEY SIGNAL
        self.threadVideo.key_one_signal.connect(_target.key_one_slot)
        self.threadVideo.key_repeat_signal.connect(_target.key_repeat_slot)
        # NEW : Finger SIGNAL
        self.threadVideo.finger_repeat_signal.connect(_target.finger_repeat_slot)
        self.threadVideo.hand_position_signal.connect(_target.hand_position_slot)

        #     FPS SIGNAL
        self.threadVideo.fps_signal.connect(_target.fps_signal_slot)
        #     SOUND SIGNAL
        _target.sound_play_signal.connect(self.threadSound.sound_play_slot)
        #     MENU GO TO SIGNAL
        _target.main_to_signal.connect(self.main_to_slot)

        # 일정시간후 키보드 보이기
        QTimer.singleShot( _delay_time, _target_button )

    ################################################################
    # self.threadFaceTitle.
    # 틸트 퀴즈 디스플레이 전환(  화면이름, 키)
    #         
    ################################################################
    def display_2ConnectChange(self, _target):
        # **<경고|주의>반드시 기존의 signal-connect 를 disconnect 하지 않으면
        #   중복 반복 동작하는 문제 발생함.
        self.all_disconnect()

        # 버튼 바로 지우기
        self.stack.setCurrentWidget(_target)
        QTimer.singleShot(DISPLAY_CHANGE_DELAY, lambda :self.display_2ConnectChange_2(_target))

    def display_2ConnectChange_2(self, _target):
        #  2) signal connect
        #    VIDEO SIGNAL
        self.threadFaceTitle.change_pixmap_signal.connect(_target.update_image_slot)
        #     KEY SIGNAL
        # self.threadVideo.key_one_signal.connect(_target.key_one_slot)
        # self.threadVideo.key_repeat_signal.connect(_target.key_repeat_slot)
        self.threadFaceTitle.foreheadxy_angle_signal.connect(_target.foreheadxy_angle_slot)
        #     FPS SIGNAL
        self.threadFaceTitle.fps_signal.connect(_target.fps_slot)
        #     SOUND SIGNAL
        _target.sound_play_signal.connect(self.threadSound.sound_play_slot)
        #     MENU GO TO SIGNAL
        _target.main_to_signal.connect(self.main_to_slot)


        # 일정시간후 키보드 보이기
        # QTimer.singleShot( _delay_time, _target_button )

    def all_disconnect(self):
        try: self.threadFaceTitle.change_pixmap_signal.disconnect()
        except: pass

        try: self.threadFaceTitle.foreheadxy_angle_signal.disconnect()
        except: pass
        try: self.threadFaceTitle.fps_signal.disconnect()
        except: pass
        try: self.threadFaceTitle.sound_play_signal.disconnect()
        except: pass
        try: self.threadFaceTitle.main_to_signal.disconnect()
        except: pass
        
        try: self.threadVideo.change_pixmap_signal.disconnect()
        except: pass
        try: self.threadVideo.key_one_signal.disconnect()
        except: pass
        try: self.threadVideo.key_repeat_signal.disconnect()
        except: pass
        try: self.threadVideo.fps_signal.disconnect()
        except: pass

        try: currentWidget = self.stack.currentWidget()
        except: pass
        try: currentWidget.sound_play_signal.disconnect()
        except: pass
        try: currentWidget.main_to_signal.disconnect()
        except: pass

        # 실시간Pixmap 잔상 방지를 위해서 change_pixmap_signal.disconnect 후 clear 함 
        self.startWaitDisplay.lb_imageView.clear()
        self.quizDisplay.lb_imageView.clear()
        self.quizMentalDisplay.lb_imageView.clear()
        self.quizEndDisplay.lb_imageView.clear()


    def closeEvent(self, event):
        stateIni_save()
        print(' > Thread stop...')
        try:
            self.threadVideo.stop()
            self.threadSound.stop()
            self.threadFaceTitle.stop()
        except AttributeError:
            pass
        event.accept()

    # @Slot(bool)
    # def daychange_slot(self, e):
    #     val.quiz_in_progress_date_change = True
    #     self.display_StartWait()

    @Slot(str)
    def main_to_slot(self, e):
        # print('val.quizMode : ', val.quizMode)
        print(f' < 0 >>> main_to_slot = {e}')

        
        ####################################################
        # MENU DISPLAY CHANGE
        ####################################################
        menu_items = ["user_reg", "quiz_start", "quiz_start_wait", "quiz_end", "quizMental_end"]

        if e == "user_reg":
            st_clear()          # 학생 정보 초기화
            st_state_clear()    # 학생 점수 초기화
            self.threadVideo.button_clear()
            QTimer.singleShot(1000, self.display_UserReg)
            # self.display_UserReg()
        
        elif e == "user_reg_scan":
            st_state_clear()    # 학생 점수 초기화
            self.threadVideo.button_clear()
            QTimer.singleShot(1000, self.display_UserReg_Scan)

        elif e == "user_reg_scan_repeat":
            self.display_UserReg_Scan_Repeat()

        elif e == "quiz_start":

            # [확인 보완이 필요함]
            ##############################################################
            # # QR scan -> select 경우 : 퀴즈 정보 다시 로드 하기 위함.
            if self.qr_select_quiz_num != None:
                val.quizFileNum = self.qr_select_quiz_num

            qArea, val.speedQuizTime, val.quizTitleImage, val.quizMode, val.quizOption1, val.quizOption2 = self.quizDisplay.xlsxQuizPreLoad.getQuizInfo(val.quizFileNum)
            # if val.speedQuizTime == 'None':     # str 영역
            #     val.speedQuizTime = SPEED_QUIZ_DEFAULT_TIME

            ##############################################################
            val.visitor_DayCount += 1   # 오늘 방문자 카운터 증가
            val.visitor_TotalCount += 1 # 전체 방문자 카운터
            
            self.qr_scan_available = False

            ##############################################################
            # 1) 멘탈 퀴즈
            if val.quizMode == 'mental arithmetic':
                st_state_clear()    # 학생 점수 초기화
                self.threadVideo.button_clear()
                QTimer.singleShot(1000, self.display_QuizMental)

            # 2) 단어 퀴즈
            elif val.quizMode == 'word quiz':
                st_state_clear()    # 학생 점수 초기화
                self.threadVideo.button_clear()
                QTimer.singleShot(1000, self.display_Quiz)

            # 3) 일반퀴즈  -> self.display_Quiz ->
            else:      # val.quizMode != 'mental arithmetic':
                print('@3')
                st_state_clear()    # 학생 점수 초기화
                self.threadVideo.button_clear()
                QTimer.singleShot(1000, self.display_Quiz)

            ##############################################################

        elif e == "quiz_start_wait":
            st_state_clear()    # 학생 점수 초기화
            self.threadVideo.button_clear()
            QTimer.singleShot(1000, self.display_StartWait)


        elif e == "quiz_end":
            self.threadVideo.button_clear()
            self.quizDisplay.sound_play_signal.emit('effectLoop_stop') # 틱톡 소리 중지
            self.quizDisplay.timerSpeedQ_stop()
            QTimer.singleShot(1000, self.display_QuizEnd)
            
        elif e == "quizMental_end":
            # self.quizMentalDisplay.sound_play_signal.emit('effectLoop_stop') # 틱톡 소리 중지
            self.quizMentalDisplay.timerSpeedQ_stop()
            QTimer.singleShot(1000, self.display_QuizMentalEnd)


        ####################################################
        # VIDEO THREAD MESSAGE
        # 터치 모드는 버튼을 threadVideo 에서 생성
        ####################################################
        elif e == 'button_choice1':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.button_clear()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.threadVideo.button_choice1_create)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg('touchMode'))
        elif e == 'button_choice2':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.button_clear()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.threadVideo.button_choice2_create)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg('touchMode'))
        elif e == 'button_choice3':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.button_clear()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.threadVideo.button_choice3_create)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg('touchMode'))
        elif e == 'button_choice4':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.button_clear()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.threadVideo.button_choice4_create)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg('touchMode'))
        elif e == 'button_choice5':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.button_clear()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.threadVideo.button_choice5_create)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg('touchMode'))
        elif e == 'button_ox':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.button_clear()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.threadVideo.button_ox_create)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg('touchMode'))
        
        elif e == 'button_clear':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.button_clear()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg(None))

        ###################################################
        # 손가락 인식모드 VIDEO THREAD MESSAGE
        #     손가락 카운트 모드는 m_quiz.py 에서 이미지 안내 표시 변경
        elif e == 'fingerCount1':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.input_fingerNone()
            # self.quizDisplay.FingerKeyTimer.reset()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.quizDisplay.FingerKeyTimer.reset)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.threadVideo.input_fingerCount(1))
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg('fingerCount1'))
        elif e == 'fingerCount2':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.input_fingerNone()
            # self.quizDisplay.FingerKeyTimer.reset()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.quizDisplay.FingerKeyTimer.reset)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.threadVideo.input_fingerCount(2))
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg('fingerCount2'))
        elif e == 'fingerCount3':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.input_fingerNone()
            # self.quizDisplay.FingerKeyTimer.reset()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.quizDisplay.FingerKeyTimer.reset)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.threadVideo.input_fingerCount(3))
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg('fingerCount3'))
        elif e == 'fingerCount4':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.input_fingerNone()
            # self.quizDisplay.FingerKeyTimer.reset()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.quizDisplay.FingerKeyTimer.reset)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.threadVideo.input_fingerCount(4))
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg('fingerCount4'))
        elif e == 'fingerCount5':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.input_fingerNone()
            # self.quizDisplay.FingerKeyTimer.reset()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.quizDisplay.FingerKeyTimer.reset)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.threadVideo.input_fingerCount(5))
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg('fingerCount5'))
        elif e == 'thumbUpDown':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.input_fingerNone()
            # self.quizDisplay.FingerKeyTimer.reset()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.quizDisplay.FingerKeyTimer.reset)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.threadVideo.input_thumbUpDown)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg('thumbUpDown'))
        elif e == 'touchMode':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.input_fingerNone()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.threadVideo.input_touchMode)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg('touchMode'))
        elif e == 'fingerNone':
            self.quizDisplay.viewInputModImg(None)
            self.threadVideo.input_fingerNone()
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, self.threadVideo.input_fingerNone)
            QTimer.singleShot(VIDEO_BTN_REFLASH_DELAY, lambda : self.quizDisplay.viewInputModImg(None))


        self.befor_menu = e

        ###### animaiton stop ###########################
        # 메뉴 전환시, 비활성화된 디스플레이 애니메이션 중지
        if e in menu_items:
            if self.e_menu_item != "quiz_start_wait":
                self.startWaitDisplay.rankingTableAllView_stop()
                if MENU_ANIMATION:
                    QTimer.singleShot(1000, self.startWaitDisplay.animation_stop)
                else:
                    QTimer.singleShot(1000, self.startWaitDisplay.change_chAnswerView_stop)

            elif self.e_menu_item != "quiz_end":
                self.quizEndDisplay.rankingTableAllView_stop()
                if MENU_ANIMATION:
                    QTimer.singleShot(1000, self.quizEndDisplay.animation_stop)
            self.e_menu_item = e
            print(f'before_menu_item = {e}')
        #################################################



    @Slot(list)
    def qrScanner_slot(self, scan_data):
        # ##### 중첩 함수 정의 #####
        def str_to_NoneOrStr( _str):
            if _str == '':
                return None
            else:
                return _str
        def str_to_NoneOrInt( _str):
            if _str == '':
                return None
            else:
                return int(_str)
            
        def userFindAdd():
            # ####### 등록 /조회 #######
            # 1. db 에서 검색
            val.st_id, val.st_school, val.st_grade, val.st_name = self.userRegDisplay.find_db_id(id_int)
            #   1-1. db 에 없으면
            if val.st_id == '':
                print('[SCAN ID] : db에 없음 -> DB 등록')
                # DB에 id 등록 / xlsx_id_load 정의됨

                if 'select:' in scan_data[SCAN_ETC]: etc = None 
                self.userRegDisplay.idLoad.db_create_User([id_int, school_str, grade_int, class_int, number_int, name_str, gender_str, etc])
                
                self.userRegDisplay.idLoad.conn.commit()    # 저장
                # 다시 조회
                val.st_id, val.st_school, val.st_grade, val.st_name = self.userRegDisplay.find_db_id(id_int)
            #   1-2. db 있으면
            else:
                print('[SCAN ID] : db에 있음')

        def selectQuizNum():
            # 퀴즈 번호 검사
            if 'select:' in etc_str:
                etc_list = scan_data[SCAN_ETC].split(':')
                # val.quizFileNum = int(etc_list[1])   # 퀴즈 번호
                self.qr_select_quiz_num = int(etc_list[1])
                print(f'퀴즈 번호 : etc_select_quiz_num = {self.qr_select_quiz_num}')
            else:
                self.qr_select_quiz_num = None
            
        def toRegMenu():
            self.userRegDisplay.timerkey_touch = True   # 입력 타이머 초기화
            # print(f'*** self.e_menu_item = {self.e_menu_item}')
            print('[data]', val.st_id, val.st_school, val.st_grade, val.st_name)
            if self.befor_menu in [None, 'quiz_start_wait', 'quiz_end']:
                self.main_to_slot('user_reg_scan')
            elif self.befor_menu in ['user_reg_scan', 'user_reg_scan_repeat']:
                self.main_to_slot('user_reg_scan_repeat')
            # 2. 추가/ 다시 도전 - 화면 전환
            # 3. 퀴즈 시작 준비

        # #### 클래스 함수 시작 #####
        if self.qr_scan_available == False:
            return
        
        print(f'str_list = {scan_data}')
        # str_list = ['add','1234','고실초','2','6','30','홍길순','남','테스트1']
        # id
        id_int = str_to_NoneOrInt(scan_data[SCAN_ID])
        # school
        school_str = str_to_NoneOrStr(scan_data[SCAN_SCHOOL])
        # grade
        grade_int = str_to_NoneOrInt(scan_data[SCAN_GRADE])
        # class
        class_int = str_to_NoneOrInt(scan_data[SCAN_CLASS])
        # number
        number_int = str_to_NoneOrInt(scan_data[SCAN_NUMBER])
        # name
        name_str = str_to_NoneOrStr(scan_data[SCAN_NAME])
        # gender
        gender_str = str_to_NoneOrStr(scan_data[SCAN_GENDER])
        # etc
        etc_str = str_to_NoneOrStr(scan_data[SCAN_ETC])

        if scan_data[SCAN_HEADER] == 'guest' or name_str =='guest':
            _mode = 'guest'
        elif scan_data[SCAN_HEADER] == 'add':
            _mode = 'add'
        elif scan_data[SCAN_HEADER] == 'del':
            _mode = 'del'
        else:
            _mode = None

        # [add] 모드
        if _mode == 'add':
            print('[QR ADD] Mode')

            # ####### 사용자 조회/등록 #######
            userFindAdd()
            # ####### 퀴즈 선택 검사 #######
            selectQuizNum()
            # ####### 메뉴(화면) 전환 #######
            toRegMenu()
        
        # [del] 삭제 모드
        elif _mode == 'del':
            print('[QR DEL] Mode')
            # 1. db 에서 검색
            # 2. db 에서 삭제, 랭킹에서 삭제
            # 3. 삭제 메시지 보여주기

        elif _mode == 'guest':
            print('[QR guest] Mode')
            val.st_id = '0000'
            val.st_school =''
            val.st_grade =''
            val.st_name ='손님'
            # ####### 퀴즈 선택 검사 #######
            selectQuizNum()
            # ####### 메뉴(화면) 전환 #######
            toRegMenu()


    def mainTimerStart(self):
        self.mainTimer = QTimer()
        self.mainTimer.setInterval(TIMER_MAIN_INTERVER)
        self.mainTimer.timeout.connect(self.mainTimer_timeout)
        self.mainTimer.start()


    def mainTimer_timeout(self):
        current_qdate = QDateTime.currentDateTime().date()

        if self.previous_qdate != current_qdate:
            val.quiz_in_progress_date_change = True
            self.display_StartWait()
            self.ranking_file_reset_ckeck()


        self.previous_qdate = current_qdate

    
    def ranking_file_reset_ckeck(self):
        # how_to_reset_ranking = 'everyday'
        # how_to_reset_ranking = 'month'
        print('val.how_to_reset_ranking = ', val.how_to_reset_ranking)

        # DATE
        # rank_file_lastDate = QDate(2024, 3, 1)
        rank_file_lastDate = self.quizEndDisplay.rankJsonRW.lastDate()
        print('[debug] rank_file_lastDate =', rank_file_lastDate)

        if rank_file_lastDate == None:
            return
        current_date = QDate.currentDate()

        # FILE NAME
        xlsFileName = os.path.splitext(val.quizFileList[val.quizFileNum])
        # current_filename = f'{RANKING_PATH}{xlsFileName[0]}{RANKING_POST_NAME}.{RANKING_FILE_Ecurrent_filenameXT}'
        current_filename = self.quizEndDisplay.rankJsonRW.rankFile

        print('[debug] current_filename = ', current_filename)
        # FILE NAME 확장
        ext_name = rank_file_lastDate.toString("yyyy-MM-dd")
        
        def ranking_backup(how):
            if not EXHIBITION_MODE:
                new_filename = f'{RANKING_PATH}{xlsFileName[0]}{RANKING_POST_NAME}_{how}_{ext_name}.{RANKING_FILE_EXT}'  # 랭킹 파일 이름 | 파일에서 확장자 구분하기  https://chancoding.tistory.com/182
                os.rename(current_filename, new_filename)
            else:
                new_filename = f'{RANKING_PATH}{xlsFileName[0]}{RANKING_EXHIBITION_POST_NAME}_{how}_{ext_name}.{RANKING_FILE_EXT}'  # 랭킹 파일 이름 | 파일에서 확장자 구분하기  https://chancoding.tistory.com/182
                os.rename(current_filename, new_filename)

        # 매일 변경하는 경우
        if val.how_to_reset_ranking == 'everyday' and rank_file_lastDate != current_date:
            ranking_backup('everyday')

        # 주 단위 변경의 경우
        elif 'week' in val.how_to_reset_ranking:
            week1, year1 = rank_file_lastDate.weekNumber()
            week2, year2 = current_date.weekNumber()
            if val.how_to_reset_ranking == '1week' and (week2 - week1 > 1):
                ranking_backup('1week')
            elif val.how_to_reset_ranking == '2week' and (week2 - week1 > 2):
                ranking_backup('2week')
            elif val.how_to_reset_ranking == '3week' and (week2 - week1 > 3):
                ranking_backup('3week')
            elif val.how_to_reset_ranking == '4week' and (week2 - week1 > 4):
                ranking_backup('4week')
            else:
                pass

        elif 'month' == val.how_to_reset_ranking:
            month1 = rank_file_lastDate.month(); year1 = rank_file_lastDate.year()
            month2 = current_date.month(); year2 = current_date.year()
            if (month1 != month2) or (year1 != year2):
                ranking_backup('month')



def msdelay(ms):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit) # msec
    loop.exec()

# class ConsoleOut:
#     def write(self, msg):
#         sys.__stdout__.write(msg)

#     def flush(self):
#         sys.__stdout__.flush()

# sys.stdout = ConsoleOut()

if __name__=="__main__":
    # PySide6Ui('ui_quiz.ui').toPy()
    # PySide6Ui('ui_start_wait.ui').toPy()
    # PySide6Ui('ui_quiz.ui').toPy()
    # PySide6Ui('ui_quiz_end.ui').toPy()

    app = QApplication(sys.argv)
    window = MyWidonws()
    window.show()
    sys.exit(app.exec())


    '''
    # ranking date 변화 
    app = QApplication(sys.argv)
    window = MyWidonws()
    window.mainTimer_timeout()
    '''

