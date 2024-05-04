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
import sys

from PySide6.QtCore import *
import mediapipe as mp
import numpy as np

# import pandas as pd

###############
from thread_video import *

from setup import *
from circular_progress import CircularProgress
from key_press_timer import Key3PressTimer

# 학생 id 화일 읽어 오기
from xlsx_id_load import *

## .ui -> .py ##
from pyside6_uic import PySide6Ui
from ui_user_reg import Ui_user_reg

import val

# #########################################################################


class UserRegDisplay(QWidget, Ui_user_reg, ThreadVideo):

    sound_play_signal = Signal(str)
    main_to_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Ui_quizView

        self.setWindowTitle("사용자 등록")

        # https://www.geeksforgeeks.org/pyqt5-access-the-size-of-the-label/
        imageView_width, imageView_height = self.lb_imageView.size().width(), self.lb_imageView.size().height()
        print('frameView Size:',imageView_width, imageView_height)

        shadow1 = QGraphicsDropShadowEffect(self)
        shadow1.setBlurRadius(2)
        shadow1.setOffset(2)
        shadow1.setColor(Qt.gray)
        self.label.setGraphicsEffect(shadow1)

        shadow2 = QGraphicsDropShadowEffect(self)
        shadow2.setBlurRadius(5)
        shadow2.setOffset(2)
        shadow2.setColor(Qt.white)
        self.lb_msg.setGraphicsEffect(shadow2)

        self.lb_id.setText('')
        self.lb_name.setText('손님')

        ##### 버전 정보 표시 #####
        try:
            self.lb_verInfo.setText( f'프로그램 {PROGRAM_VER}  |  퀴즈 {QUIZ_VER}  |  Program developer : {PROGRAM_DEVELOPER}')
        except:
            pass

        # Create Circular Progress
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

        if RANKING_EXHIBITION_MODE:
            self.lb_school.setText('')
            self.lb_school.show()
            self.lb_grade.setText('')
            self.lb_grade.show()
        else:
            self.lb_school.hide()
            self.lb_grade.hide()

        # Center CircularProgress
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.progress)
        self.center_progress.setLayout(self.vlayout)

        ## Key Pess timer 생성 (Timer :2000ms)
        self.keyOld = ''
        self.progress.hide()
        self.quitPressKeyTimer = Key3PressTimer(KEY3_TIMER_INTERVAL, KEY3_PUSH_TIME, KEY3_VIEW_DELAY, self.progress)
        self.okPressKeyTimer = Key3PressTimer(KEY3_TIMER_INTERVAL, KEY3_PUSH_TIME, KEY3_VIEW_DELAY, self.progress)

        self.timerkey_touch = False     # REG_KEY_TIME_OUT
        
        #################################################################################
        self.idLoad = IdLoad()
        self.idLoad.init()

        #################################################################################
        # 하단 안내메시지 파일 로딩 self.lb_chAnswer
        try:
            with open(f'{CONFIG_PATH}{MSG_FILE_USER_SEARCH}', 'r', encoding='utf-8') as file:
                txt = file.read()
                self.lb_msg.setText(txt)
        except FileNotFoundError:
            pass

        # 터치 연속 입력 제한
        #  지정하지 않으면 emit가 연속으로 발생
        #     -> main_to_slot() 신호가 계속 발생, connect 가 중복, 반복실행 결과가 나옴
        #     xls 파일 2회 검사 로딩시, 느린 응답의 경우 발생함
        self.key_repeat_ready = True    
    

    ###########################################################################
    def timerKeyTouch_start(self):
        # 입력시간 타이머
        self.timerkey = QTimer()
        self.timerkey_rem = QTime.fromString(REG_KEY_TIME_OUT, 'ss')
        self.timerkey.setInterval(QTIMER_INTERVAL)
        self.timerkey.timeout.connect(self.timerKeyTouch_timeout)
        self.timerkey.start()

        self.lb_keytime.setText(f'입력대기: {self.timerkey_rem.toString("ss") } 초')
        self.key_repeat_ready = True
        
    
    def timerKeyTouch_stop(self):
        self.timerkey.stop()

    def timerKeyTouch_timeout(self):
        if self.timerkey_touch == True:     # REG_KEY_TIME_OUT
            self.timerkey_touch = False
            self.timerkey_rem = QTime.fromString(REG_KEY_TIME_OUT, 'ss')

        else:
            self.timerkey_rem = self.timerkey_rem.addMSecs(-QTIMER_INTERVAL)
            self.lb_keytime.setText(f'입력대기: {self.timerkey_rem.toString("ss") } 초')

            timeOverChk = ( self.timerkey_rem.__eq__(QTime.fromString('00', 'ss')) or
                self.timerkey_rem.__ge__(QTime.fromString(REG_KEY_TIME_OUT, 'ss')) )

            if timeOverChk :
                self.timerkey.stop()
                self.main_to_signal.emit('quiz_start_wait')

    ###########################################################################

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()


    @Slot(np.ndarray)
    def update_image_slot(self, qt_img):

        """ X:주의 슬롯에 넣으면, 처리 못함.가상 키보드 """
        # self.vr_keyboard(cv_img)

        """Updates the image_label with a new opencv image"""
        # qt_img = self.convert_cv2qt(cv_img) -> thread 에서 처리하는 것으로 변경함.
        self.lb_imageView.setPixmap(qt_img)
    

    @Slot(str)
    def key_one_slot(self, key):
        self.timerkey_touch = True      # REG_KEY_TIME_OUT
        if key == "OK" or key == "QUIT":
            return
        # delete key
        if key == '<-':
            a = self.lb_id.text()
            if len(a) > 0:
                a = a[:-1]
                self.lb_id.setText(a)   # 삭제되면 id,name 검색이 않되는 문제가 있음.
                key =''
            elif len(a) == 0:
                return
            
        # 학번 최대자릿수 검사
        if len(self.lb_id.text()) + 1 > STUDENT_ID_MAX:   # key+ 되기 전 검사
            return

        # Sound play & 숫자 입력
        if not key in PRESS_KEY_DELAY_LIST:
            print('SOUND PLAY :', key)
            self.sound_play_signal.emit(key)
            id_str = self.lb_id.text()+key  # 문자열 더하기
            self.lb_id.setText(self.lb_id.text()+key)
            
        # id, name 검색 -> 모듈 변수에 저장
        if RANKING_EXHIBITION_MODE:
            # 전시관 모드
            # db 에서 검색
            val.st_id, val.st_school, val.st_grade, val.st_name = self.find_db_id(id_str)

        else:
            # 일반모드
            #    self.xlsxIdLoad.id_dicLis 에서 검색
            val.st_id, val.st_school, val.st_grade, val.st_name = self.find_id(id_str)
        
        # GUI 화면에 표시
        self.lb_id.setText(id_str)
        self.lb_school.setText(val.st_school)
        if val.st_grade == "":
            self.lb_grade.setText(f'')
        else:
            self.lb_grade.setText(f'{val.st_grade}학년')
        self.lb_name.setText(val.st_name)

    def find_db_id(self, id_str):
        ret = []
        if id_str != "":
            ret = self.idLoad.db_find_UserID(int(id_str))

        print(f' DB ret = {ret}')
        if len(ret) != 0:
            find_id = str(ret[TO_ID])
            find_school = ret[TO_SCHOOL]
            find_grade = str(ret[TO_GRADE])
            find_name = ret[TO_NAME]
        else:
            find_id = ''
            find_name = '손님'
            find_school = ''
            find_grade = ''

        return find_id, find_school, find_grade, find_name


    def find_id(self, id_str):
        if id_str in self.idLoad.id_dicList:
            name = self.idLoad.id_dicList[id_str][TO_NAME-1]

            #1) name 원하는 위치 문자 변경 https://gbjeong96.tistory.com/25
            name = list(name)
            name[1] = "*"
            find_id = id_str
            find_name =''.join(name)

            #2) school, grade
            find_school = self.idLoad.id_dicList[id_str][TO_SCHOOL-1]
            find_grade = self.idLoad.id_dicList[id_str][TO_GRADE-1]
        else:
            find_id = ''
            find_name = '손님'
            find_school = ''
            find_grade = ''
        return find_id, find_school, find_grade, find_name

    @Slot(str)
    def finger_repeat_slot(self, finger):
        pass

    @Slot(list)
    def hand_position_slot(self, dataList):
        pass
    
    @Slot(str)
    def key_repeat_slot(self, key):     # None, QUIT, OK
        if self.key_repeat_ready == False:
            return

        if not (key == 'OK' or key == 'QUIT'):
            return
        if self.keyOld == key:
            self.timerkey_touch = True  # REG_KEY_TIME_OUT

            # Quit 부분은 구현하지 않음, 확인 필요함.
            if key == 'QUIT':
                keyState = True
            else:
                keyState = False
            
            if self.quitPressKeyTimer.state(keyState):
                self.sound_play_signal.emit("QUIT")
                self.main_to_signal.emit("main")    # 메인에 신호를 보낸다.
                self.timerKeyTouch_stop()           # REG_KEY_TIME_OUT
            
            if key == 'OK':
                keyState = True
            else:
                keyState = False
            
            if self.okPressKeyTimer.state(keyState):
                self.sound_play_signal.emit("OK")
                print('*** ok')
                self.main_to_signal.emit("quiz_start")  # 메인에 신호를 보낸다.
                self.timerKeyTouch_stop()               # REG_KEY_TIME_OUT
                self.key_repeat_ready = False

                
        else:
            self.quitPressKeyTimer.timeEnd()
            self.okPressKeyTimer.timeEnd()

        self.keyOld = key
        

    @Slot(str)
    def fps_signal_slot(self, fps_str):
        self.lb_fps.setText(fps_str)
        
############################################################################3
if __name__=="__main__":
    from _main import *
    PySide6Ui('ui_user_reg.ui').toPy()

    app = QApplication(sys.argv)
    a = MyWidonws()
    a.display_UserReg()   # main 에서 실행후 , 다시 실행하면 2번 emit 동작을 함.
    QTimer.singleShot(500, a.threadVideo.button_clear)
    QTimer.singleShot(2500, a.threadVideo.button_user_create)

    a.show()
    sys.exit(app.exec())