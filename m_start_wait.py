# OpenCV(Python) + PyQt
#  https://blog.xcoda.net/104


'''
** How to display opencv video in pyqt apps **
    https://gist.github.com/docPhil99/ca4da12c9d6f29b9cea137b617c7b8b1 (기본)
    https://webnautes.tistory.com/1290 (보조)

    https://webnautes.tistory.com/1290
    https://blog.xcoda.net/104

Pyqt5와 OpenCV 연동시 주의점
    https://hagler.tistory.com/190


23.4.24 - 웹카메라 인식
'''


######################################
# 카메라 OpenCV -> QImage 로 뛰우기
######################################
from PySide6 import QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
import sys, os, fnmatch
import json

from PySide6.QtCore import *
import mediapipe as mp
import numpy as np
import math
from setup import *
from circular_progress import CircularProgress
from key_press_timer import Key3PressTimer

from ui_quiz_ranking import Ui_ranking_widget
from rank_widget import *

###############
from thread_video import *

## .ui -> .py ##
from pyside6_uic import PySide6Ui
from ui_start_wait import Ui_startWait
from ui_hand_finger import Ui_hand_widget

class StartWaitDisplay(QWidget, Ui_startWait, ThreadVideo):
    main_to_signal = Signal(str)
    sound_play_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Ui_quizView

        self.setWindowTitle("You Quiz?")
        self.fr_ranking.setStyleSheet('')

        # ############################################################################
        # https://www.geeksforgeeks.org/pyqt5-access-the-size-of-the-label/
        imageView_width, imageView_height = self.lb_imageView.size().width(), self.lb_imageView.size().height()
        print('frameView Size:',imageView_width, imageView_height)
        # ############################################################################

        # 타이틀1 그림자
        shadow1 = QGraphicsDropShadowEffect(self)
        shadow1.setBlurRadius(20)
        shadow1.setOffset(3)
        shadow1.setColor(Qt.black)
        self.lb_quizArea.setGraphicsEffect(shadow1)

        # 타이틀1 그림자
        # shadow2 = QGraphicsDropShadowEffect(self)
        # shadow2.setBlurRadius(5)
        # shadow2.setOffset(6)
        # shadow2.setColor(Qt.white)
        # self.lb_title2.setGraphicsEffect(shadow2)

        # shadow3 = QGraphicsDropShadowEffect(self)
        # shadow3.setBlurRadius(2)
        # shadow3.setOffset(1)
        # shadow3.setColor(Qt.white)
        # self.lb_chAnswer2.setGraphicsEffect(shadow3)

        self.lb_chAnswer.hide()
        self.lb_chAnswer_2.hide()

        # 손가락 아이콘 그림자
        shadow4 = QGraphicsDropShadowEffect(self)
        shadow4.setBlurRadius(2)
        shadow4.setOffset(1)
        shadow4.setColor(Qt.white)
        self.lb_hand_icon.setGraphicsEffect(shadow4)

        # self.fr_top.hide()

        # self.centeralwidget.hide()

        # 타이머 : 디스플레이 랭킹 표시  https://wikidocs.net/38522
        # self.timerRankingDisp = QTimer()
        # self.timerRankingDisp.setInterval(1000)
        # self.timerRankingDisp.timeout.connect(self.dispRanking)
        # self.timerRankingDisp.start()

        if QUIZ_TYPE == 'speed':
            # self.lb_type2.setText('퀴즈 유형: ' + '스피드 퀴즈')
            self.lb_type2.setText('스피드 퀴즈')

        elif QUIZ_TYPE == 'golden':
            # self.lb_type2.setText('퀴즈 유형: ' + '골든벨 퀴즈')
            self.lb_type2.setText('골든벨 퀴즈')

            
        '''    
        # self.lb_timeView.setText(QTime.fromString(val.speedQuizTime, 'm:s').toString('mm:ss'))
        print('>> ', val.speedQuizTime)
        self.lb_timeView.setText(QTime.fromString('5:59', 'm:s').toString('mm:ss'))


        ###### Title image ########
        # self.lb_title_img = QLabel()
        self.lb_title_img.move(IMG_TITLE_XY[0], IMG_TITLE_XY[1])
        pixmap_title = QPixmap(f"{IMG_PATH}{IMG_TITLE_FILE}")
        # pixmap 종횡비
        # https://bskyvision.com/entry/pyside-keepaspectratio
        # pixmap_title.scaled(QSiz(200, 100), aspectMode=Qt.KeepAspectRatioByExpanding)
        pixmap_title = pixmap_title.scaled(IMG_TITLE_SIZE, IMG_TITLE_SIZE,  Qt.KeepAspectRatio)
        self.lb_title_img.resize(IMG_TITLE_SIZE, IMG_TITLE_SIZE)
        self.lb_title_img.setPixmap(pixmap_title)
        # self.lb_title_img.setText('TITLE')
        '''
        # ###### 퀴즈 모드 이미지 ######
        self.lb_mode_img.setScaledContents(False)   # False 상태에서, 스케일 동작함.
        if EXHIBITION_MODE:
            pixmap_mode = QPixmap(f'{IMG_PATH}{IMG_MODE_EXHIBITION}')
        else:
            pixmap_mode = QPixmap(f'{IMG_PATH}{IMG_MODE_SCHOOL}')
        pixmap_mode = pixmap_mode.scaled(self.lb_mode_img.size().width(), self.lb_mode_img.size().height(), Qt.KeepAspectRatio) 
        self.lb_mode_img.setPixmap(pixmap_mode)

        # https://stackoverflow.com/questions/13119534/resize-images-inside-qt-label
        # 캐릭터 아이콘
        self.lb_face_icon.setScaledContents(False)   # False 상태에서, 스케일 동작함.
        pixmap1 = QPixmap(f'{IMG_PATH}{IMG_FACE_FILE}')
        pixmap1 = pixmap1.scaled(self.lb_face_icon.size().width(), self.lb_face_icon.size().height(), Qt.KeepAspectRatio) 
        self.lb_face_icon.move(IMG_FACE_FILE_XY[0], IMG_FACE_FILE_XY[1])
        self.lb_face_icon.resize(IMG_FACE_FILE_SIZE, IMG_FACE_FILE_SIZE)
        self.lb_face_icon.setPixmap(pixmap1)
        
        # 손가락 아이콘
        self.lb_hand_icon.setScaledContents(False)   # False 상태에서, 스케일 동작함.
        pixmap2 = QPixmap(f'{IMG_PATH}{IMG_HAND_FILE}')
        pixmap2= pixmap2.scaled(self.lb_hand_icon.size().width(), self.lb_hand_icon.size().height(), Qt.KeepAspectRatio) 
        self.lb_hand_icon.setPixmap(pixmap2)

        ##### 버전 정보 표시 #####
        try:
            self.lb_verInfo.setText( f'프로그램 {PROGRAM_VER}  |  퀴즈 {QUIZ_VER}  |  Program developer : {PROGRAM_DEVELOPER}')
        except:
            pass

        self.lb_cmdMsg.setText('')
        self.lb_visitorTotalCount.setText('')   # 누적 방문자
        self.lb_visitorCount.setText('')        # 오늘 방문자

        # 구 버전 랭킹표시 부분
        # self.sence = 0      # 초기값
        # self.moveVal = 10
        # self.sec = 1
        
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
        self.progress.text = 'START'

        # Center CircularProgress
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.progress)
        self.center_progress.setLayout(self.vlayout)

        ## Key Press Timer 생성 ( timer: 2000ms)
        self.progress.hide()
        self.startPressKeyTimer = Key3PressTimer(KEY3_TIMER_INTERVAL, KEY3_PUSH_TIME, KEY3_VIEW_DELAY, self.progress)

        # 퀴즈 영역
        self.lb_quizArea.hide()
        #################################################################################
        # 랭킹 테이블 위젯 초기화
        # #   테이블 지정 : self.tbw_ranking
        # self.rankingTableView = RankingTableView(self.tbw_ranking)

        # # 자신의 랭킹 보기
        # self.rankingTableView.RankAllView()

        

        #################################################################################
        # 하단 안내메시지 파일 로딩 self.lb_chAnswer
        # try:
        #     with open(f'{CONFIG_PATH}{MSG_FILE_QUIZ_WIAT}', 'r', encoding='utf-8') as file:
        #         txt = file.read()
        #         self.lb_chAnswer.setText(txt)
        # except FileNotFoundError:
        #     pass
        #################################################################################
        files = os.listdir(f'{CONFIG_PATH}')
        message_quiz_wait_files = [i for i in files if fnmatch.fnmatch(i, f'{MSG_FILE_QUIZ_WIAT}')]
        print('message_quiz_wait_files = ', message_quiz_wait_files)

        self.message_quiz_wait_count = 0
        self.message_quiz_wait_data = []
        try:
            for file_name in message_quiz_wait_files:
                with open(f'{CONFIG_PATH}{file_name}', 'r', encoding='utf-8') as fileread:
                    txt = fileread.read()
                    # self.lb_chAnswer.setText(txt)
                    self.message_quiz_wait_data.append(txt)
        except FileNotFoundError:
            print("'message_quiz_wait*.html' 파일을 찾을 수 없음.")

        if len(self.message_quiz_wait_data) > 0:
            self.labelTextChange(self.lb_chAnswer, self.message_quiz_wait_data)

        # icon face 표시
        
        # # NEW
        self.createRankWidget()
        self.change_chAnswerView_init()

        ## new
        # https://stackoverflow.com/questions/25438616/pyqt-not-recognizing-arrow-keys

        # 터치 연속 입력 제한
        self.key_repeat_ready = True


    def displayStart(self):
        if MENU_ANIMATION:
            self.animation_start()
        else:
            self.change_chAnswerView_start()
        self.key_repeat_ready = True


    def rankingTableAllView(self):
        # self.rankingTableView.RankAllView()
        self.rankView.rankingTableView.RankAllView()
        self.rankView.show()
    
    def rankingTableAllView_stop(self):
        # self.rankingTableView.tabletimer_stop()
        self.rankView.rankingTableView.tabletimer_stop()
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
        # self.thread.stop()
        event.accept()

    ########################################################################################
    def labelTextChange(self, _label, _list):
        _label.setText(_list[self.message_quiz_wait_count])
        self.message_quiz_wait_count +=1
        if self.message_quiz_wait_count > len(_list) -1:
            self.message_quiz_wait_count = 0

    ########################################################################################
    def change_chAnswerView_init(self):
        self.chAnswerTimer = QTimer()
        self.chAnswerTimer.setInterval(MENU_INFO_TIME)
        self.chAnswerTimer.timeout.connect(self.chAnswerTimer_timeout)

    def change_chAnswerView_start(self):
        if len(self.message_quiz_wait_data) > 0:
            self.lb_chAnswer.show()
            self.lb_chAnswer_2.hide()
            self.chAnswerTimer.start()

    def chAnswerTimer_timeout(self):
        self.labelTextChange(self.lb_chAnswer, self.message_quiz_wait_data)
        print('chAnswerView 화면 전환 ')

    def change_chAnswerView_stop(self):
        print('chAnswerView 화면 중지 ')
        if len(self.message_quiz_wait_data) > 0:
            self.chAnswerTimer.stop()
    ########################################################################################
   
    '''
    #############################################################################################
    '''
    # 애니메이션 효과
    #   https://www.pythonguis.com/tutorials/qpropertyanimation/
    #   https://zetcode.com/pyqt/qpropertyanimation/
    #   https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QGraphicsItemAnimation.html
    #   https://www.pythonguis.com/tutorials/qpropertyanimation/

    #   https://zetcode.com/pyqt/qpropertyanimation/
    #   https://doc.qt.io/qt-6/qeasingcurve.html


    def animation_start(self):
        if len(self.message_quiz_wait_data) > 0:
            self.start_wait_ani_fg = True
            self.lb_chAnswer.show()
            self.lb_chAnswer_2.show()
            self.ani_rankView()
            self.ani_titleView(30, 30)
            self.ani_chAnswerView(20, 790)
            # self.chAnswerView = ChAnswerView(self.lb_chAnswer, 20, 790)

        print(" StartWiatDisplay | animation_start")

    def animation_stop(self):
        if len(self.message_quiz_wait_data) > 0:
            try:
                self.ani_title.finished.disconnect()
                self.ani_chAnser_group2.finished.disconnect()
                self.ani_chAnser_group4.finished.disconnect()
            except Exception as e:
                print(f'[ERR 5 animation_stop] : {e}')
            self.start_wait_ani_fg = False
            print(" StartWiatDisplay | animation_stop")
            
        
            
    ########################################################################################
    # https://stackoverflow.com/questions/50640196/pyqt5-qpropertyanimation-finished-how-to-connect
    

    def ani_rankView(self):
        self.rankView.move(451, 0)
        self.anim = QPropertyAnimation(self.rankView, b"pos")
        self.anim.setStartValue(QPoint(451,0))
        self.anim.setEndValue(QPoint(0,0))
        self.anim.setDuration(3000)
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        # QTimer.singleShot(1000, lambda :self.anim.start )
        self.anim.start()

    def ani_titleView(self, _x, _y):
        self.ani_title = QPropertyAnimation(self.lb_title_img, b"pos")
        self.ani_down_title(_x, _y)
    
    ##################################################################################
    def ani_down_title(self, _x, _y):
        if self.start_wait_ani_fg:
            self.lb_challenge.hide()
            self.ani_title.setStartValue(QPoint(IMG_TITLE_XY[0], IMG_TITLE_XY[1]))
            self.ani_title.setEndValue(QPoint(IMG_TITLE_XY[0]+_x, IMG_TITLE_XY[1]+_y))
            self.ani_title.setDuration(2000)
            self.ani_title.setEasingCurve(QEasingCurve.OutBounce)
            try:
                self.ani_title.finished.disconnect()
            except Exception as e:
                print(f'[ERR ani_down_title] : {e}')
            self.ani_title.finished.connect(lambda: self.ani_up_title(_x, _y))
            QTimer.singleShot(500, self.ani_title.start )
            # self.anim1.start()

    def ani_up_title(self, _x, _y):
        if self.start_wait_ani_fg:
            self.lb_challenge.show()
            self.ani_title.setStartValue(QPoint(IMG_TITLE_XY[0]+_x, IMG_TITLE_XY[1]+_y))
            self.ani_title.setEndValue(QPoint(IMG_TITLE_XY[0], IMG_TITLE_XY[1]))
            self.ani_title.setDuration(2000)
            self.ani_title.setEasingCurve(QEasingCurve.InOutBack)
            try:
                self.ani_title.finished.disconnect()
            except Exception as e:
                print(f'[ERR ani_up_title] : {e}')
            self.ani_title.finished.connect(lambda: self.ani_down_title(_x, _y))
            QTimer.singleShot(500, self.ani_title.start )
            # self.anim2.start()

    ##################################################################################

    def ani_chAnswerView(self, _x, _y):    
        if self.start_wait_ani_fg:    
            self.lb_chAnswer.move(_x, _y)
            self.ani_pos_chAnser = QPropertyAnimation(self.lb_chAnswer, b"pos")
            effect = QGraphicsOpacityEffect(self.lb_chAnswer)
            self.lb_chAnswer.setGraphicsEffect(effect)
            self.ani_opa_chAnser = QPropertyAnimation(effect, b"opacity")

            self.lb_chAnswer_2.move(_x, _y)
            self.ani_pos_chAnser_2 = QPropertyAnimation(self.lb_chAnswer_2, b"pos")
            effect_2 = QGraphicsOpacityEffect(self.lb_chAnswer_2)
            self.lb_chAnswer_2.setGraphicsEffect(effect_2)
            self.ani_opa_chAnser_2 = QPropertyAnimation(effect_2, b"opacity")

            self.pos_p0= [_x, _y - 118] # 20, 672
            self.pos_p1= [_x, _y] # 20, 790
            self.pos_p2= [_x, _y + 118] # 20, 908
    
            self.ani_chAnswer_duration = 1000
            self.ani_chAnswer_interval = 200
            self.ani_chAnswer_show1_time = MENU_INFO_TIME
            self.ani_chAnswer_show2_time = MENU_INFO_TIME

            self.ani_down1hide_chAnswerView()

    def ani_down1hide_chAnswerView(self):
        if self.start_wait_ani_fg:
            # print('1')
            # message 2 hide
            self.ani_pos_chAnser_2.setStartValue(QPoint(self.pos_p1[0], self.pos_p1[1]))
            self.ani_pos_chAnser_2.setEndValue(QPoint(self.pos_p2[0], self.pos_p2[1]))
            self.ani_pos_chAnser_2.setDuration(self.ani_chAnswer_duration )
            self.ani_pos_chAnser_2.setEasingCurve(QEasingCurve.OutCubic)

            self.ani_opa_chAnser_2.setStartValue(1.0)
            self.ani_opa_chAnser_2.setEndValue(0.0)
            self.ani_opa_chAnser_2.setDuration(self.ani_chAnswer_duration/2)
            
            try:
                del self.ani_chAnser_group1
            except Exception as e:
                # print(f'[ERR 1] : {e}')
                pass
            self.ani_chAnser_group1 = QParallelAnimationGroup()
            self.ani_chAnser_group1.addAnimation(self.ani_pos_chAnser_2)
            self.ani_chAnser_group1.addAnimation(self.ani_opa_chAnser_2)
            self.ani_chAnser_group1.start()                                 # 즉시 hide 2

            QTimer.singleShot(self.ani_chAnswer_interval, self.ani_down1show_chAnswerView)         # hide 후 500ms 지연

    def ani_down1show_chAnswerView(self):
        if self.start_wait_ani_fg:
            self.labelTextChange(self.lb_chAnswer_2, self.message_quiz_wait_data)
            # print('2')
            # message1 show
            self.ani_pos_chAnser.setStartValue(QPoint(self.pos_p0[0], self.pos_p0[1]))
            self.ani_pos_chAnser.setEndValue(QPoint(self.pos_p1[0], self.pos_p1[1]))
            self.ani_pos_chAnser.setDuration(self.ani_chAnswer_duration )
            self.ani_pos_chAnser.setEasingCurve(QEasingCurve.OutCubic)

            self.ani_opa_chAnser.setStartValue(0.0)
            self.ani_opa_chAnser.setEndValue(1.0)
            self.ani_opa_chAnser.setDuration(self.ani_chAnswer_duration/2)

            try:
                # del self.ani_pos_chAnser_group2
                self.ani_chAnser_group2.finished.disconnect()
            except Exception as e:
                # print(f'[ERR 2] : {e}')
                pass
            self.ani_chAnser_group2 = QParallelAnimationGroup()         # New 정의되므로 기존 connecnt는 삭제됨
            self.ani_chAnser_group2.addAnimation(self.ani_pos_chAnser)
            self.ani_chAnser_group2.addAnimation(self.ani_opa_chAnser)
            self.ani_chAnser_group2.start()                                 # 즉시 show 1
            self.ani_chAnser_group2.finished.connect(self.ani_down1show_chAnswerView_delay)
    def ani_down1show_chAnswerView_delay(self):
        QTimer.singleShot(self.ani_chAnswer_show1_time, self.ani_down2hide_chAnswerView)  # show 되는 시간 시간

    def ani_down2hide_chAnswerView(self):
        if self.start_wait_ani_fg:
            # print('3')
            # message1 hide
            self.ani_pos_chAnser.setStartValue(QPoint(self.pos_p1[0], self.pos_p1[1])) 
            self.ani_pos_chAnser.setEndValue(QPoint(self.pos_p2[0], self.pos_p2[1])) 
            self.ani_pos_chAnser.setDuration(self.ani_chAnswer_duration )
            self.ani_pos_chAnser.setEasingCurve(QEasingCurve.OutCubic)

            self.ani_opa_chAnser.setStartValue(1.0)
            self.ani_opa_chAnser.setEndValue(0.0)
            self.ani_opa_chAnser.setDuration(self.ani_chAnswer_duration/2)

            try:
                del self.ani_chAnser_group3
            except Exception as e:
                # print(f'[ERR 3] : {e}')
                pass
            self.ani_chAnser_group3 = QParallelAnimationGroup()
            self.ani_chAnser_group3.addAnimation(self.ani_pos_chAnser)
            self.ani_chAnser_group3.addAnimation(self.ani_opa_chAnser)
            self.ani_chAnser_group3.start()                                 # 즉시 hide  1

            QTimer.singleShot(self.ani_chAnswer_interval, self.ani_down2show_chAnswerView)         # hide 후 500ms 지연

    def ani_down2show_chAnswerView(self):
        if self.start_wait_ani_fg:
            self.labelTextChange(self.lb_chAnswer, self.message_quiz_wait_data)
            # print('4')
            # message2 show
            self.ani_pos_chAnser_2.setStartValue(QPoint(self.pos_p0[0], self.pos_p0[1])) 
            self.ani_pos_chAnser_2.setEndValue(QPoint(self.pos_p1[0], self.pos_p1[1]))      # 1/2 908, 2/2 1026
            self.ani_pos_chAnser_2.setDuration(self.ani_chAnswer_duration )
            self.ani_pos_chAnser_2.setEasingCurve(QEasingCurve.OutCubic)

            self.ani_opa_chAnser_2.setStartValue(0.0)
            self.ani_opa_chAnser_2.setEndValue(1.0)
            self.ani_opa_chAnser_2.setDuration(self.ani_chAnswer_duration/2)

            try:
                # del self.ani_pos_chAnser_group4
                self.ani_chAnser_group4.finished.disconnect()
            except Exception as e:
                # print(f'[ERR 4] : {e}')
                pass
            self.ani_chAnser_group4 = QParallelAnimationGroup()         # New 정의되므로 기존 connecnt는 삭제됨
            self.ani_chAnser_group4.addAnimation(self.ani_pos_chAnser_2)
            self.ani_chAnser_group4.addAnimation(self.ani_opa_chAnser_2)
            self.ani_chAnser_group4.start()                             
            self.ani_chAnser_group4.finished.connect(self.ani_down2show_chAnswerView_delay)
    def ani_down2show_chAnswerView_delay(self):
        QTimer.singleShot(self.ani_chAnswer_show2_time, self.ani_down1hide_chAnswerView)  # hide 보여지는 시간

    
    
    ##################################################################################



    '''
    #############################################################################################
    '''
    @Slot(np.ndarray)
    def update_image_slot(self, qt_img):

        """ X:주의 슬롯에 넣으면, 처리 못함.가상 키보드 """
        # self.vr_keyboard(cv_img)

        """Updates the image_label with a new opencv image"""
        # qt_img = self.convert_cv2qt(cv_img) -> thread 에서 처리하는 것으로 변경함.
        self.lb_imageView.setPixmap(qt_img)

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

        if key == "START":
            keyState = True
        else:
            keyState = False

        # 누르는 시간(KEY3_PUSH_TIME)을 넘는 경우
        if self.startPressKeyTimer.state(keyState):
            self.sound_play_signal.emit("START")
            self.main_to_signal.emit("user_reg")    # 메인 에 신호를 보낸다.
            # 환영 시작 사운드 재생
            # print('START')

            # 터치 연속 입력 제한
            self.key_repeat_ready = False
            

    @Slot(str)
    def key_one_slot(self, one_key):
        pass
        # self.sounds[self.soundDict[touchkey]].play()    # video_thread > 현재.py 에서 재생
    
    @Slot(str)
    def fps_signal_slot(self, fps_str):
        self.lb_fps.setText(fps_str)

    # # thread_sound to signal
    @Slot(str)
    def music_play_slot(self, cmd):
        self.lb_cmdMsg.setText(f'{cmd}')

    # # thread_scheduler to signal
    @Slot(str)
    def scheduer_Msg_slot(self, msg):
        self.lb_cmdMsg.setText(f'{msg}')

def msdelay(ms):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit) # msec
    loop.exec()





if __name__=="__main__":
    PySide6Ui('ui_start_wait.ui').toPy()

    app = QApplication(sys.argv)
    a = StartWaitDisplay()
    a.show()
    a.animation_start()
    sys.exit(app.exec())