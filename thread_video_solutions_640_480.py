'''
video_thead -> sout_thread : X 취소 문제가 있음. 재생 타이밍을 제어가하기 힘듬.

'''
# #########################################################################
CAP_DISPLAY_WIDTH = 640 ; CAP_DISPLAY_HEIGHT = 480    # 480p       - 15 프레임 이하
PIPE_DISPLAY_WIDTH = 640 ; PIPE_DISPLAY_HEIGHT = 480  # 1.33
# #########################################################################

# ####### 버튼 관련 #######################################################
# x = 640(320), y = 480(240)
BUTTON_START_X = 210 ; BUTTON_START_Y = 200   # 버튼 시작 위치 margin (처음 위치만 지정) 240, 290
BUTTON_SIZE_X = 35 ; BUTTON_SIZE_Y = 45       # 버튼 사이즈 60, 80

BUTTON_FONT_SIZE = 1                          # 2
# BUTTON_TEXT_POS_X = 10 ; BUTTON_TEXT_POS_Y = 43 # 버튼 내부 텍스트 상대위치 10, 50
BUTTON_TEXT_POS_X = -2 ; BUTTON_TEXT_POS_Y = 43 # 버튼 내부 텍스트 상대위치 10, 50

BUTTON_CAP_X = 10  ; BUTTON_CAP_Y = 10        # 버튼 사이간격 27, 20


# #########################################################################
# CAP_DISPLAY_WIDTH = 640 ; CAP_DISPLAY_HEIGHT = 480    # 480p       - 15 프레임 이하
# PIPE_DISPLAY_WIDTH = 840 ; PIPE_DISPLAY_HEIGHT = 631  # 1.33
# #########################################################################

from PySide6.QtCore import *
import mediapipe as mp
import numpy as np
import cv2
import math, time
from PySide6.QtGui import *
# from PySide6 import QtGui
from PySide6 import QtTest
# from PyQt5.QtWidgets import QApplication

from setup import *

# #########################################################################
#  ThreadVideo
# #########################################################################
class ThreadVideo(QThread):

    change_pixmap_signal = Signal(np.ndarray)   # 시그널 정의
    key_repeat_signal = Signal(str)          # 터치 연속 신호
    key_one_signal = Signal(str)            # 터치 1회만 신호
    fps_signal = Signal(str)
    _started_signal = Signal()               # thread 실행됨을 알림.

    def __init__(self, frameView_width, frameView_height):

        super().__init__()

        self.buttonlist=[]
        self.keys = []

        self._run_flag = True

        self.frameView_width = frameView_width
        self.frameView_height = frameView_height

        ##################################################################
        # find_postion(self, frame) / MediaPipe 패키지에서 사용할 기능들.
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands           # 손 인식을 위한 객체
        self.hands = self.mp_hands.Hands()           # 손 인식 객체 생성
        ##################################################################

        self.keyTouchSelect = None
        self.keyTouchSelectOld = None

        self.viewText = ""

        ''' 터치 KEY 버튼 Display 생성 TEST '''
        # self.button_default_create()
        # self.button_choice5_create()
        # self.button_ox_create()
        # self.button_yn_create()
        # self.button_start_create()
        # self.button_user_create()
        # self.button_clear()

        # 기본적으로 외부 장치 선택
        if DEFAULT_CAPTURE_DEVICE == 0:
            self.captureDevice = CAPTURE_DEVICE0
        elif DEFAULT_CAPTURE_DEVICE == 1:
            self.captureDevice = CAPTURE_DEVICE1

        self._started = False

    def run(self):
        self._run_flag = True
        print(' > Video Thread run... ')
        # capture from web cam
        # OpenCV 웹캠 연결 문제 https://deep-eye.tistory.com/73 > cv2.CAP_DSHOW 로딩 속도 개선
        # cap = cv2.VideoCapture(cv2.CAP_DSHOW+1)       # cv2.CAP_DSHOW 로딩 속도 개선
        cap = cv2.VideoCapture(self.captureDevice)                   # USB 캠 속도 매우 느림.

        # <1> 캡쳐 사이즈 결정
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAP_DISPLAY_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAP_DISPLAY_HEIGHT)

        prevTime = 0 #frame 계산 : 이전 시간을 저장할 변수
        while self._run_flag:

            ret, frame = cap.read() # 카메라 데이터 읽기
            # print('frame : ', type(frame))
            h, w, c = frame.shape
            if prevTime == 0 : 
                print('capture size =',w ,'*', h)

            ######################## 프레임 수계산하기 #######################
            curTime = time.time() # 현재 시간 가져오기 (초단위로 가져옴)
            sec = curTime - prevTime
            prevTime = curTime
            fps = 1/(sec)               # 1 / time per frame
            fps_str = "FPS : %0.1f" % fps    # 프레임 수를 문자열에 저장
            self.fps_signal.emit(fps_str)
            ################################################################

            if ret:
                # <2> 이미지 자르기1
                # crop_image # 1280x720 > 840x631기본 처리 설정된 사이즈로 변환
                #   1280-840 = 440/2 =220
                #   720-680 = 40/2 =20

                ## ( option2 ) ******** >> 이미지 자르기 << **********
                # cropH = 20+PIPE_DISPLAY_HEIGHT ; cropW = 220+PIPE_DISPLAY_WIDTH
                # cv_frame = frame[20:cropH , 220:cropW]
                cv_frame = frame    # ( option2 )  ************ > 자르지 않고 사용하기

                # <2> 이미지 자르기2
                # crop_image # 840x680 > 840x631기본 처리 설정된 사이즈로 변환
                # cv_frame = frame[:PIPE_DISPLAY_WIDTH , :PIPE_DISPLAY_HEIGHT]
                ##################################################
                # h, w, c = frame.shape   ; print(h, w, c)

                if self._started == False:   # 비디오 쓰레드가 실행되어 준비됨을 알림.
                    self._started = True
                    self._started_signal.emit()
                    self._started

                cv_frame = cv2.flip(cv_frame, flipCode = 1)                 # 셀프 카메라처럼 좌우 반전
                # cv_frame = cv2.resize(cv_frame, (PIPE_DISPLAY_WIDTH, PIPE_DISPLAY_HEIGHT))  # 과정을 거치면 비율이 변함
                # cv2.putText(cv_frame, fps_str, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),1) # frame 표시

                # <1> 손 디스플레이 및 리스트 가져오기
                a = self.find_postion(cv_frame)                             # 손 디스플레이이 및 리스트 가져오기
                
                # <2> 터치버튼 모두 그리기
                cv_frame = self.draw_all_keys(cv_frame, self.buttonlist)    # [_]버튼 모두 그리기

                # <3> 손가락 키보드 검사
                self.keyTouchCheck(cv_frame, a)

                # <4> 손

                ########### 테스트용 #############################
                if __name__=="__main__":
                    cv2.imshow('frame',cv_frame)
                    if cv2.waitKey(1) == ord('q'):
                        break
                ########### 테스트용 #############################

                qt_img = self.convert_cv2qt(cv_frame)

                self.change_pixmap_signal.emit(qt_img)
        # shut down capture system
        cap.release()

    def convert_cv2qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # >> 화면 전체 프레임 채우기 <<
        p = convert_to_Qt_format.scaled(self.frameView_width, self.frameView_width, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
        
        # return QPixmap.fromImage(convert_to_Qt_format)
    

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.quit()
        self.wait(5000) # 쓰레드가 정리 작업을 완료하고 종료될 때까지 메인 프로그램이 대기


    def find_postion(self, frame):
        w = PIPE_DISPLAY_WIDTH
        h = PIPE_DISPLAY_HEIGHT

        list=[]
        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # 이미지에서 손을 찾고 결과를 반환 < 이미지 인식

        if results.multi_hand_landmarks != None:                        # 손이 인식되었는지 확인
            # print('test f2 : ',results.multi_hand_landmarks)
            # multi_hand_landmarks 손의 주요 부분에 대한 x,yz정보를 리스트 형태도 담고 있음
            # index를 사용하여 해당 부분에 접근이 가능함.
            for handLandmarks in results.multi_hand_landmarks:          # 반복문을 활용해 인식된 손의 주요 부분을 그림으로 그려 표현
                self.mp_drawing.draw_landmarks(
                    frame,                              # 프레임
                    handLandmarks,                      # 손에 인식된 정보
                    self.mp_hands.HAND_CONNECTIONS,     # 전달된 정보를 손의 형태로 그리도록
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),   # mp_drawing_styles 그르는 색상, 크기 등을 지정
                    self.mp_drawing_styles.get_default_hand_connections_style(),
                    )
                
                # list=[] # 활성화시 한손만 데이터만 리스트에 저장됨.
                for id, pt in enumerate (handLandmarks.landmark):
                    x = int(pt.x * w)
                    y = int(pt.y * h)

                    list.append([id, x, y]) # 모든 선 정보가 저장된다.
        return list
# COLOR = (255, 255, 0) # BGR : 옥색
# RADIUS = 50     # 반지름
# THICKNESS = 10  # 두께

# #         그릴위치, 원의 중심점, 반지름, 색깔, 두께, 선 종류
# cv2.circle(img, (200, 100), RADIUS, COLOR, THICKNESS, cv2.LINE_AA)  # 속 빈 원

    def keyTouchCheck(self, frame, a):
        self.keyTouchSelect = None

        while( len(a)>20 ):
        # if len(a) != 0:
            for button in self.buttonlist:   # 모든 버튼list 을 검사
                x, y = button.pos
                w, h = button.size
                x1, y1 = a[8][1], a[8][2]      # 검지(8) 손가락 위치
                x2, y2 = a[12][1], a[12][2]    # 중지(12) 손가락 위치

                # 집게 손가락 위치에 원 그리기
                #                    위치, 반지름, 색상        ,두께, 빈원
                cv2.circle(frame, ( x1, y1), 15 , (255, 255, 0), 3, cv2.LINE_AA)


                ## <1> : 손가락 거리 계산
                length = math.hypot(x2-x1, y2-y1)    # 중지(12)-검지(8): 사이 거리계산
                # button.text 순환하면서 검사 하므로 의미 없음.

                ## <2> : 검지(8) 손가락 위치 & [버튼] 터치 여부 검사
                if x < x1 < x+w and y < y1 < y+h:
                    ''' <키보드 터치 그리기>  검지(8) 터치 [버튼] 색상변경  '''
                    # def draw_key(self, frame, button, rec_color, rec_type, txt_color):
                    self.draw_key(frame, button, (122, 0, 122), -1, (255,255,255))
                    '''                                                  '''

                    # # <2-1> 터치할 경우 입력
                    self.keyTouchSelect = button.text       # 터치된 버튼 저장
                    if self.keyTouchSelectOld == None:      # ** 터치 순간 1회만 입력이 인식한다. **

                        self.key_one_signal.emit(str(button.text))
                        print('key_one_signal.emit =', str(button.text))

                        # if button.text == '1':
                        #     button_yn_create()
                        # elif button.text == '2':
                        #     button_ox_create()

                        # if button.text == '<':
                        #     self.viewText = self.viewText[:-1]  # 마지막 문자 삭제
                        # else:
                        #     if len(self.viewText) > 15:      
                        #         self.viewText = self.viewText[len(button.text):]
                        #     self.viewText += button.text   # View
            

                    ## <3> : 중지-검지 거리 조건 만족하는 경우.
                    # if length < 40:
                        ### <키보드 클릭 그리기> 검지-중지 [버튼] 색상변경   '''
                        # self.draw_key(frame, button, (0, 0, 255), -1, (0,255,0))
                        ###                                              '''
                    #     keySelect = button.text     # 터치 Click 한 경우 저장
                    #     if keySelectOld == None: 
                    #         if button.text == '<':
                    #             viewText = viewText[:-1]  # 마지막 문자 삭제
                    #         else:
                    #             if len(viewText) > 15:      
                    #                 viewText = viewText[1:]
                    #             viewText += button.text # View

                        # keyboard.press(button.text)
                        # keyboard.release(button.text)
            a = a[21:]
            
        self.keyTouchSelectOld = self.keyTouchSelect    # 중요

        # print(self.keyTouchSelect)
        self.key_repeat_signal.emit(str(self.keyTouchSelect))  # ** 터치 연속 입력이 인식한다. **
        # print('key_repeat_signal =', self.keyTouchSelect)   # None, 1,2,3 ... 신호가 연속 전달됨.

    # #########################################################################
    # 키보드 그리기 (형광색)
    #   전체 키보드를 그리기
    # #########################################################################
    
    def draw_all_keys(self, img, buttonlist):
        for button in self.buttonlist:
            ''' <키보드 전체 그리기> '''
            # def draw_key(self, frame, button, rec_color, rec_type, font_color, font_size):
            self.draw_key(img, button, (0,255,0), 2, (0,255,0))
            '''                    '''
        return img
    
    def draw_key(self, frame, button, rec_color, rec_type, font_color):
        x, y = button.pos
        w, h = button.size
        font_size = button.font_size
        cv2.rectangle(frame, (button.pos), (x+w, y+h), (rec_color), rec_type)   # 버튼 사격형그리기 / (0,0,255)
        if font_size == 2:
            cv2.putText(frame, button.text, (x+BUTTON_TEXT_POS_X+button.font_pos, y+BUTTON_TEXT_POS_Y),cv2.FONT_HERSHEY_SIMPLEX, font_size ,(font_color), 5 , cv2.LINE_AA)   # (255,255,255)
        else:
            cv2.putText(frame, button.text, (x+BUTTON_TEXT_POS_X+10+button.font_pos, y+BUTTON_TEXT_POS_Y-10),cv2.FONT_HERSHEY_SIMPLEX, font_size ,(font_color), 3 , cv2.LINE_AA)   # (255,255,255)



    '''  ###################  가상 버튼 관련 정의 ##########################  '''

    # #########################################################################
    #  (640*480)
    #  (5선다형) 문제 버튼 리스트 생성 | quit, 1, 2, 3 4, 5, pass
    # #########################################################################

    def button_choice1_create(self):

        BUTTON_START_X = 110
        BUTTON_CAP_X = 13          # 버튼 사이간격

        self.buttonlist.clear()
        self.keys       = [ ["QUIT","1","2","3","4","5","PASS"] ]

        for i in range(1):
            # 1번째 START - 시작부분
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*0 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][0],                         # 리스트[][순번]
                                        [BUTTON_SIZE_X*2, BUTTON_SIZE_Y],   # 버튼사이즈 사용자정의
                                        0.7))                                 # 폰트 크기 1 or 2
            # 2번째 [1]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*2 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][1]))

            # 7번째 END - 끝부분
            self.buttonlist.append( Button([ PIPE_DISPLAY_WIDTH-BUTTON_SIZE_X*2 - BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][6],
                                        [BUTTON_SIZE_X*2, BUTTON_SIZE_Y],
                                        0.7))

    # #########################################################################
    def button_choice2_create(self):

        BUTTON_START_X = 110
        BUTTON_CAP_X = 13          # 버튼 사이간격

        self.buttonlist.clear()
        self.keys       = [ ["QUIT","1","2","3","4","5","PASS"] ]

        for i in range(1):
            # 1번째 START - 시작부분
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*0 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][0],                         # 리스트[][순번]
                                        [BUTTON_SIZE_X*2, BUTTON_SIZE_Y],   # 버튼사이즈 사용자정의
                                        0.7))                                 # 폰트 크기 1 or 2
            # 2번째 [1]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*2 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][1]))
            # 3번째 [2]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*3 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][2]))

            # 7번째 END - 끝부분
            self.buttonlist.append( Button([ PIPE_DISPLAY_WIDTH-BUTTON_SIZE_X*2 - BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][6],
                                        [BUTTON_SIZE_X*2, BUTTON_SIZE_Y],
                                        0.7))
            
    # #########################################################################
    def button_choice3_create(self):

        BUTTON_START_X = 110
        BUTTON_CAP_X = 13          # 버튼 사이간격

        self.buttonlist.clear()
        self.keys       = [ ["QUIT","1","2","3","4","5","PASS"] ]

        for i in range(1):
            # 1번째 START - 시작부분
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*0 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][0],                         # 리스트[][순번]
                                        [BUTTON_SIZE_X*2, BUTTON_SIZE_Y],   # 버튼사이즈 사용자정의
                                        0.7))                                 # 폰트 크기 1 or 2
            # 2번째 [1]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*2 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][1]))
            # 3번째 [2]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*3 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][2]))
            # 4번째 [3]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*4 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][3]))

            # 7번째 END - 끝부분
            self.buttonlist.append( Button([ PIPE_DISPLAY_WIDTH-BUTTON_SIZE_X*2 - BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][6],
                                        [BUTTON_SIZE_X*2, BUTTON_SIZE_Y],
                                        0.7))
            
    # #########################################################################
    def button_choice4_create(self):

        BUTTON_START_X = 110
        BUTTON_CAP_X = 13          # 버튼 사이간격

        self.buttonlist.clear()
        self.keys       = [ ["QUIT","1","2","3","4","5","PASS"] ]

        for i in range(1):
            # 1번째 START - 시작부분
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*0 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][0],                         # 리스트[][순번]
                                        [BUTTON_SIZE_X*2, BUTTON_SIZE_Y],   # 버튼사이즈 사용자정의
                                        0.7))                                 # 폰트 크기 1 or 2
            # 2번째 [1]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*2 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][1]))
            # 3번째 [2]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*3 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][2]))
            # 4번째 [3]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*4 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][3]))
            # 5번째 [4]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*5 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][4]))

            # 7번째 END - 끝부분
            self.buttonlist.append( Button([ PIPE_DISPLAY_WIDTH-BUTTON_SIZE_X*2 - BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][6],
                                        [BUTTON_SIZE_X*2, BUTTON_SIZE_Y],
                                        0.7))

    # #########################################################################
    def button_choice5_create(self):

        BUTTON_START_X = 110
        BUTTON_CAP_X = 13          # 버튼 사이간격

        self.buttonlist.clear()
        self.keys       = [ ["QUIT","1","2","3","4","5","PASS"] ]

        for i in range(1):
            # 1번째 START - 시작부분
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*0 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][0],                         # 리스트[][순번]
                                        [BUTTON_SIZE_X*2, BUTTON_SIZE_Y],   # 버튼사이즈 사용자정의
                                        0.7))                                 # 폰트 크기 1 or 2
            # 2번째 [1]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*2 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][1]))
            # 3번째 [2]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*3 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][2]))
            # 5번째 [3]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*4 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][3]))
            # 5번째 [4]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*5 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][4]))
            # 6번째 [5]
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*6 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][5]))
            # 7번째 END - 끝부분
            self.buttonlist.append( Button([ PIPE_DISPLAY_WIDTH-BUTTON_SIZE_X*2 - BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][6],
                                        [BUTTON_SIZE_X*2, BUTTON_SIZE_Y],
                                        0.7))

    # #########################################################################
    #  (640*480)
    #  (O,X) 문제 버튼 리스트 생성 | quit, O, X, pass
    # #########################################################################
    def button_ox_create(self):

        BUTTON_START_X = 110
        BUTTON_CAP_X = 13   # 버튼 사이간격

        self.buttonlist.clear()
        self.keys       = [ ["QUIT","O","X","PASS"] ]

        for i in range(1):
            # 1번째 START - 시작부분 *0
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*0 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][0],
                                        [BUTTON_SIZE_X*2, BUTTON_SIZE_Y],
                                        0.7))
            # 2번째 *2
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*2 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][1],                                 # 리스트[][순번]
                                        [BUTTON_SIZE_X*3, BUTTON_SIZE_Y],           # 버튼사이즈 사용자정의
                                        BUTTON_FONT_SIZE,                           # 폰트 크기 1 or 2
                                        35))                                        # 텍스트 위치 상대위치 추가
            # 3번째 *5-20
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*5-20 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][2],
                                        [BUTTON_SIZE_X*3, BUTTON_SIZE_Y],
                                        BUTTON_FONT_SIZE,
                                        35))
    
            # 7번째 END - 끝부분
            self.buttonlist.append( Button([ PIPE_DISPLAY_WIDTH-BUTTON_SIZE_X*2 - BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][3],
                                        [BUTTON_SIZE_X*2, BUTTON_SIZE_Y],
                                        0.7))

    # #########################################################################
    #  (640*480)
    #  (YES,NO) 선택 버튼 리스트 생성
    # #########################################################################
    def button_yn_create(self):

        BUTTON_START_X = 200
        BUTTON_CAP_X = 13   # 버튼 사이간격

        self.buttonlist.clear()
        self.keys       = [ ["YES","NO"] ]

        for i in range(1):
            # 1번째 START - 시작부분
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*0 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][0],
                                        [BUTTON_SIZE_X*3, BUTTON_SIZE_Y],
                                        BUTTON_FONT_SIZE,
                                        15))
    
            # 2번째 END - 끝부분
            self.buttonlist.append( Button([ PIPE_DISPLAY_WIDTH - BUTTON_SIZE_X*3 - BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][1],
                                        [BUTTON_SIZE_X*3, BUTTON_SIZE_Y],
                                        BUTTON_FONT_SIZE,
                                        22))


    # #########################################################################
    #  (640*480)
    #  (START) 단독 선택 버튼 리스트 생성
    # #########################################################################
    def button_start_create(self):
        
        BUTTON_START_X = 225;       # 버튼 시작 위치 margin (처음 위치만 지정) 240, 290

        self.buttonlist.clear()
        self.keys       = [ ["START"] ]

        for i in range(1):
            # 1번째 START - 시작부분
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X) + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][0],
                                        [BUTTON_SIZE_X*3+9, BUTTON_SIZE_Y],
                                        BUTTON_FONT_SIZE,
                                        3))

    # #########################################################################
    #  (640*480)
    #  (OK) 단독 선택 버튼 리스트 생성
    # #########################################################################
    def button_ok_create(self):

        BUTTON_START_X = 225 ;      # 버튼 시작 위치 margin (처음 위치만 지정) 240, 290

        self.buttonlist.clear()
        self.keys       = [ ["OK"] ]

        for i in range(1):
            # 1번째 START - 시작부분
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X) + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][0],
                                        [BUTTON_SIZE_X*3+9, BUTTON_SIZE_Y],
                                        BUTTON_FONT_SIZE,
                                        25))


    # #########################################################################
    #  (640*480)
    #  (사용자입력) 문제 버튼 리스트 생성 | <-, 1, 2, 3 4, 5, 6, 7, 8, 9, 0 OK
    # #########################################################################
    def button_user_create(self):

        BUTTON_START_X = 30 ;       # 버튼 시작 위치 margin (처음 위치만 지정)
        BUTTON_CAP_X = 14  ;        # 버튼 사이간격

        self.buttonlist.clear()
        self.keys       = [ ["<-","1","2","3","4","5","6","7","8","9","0","OK"] ]

        for i in range(1):
            # 1번째 <-
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*0 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][0],                         # 리스트[][순번]
                                        [BUTTON_SIZE_X, BUTTON_SIZE_Y],   # 버튼사이즈 사용자정의
                                        0.6,                                  # 폰트 크기 1 or 2
                                        -5))   # -13                              
            # 1
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*1 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][1]))
            # 2
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*2 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][2]))
            # 3
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*3 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][3]))
            # 4
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*4 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][4]))
            # 5
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*5 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][5]))
            # 6
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*6 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][6]))
            # 7
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*7 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][7]))
            # 8
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*8 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][8]))
            # 9
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*9 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][9]))
            # 0
            self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*10 + BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][10]))
            # OK - 끝부분
            self.buttonlist.append( Button([ PIPE_DISPLAY_WIDTH-BUTTON_SIZE_X*1 - BUTTON_START_X,
                                        (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                        self.keys[0][11],
                                        [BUTTON_SIZE_X, BUTTON_SIZE_Y],
                                        0.7,
                                        -5))   # 10
            
    # #########################################################################
    #  (clear) 문제 버튼 리스트 지우기
    # #########################################################################
    def button_clear(self):
        self.buttonlist = []

    def button_none(self):
        # self.buttonlist = []
        pass


    # #########################################################################
    # 버튼 리스트 생성
    # #########################################################################
    def button_default_create(self):
        self.buttonlist = []
        self.keys=[["0","1","2","3","4","5","6","7","8","9","X"],
            ["O"],
            ["<"]]
        
        for i in range(2):                          # range[행] i <- 표시할 행의 갯수
            for j, key in enumerate( self.keys[i] ):
                # self.buttonlist.append(button([70*j+20, 70*i+40], key)) 
                self.buttonlist.append( Button([ (BUTTON_SIZE_X+BUTTON_CAP_X)*j + BUTTON_START_X,
                                            (BUTTON_SIZE_Y+BUTTON_CAP_Y)*i + BUTTON_START_Y ],
                                            key) )



# 버튼 사이즈 정의 ( [위치x,위치y],  텍스트, [사이즈x, 사이즈y] )
#                                          사이즈는 초기값 지정
# #########################################################################
class Button():
    def __init__(self, pos, text, size=[BUTTON_SIZE_X, BUTTON_SIZE_Y], font_size=BUTTON_FONT_SIZE, font_pos=0):
        self.pos = pos              # 버튼 위치
        self.text = text            # 버튼 텍스트
        self.size = size            # 버튼 사이즈()
        self.font_size = font_size  # 폰트 사이즈 2 or 1  (기본=2)
        self.font_pos = font_pos    # 폰트위치 상대값 추가 (기본=0)



if __name__=="__main__":
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    import sys

    app = QApplication(sys.argv)

    a = ThreadVideo(640, 480)
    a.start()


    sys.exit(app.exec())