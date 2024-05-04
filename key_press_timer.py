
'''
type 2 
 ##########################################################################
 설정시간 만족시 True = BtnPressTimer(타임아웃 간격ms, 설정시간ms, 진행바GUI)
 ##########################################################################
    Key2PressTimer.state(True) 일정간격 입력 받아야함.
        KEY2_RESPOSE_TIME_OUT 시간을 넘기면
            False 반환,
            타이머 종료,
            GUI 숨김

        gui_progress GUI 상태바에서 진행율 표시 100%

        KEY2_PUSH_TIME 시간동안 True 계속 입력이 되면
            True 반환,
            타이머 종료,
            GUI 숨김
        

'''

import os, sys, time
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from setup import *

# KEY2_RESPOSE_TIME_OUT = 0.5  # 키입력 타임아웃 시간 (초)
# KEY2_TIMER_INTERVAL = 100    # 타이머 간격     
# KEY2_PUSH_TIME = 2000        # 누르는 대기시간
# KEY2_VIEW_DELAY = 1000       # 푸쉬완료후 화면에 보여주는 시간

# KEY3_RESPOSE_TIME_OUT = 0.5  # 키입력 타임아웃 시간 (초)
# KEY3_TIMER_INTERVAL = 100    # 타이머 간격     
# KEY3_PUSH_TIME = 2000        # 누르는 대기시간
# KEY3_VIEW_DELAY = 1000       # 푸쉬완료후 화면에 보여주는 시간

##############################################################################
# 설정시간 만족시 True = Key2PressTimer(타임아웃 간격ms, 설정시간ms, 진행바GUI)
##############################################################################
# self.btn_Timer.timeout.connect(self.timeoutEndDelay)    # <경고>  connect 변경되지 않고 connect가 추가됨.

class Key2PressTimer(object):
    #                  타이버 간격, 설정시간, ,화면진행바
    def __init__(self, interval, setTime, setDelay, gui_progress):
        self.btn_interval = interval
        self.btn_setTime = setTime
        self.btn_setDelay = setDelay
        self.gui_progress = gui_progress

        # Starting Timer
        self.btn_Timer = QTimer()
        self.btn_Timer.setInterval(self.btn_interval)
        self.btn_Timer.timeout.connect(self.timeout)    #<-
        
        # 연속된 입력시 1회만 동작하도록
        self.finished = False

        # 100% 누름 후 잠깐 화면에 보여줄 시간
        self.viewMode = 0       # 0: 초기 일반 timeout, 1: View 보이기 timeout
        self.viewModeCnt = 0    # view 보이기 카운터

    # .state(T/F) 연속된 신호를 받음
    # ret = finish (timer ended) True/False
    def state(self, state):
        # 입력신호 타임오버
        self.recvTime = time.time()   # 정수 부분은 초단위이고, 소수 값은 마이크로 초단위

        if state == True:
            # 1회 실행후, 재실행 금지 True 반환
            if self.finished == True:
                return True
            else:
                # 1) True : 타이머 시작
                if not self.btn_Timer.isActive():
                    # 타이머 시작
                    self.btn_Timer.start()
                    self.btn_TimerCnt = 0
                    self.gui_progress.setValue(0)   # view
                    self.gui_progress.show()        # view
                    self.prevTime = time.time()
                return False
        # state == False
        # else: 
        elif state == False and self.viewMode == 0: 
            if self.btn_Timer.isActive():
                self.timeEnd()
            self.finished = False

            return False

    # TIMER STARTING 'TIMEOUT' CHECK..
    def timeout(self):
        # self.viewMode == 0 / 일반 타이머 모드
        if self.viewMode == 0:
            # 응답시간 타임오버시 초기화
            responseTime = time.time() - self.recvTime
            if responseTime > KEY2_RESPOSE_TIME_OUT: # 0.2 초 응답시간
                print("KEY2_RESPOSE_TIME_OUT : responseTime OVER")
                self.timeEnd()
                return
            
            print('f1 cnt =', self.btn_TimerCnt)
            self.btn_TimerCnt += 1
            if self.btn_TimerCnt > self.btn_setTime/self.btn_interval :  # 1>30
                ''' #** 1) Timer Over : Success **# '''
                # self.timeEnd()
                self.viewMode = 1
                self.finished = True
            else:
                # 2) Timer Not Over : TIMER COUNT++ , 디스프레이 업데이트
                percent = int(self.btn_TimerCnt * 100/(self.btn_setTime/self.btn_interval))
                if percent > 100:
                    percent = 100
                self.gui_progress.setValue(percent)

        # self.viewMode == 1 / 종료후, 화면 잠깐 보이기 모드
        else:
            print('  f2 cnt = ', self.viewModeCnt)
            self.viewModeCnt += 1
            if self.viewModeCnt > self.btn_setDelay/self.btn_interval:
                self.timeEnd()

                self.viewMode = 0
                self.viewModeCnt = 0

    def timeEnd(self):
        # 2) False : 타이머 중지
        self.btn_Timer.stop()
        # 디스플레이 중지
        self.gui_progress.hide()     # view


##############################################################################
# 설정시간 만족시 True = Key2PressTimer(타임아웃 간격ms, 설정시간ms, 진행바GUI)
##############################################################################
class Key3PressTimer(object):
    #                  타이버 간격, 설정시간, ,화면진행바
    def __init__(self, interval, setTime, setDelay, gui_progress):
        self.btn_interval = interval
        self.btn_setTime = setTime
        self.btn_setDelay = setDelay
        self.gui_progress = gui_progress

        # Starting Timer
        self.btn_Timer = QTimer()
        self.btn_Timer.setInterval(self.btn_interval)
        self.btn_Timer.timeout.connect(self.timeout)    #<-
        
        # 연속된 입력시 1회만 동작하도록
        self.finished = False

        # 100% 누름 후 잠깐 화면에 보여줄 시간
        self.viewMode = 0       # 0: 초기 일반 timeout, 1: View 보이기 timeout
        self.viewModeCnt = 0    # view 보이기 카운터

    # .state(T/F) 연속된 신호를 받음
    # ret = finish (timer ended) True/False
    def state(self, state):
        # 입력신호 타임오버
        self.recvTime = time.time()   # 정수 부분은 초단위이고, 소수 값은 마이크로 초단위

        if state == True:
            # 1회 실행후, 재실행 금지 True 반환
            if self.finished == True:
                return True
            else:
                # 1) True : 타이머 시작
                if not self.btn_Timer.isActive():
                    # 타이머 시작
                    self.btn_Timer.start()
                    self.btn_TimerCnt = 0
                    self.gui_progress.value = 0   # view
                    self.gui_progress.show()      # view
                    self.prevTime = time.time()
                return False
        # state == False
        # esle: 
        elif state == False and self.viewMode == 0: 
            if self.btn_Timer.isActive():
                self.timeEnd()
            self.finished = False

            return False

    # TIMER STARTING 'TIMEOUT' CHECK..
    def timeout(self):
        # self.viewMode == 0 / 일반 타이머 모드
        if self.viewMode == 0:
            # 응답시간 타임오버시 초기화
            responseTime = time.time() - self.recvTime
            # if responseTime > KEY3_RESPOSE_TIME_OUT: # 0.2 초 응답시간
            if responseTime > val.key3_respose_time_out : # 0.2 초 응답시간

                print("KEY3_RESPOSE_TIME_OUT : responseTime OVER")
                self.timeEnd()
                return
            
            # print('f1 cnt =', self.btn_TimerCnt)
            self.btn_TimerCnt += 1
            if self.btn_TimerCnt > self.btn_setTime/self.btn_interval :  # 1>30
                ''' ** 1) Timer Over : Success ** '''
                # self.timeEnd()
                self.viewMode = 1
                self.finished = True
            else:
                # 2) Timer Not Over : TIMER COUNT++ , 디스프레이 업데이트
                percent = int(self.btn_TimerCnt * 100/(self.btn_setTime/self.btn_interval))
                if percent > 100:
                    percent = 100
                self.gui_progress.value = percent

        # self.viewMode == 1 / 종료후, 화면 잠깐 보이기 모드
        else:
            # print('  f2 cnt = ', self.viewModeCnt)
            self.viewModeCnt += 1
            if self.viewModeCnt > self.btn_setDelay/self.btn_interval:
                self.timeEnd()

                self.viewMode = 0
                self.viewModeCnt = 0

    def timeEnd(self):
        # 2) False : 타이머 중지
        self.btn_Timer.stop()
        # 디스플레이 중지
        self.gui_progress.hide()     # view
        # 연속된 입력시 1회만 동작하도록
        self.finished = False


# NEW 새로 
##############################################################################
# 설정시간 만족시 True = Key2PressTimer(타임아웃 간격ms, 설정시간ms, 진행바GUI)
##############################################################################
class FingerKeyTimer(object):
    #                  타이버 간격, 설정시간, ,화면진행바
    def __init__(self, interval, setTime, setDelay, lb_fingerText, pb_fingerText):
        self.pb_interval = interval
        self.pb_setTime = setTime
        self.pb_setDelay = setDelay
        self.lb_fingerText = lb_fingerText
        self.pb_fingerText = pb_fingerText

        # Starting Timer
        self.pb_Timer = QTimer()
        self.pb_Timer.setInterval(self.pb_interval)
        self.pb_Timer.timeout.connect(self.timeout)    # <-
        
        # 연속된 입력시 1회만 동작하도록
        self.finished = False

        # 100% 누름 후 잠깐 화면에 보여줄 시간
        self.viewMode = 0       # 0: 초기 일반 timeout, 1: View 보이기 timeout
        self.viewModeCnt = 0    # view 보이기 카운터

        self.finger_old = None

    def reset(self):
        self.finished = False
        # pass
 
    def value(self, finger):
        self.recvTime = time.time()   # 정수 부분은 초단위이고, 소수 값은 마이크로 초단위
        
        # 이전 값과 다른 경우
        if finger != self.finger_old and self.finished == False:
            print("** 손가락 변경 **")
            if self.pb_Timer.isActive():
                # 타이머 중지
                self.pb_Timer.stop()
            # 타이머 시작
            self.pb_Timer.start()
            # 리셋
            self.pb_TimerCnt = 0
            self.pb_fingerText.setValue(0) # view
            self.prevTime = time.time()
            self.lb_fingerText.show()       # view
            self.pb_fingerText.show()       # view

            self.finger_old = finger
            # self.finished = False
            return False
        
        # 이전 값과 같은 경우
        elif  self.pb_fingerText.value() >= 100 and self.finished == False:
            # print("** 손가락 Finsh **")
            self.finger_old = finger
            self.finished = True
            return True


    # FINGER_RESPOSE_TIME_OUT 시간 이내에 신호가 계속 들어오면 Progress Bar 증가
    def timeout(self):
        # self.viewMode == 0 / 일반 타이머 모드
        if self.viewMode == 0 and self.finished == False:
            # 입력시간 타임오버시 초기화
            responseTime = time.time() - self.recvTime
            if responseTime > FINGER_RESPOSE_TIME_OUT:     # 0.2 초 응답시간
                print("Finger responseTime OVER (Fail)")
                self.timeEnd()
                return
            
            # print('f1 cnt =', self.btn_TimerCnt)
            self.pb_TimerCnt += 1
            if self.pb_TimerCnt > self.pb_setTime/self.pb_interval :  # 1>30
                ''' ** 1) Timer Over : Success ** '''
                # self.timeEnd()
                self.viewMode = 1
            else:
                # 2) Timer Not Over : TIMER COUNT++ , 디스프레이 업데이트
                percent = int(self.pb_TimerCnt * 100/(self.pb_setTime/self.pb_interval))
                if percent > 100:
                    percent = 100
                self.pb_fingerText.setValue(percent)

        # self.viewMode == 1 / 종료후, 화면 잠깐 보이기 모드
        else:
            # print('  f2 cnt = ', self.viewModeCnt)
            self.viewModeCnt += 1
            if self.viewModeCnt > self.pb_setDelay/self.pb_interval:
                self.timeEnd()

                self.viewMode = 0
                self.viewModeCnt = 0

    def timeEnd(self):
        # 2) False : 타이머 중지
        self.pb_Timer.stop()
        # 디스플레이 중지
        self.pb_fingerText.hide()     # view
        self.lb_fingerText.hide()     # view
        # 연속된 입력시 1회만 동작하도록
        # self.finished = False
        self.finger_old = None


''' ###################################################################################  
     동작 테스트 

    ###################################################################################  '''
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(500, 500)
        self.show()
        # Create contatner and layout
        self.container = QFrame()
        # self.container.setStyleSheet("background-color: transparent")
        self.container.setStyleSheet("background-color: #222222")
        self.layout = QVBoxLayout()

        # Add Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        # self.slider.valueChanged.connect(self.change_value)

        # Add widgets
        self.layout.addWidget(self.slider, Qt.AlignCenter, Qt.AlignCenter)

        # Set central widget
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.sTimer = Key3PressTimer(KEY3_TIMER_INTERVAL, KEY3_PUSH_TIME, KEY3_VIEW_DELAY, self.slider)
        self.slider.setValue(5)


        ##### 버튼 테스트 #############################
        print('start..   ')
        i = 1
        while(i):
   
            msdelay(100)
            if  i < 10:
                tf = self.sTimer.signal(True) # timer 시작
                
            elif 10 < i <30:
                tf = self.sTimer.signal(False) # timer 시작
            
            elif 30 < i < 65:
                tf = self.sTimer.signal(True) # timer 시작

            elif 65 < i < 70:
                tf = self.sTimer.signal(False) # timer 시작

            elif 70 < i < 120:
                tf = self.sTimer.signal(True) # timer 시작

            # print('i =', i, 'tf =', tf)
            # tf = self.sTimer.signal(True) # timer 시작

            i += 1
            if i > 140:
                i = 0
        #############################################

def msdelay(ms):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit) # msec
    loop.exec()

''' ###################################################################################  '''

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
