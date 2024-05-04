''' 
640* 480 해상도 사용 / solutions
2023.11.x
    mediapipe.solutions.vision.HandLandmarker 이용한 손 인식 ( 2024. 업데이트 된 0.10.10 )

    https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
    https://github.com/google/mediapipe

2024.02.26
    손가락 카운트 기능 업데이트 
    https://medium.com/@oetalmage16/a-tutorial-on-finger-counting-in-real-time-video-in-python-with-opencv-and-mediapipe-114a988df46a
    https://github.com/OwenTalmo/finger-counter
    
     카운터 포인터 위치 및 계산 방식 변경
    한손 1~5 카운드, 엄지 업/다운 구현

2024.02.27
    인식되는 손의 갯수 전환 1, 2개 테스트

video_thead -> sout_thread : X 취소 문제가 있음. 재생 타이밍을 제어가하기 힘듬.

'''
# 320 x 240, 640 x 480, 1280 x 720, 1920 x 1080

# W = 1280
# H = 720
# # #########################################################################
# CAP_DISPLAY_WIDTH = W ; CAP_DISPLAY_HEIGHT = H    # 480p       - 15 프레임 이하
# PIPE_DISPLAY_WIDTH = W ; PIPE_DISPLAY_HEIGHT = H  # 1.33
# # # #########################################################################

# # #########################################################################
CAP_DISPLAY_WIDTH = 640 ; CAP_DISPLAY_HEIGHT = 480    # 480p       - 15 프레임 이하
PIPE_DISPLAY_WIDTH = 640 ; PIPE_DISPLAY_HEIGHT = 480  # 1.33
# # #########################################################################

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
    key_repeat_signal = Signal(str)          # 터치 > 연속 신호
    key_one_signal = Signal(str)             # 터치 > 1회만 신호
    finger_repeat_signal = Signal(str)       # 손가락(업지) > 연속 신호
    fps_signal = Signal(str)
    hand_position_signal = Signal(list)         # 손의 위치를 알림.
    _started_signal = Signal()               # thread 실행됨을 알림.

    def __init__(self, frameView_width, frameView_height):

        super().__init__()

        self.buttonlist=[]
        self.keys = []

        self._run_flag = True

        self.frameView_width = frameView_width
        self.frameView_height = frameView_height

        ##################################################################
        # draw_landmarks_on_image(self, frame) / MediaPipe 패키지에서 사용할 기능들.
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands           # 손 인식을 위한 객체
        # self.hands = self.mp_hands.Hands(max_num_hands=1)     # 1개 손 인식 객체 생성   mediapipe.solutions.hands()
        # 처음 시작시 2개의 손가락 인식
        self.hands = self.mp_hands.Hands()                  # 2개 손 인식 객체 생성   mediapipe.solutions.hands()
        ##################################################################

        self.keyTouchSelect = None
        self.keyTouchSelectOld = None

        self.viewText = ""

        self.input_mode = 'touch'         # touch, fingerCount, thumbUpDown, fingerNone
        self.input_finger_max = 5

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

        # NEW
        # self.input_mode = 
        self.input_mode_1_hand_list = ['fingerCount', 'thumbUpDown', 'fingerNone']


    def close(self):
        # close landmarker
        self.hands.close()


    def run(self):
        if __name__=="__main__":
            self.fps_list = []
            self.fps_cnt = 204
        self._run_flag = True
        print(' > Video Thread run... ')
        # capture from web cam
        # OpenCV 웹캠 연결 문제 https://deep-eye.tistory.com/73 > cv2.CAP_DSHOW 로딩 속도 개선
        # cap = cv2.VideoCapture(cv2.CAP_DSHOW+1)       # cv2.CAP_DSHOW 로딩 속도 개선
        cap = cv2.VideoCapture(self.captureDevice)      # USB 캠 속도 매우 느림.

        # <1> 캡쳐 사이즈 결정
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAP_DISPLAY_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAP_DISPLAY_HEIGHT)

        prevTime = 0                                    # frame 계산 : 이전 시간을 저장할 변수
        while self._run_flag:

            ret, frame = cap.read() # 카메라 데이터 읽기
            # print('frame : ', type(frame))
            frame_height, frame_width, _ = frame.shape
            if prevTime == 0 : 
                print('capture size =',frame_width ,'*', frame_height)

            ######################## 프레임 수계산하기 #######################
            curTime = time.time()           # 현재 시간 가져오기 (초단위로 가져옴)
            sec = curTime - prevTime
            prevTime = curTime
            fps = 1/(sec)                    # 1 / time per frame
            fps_str = "FPS : %0.1f" % fps    # 프레임 수를 문자열에 저장
            self.fps_signal.emit(fps_str)
            val.key3_respose_time_out = sec + KEY3_RESPOSE_TIME_OUT_ADD
            # print( 'val.key3_respose_time_out = ', val.key3_respose_time_out)
            ########### 테스트용 #############################
            if __name__=="__main__":
                fps_save = " %0.1f" % fps
                if self.fps_cnt >= 0:
                    self.fps_list.append(fps_save)       
                    # print(f'fps = {fps}')
                    self.fps_cnt -= 1
                    if self.fps_cnt == 0:
                        # print(self.fps_list)
                        with open(f'_fps_test.txt', 'w+') as file:
                            file.write('\n'.join(self.fps_list))  # '\n' 대신 ', '를 사용하면 줄바꿈이 아닌 ', '를 기준으로 문자열 구분함
                        print(f'SAVE _fps_test.txt')
            ################################################################

            if ret:
                cv_frame = frame    # ( option2 )  ************ > 자르지 않고 사용하기

                if self._started == False:   # 비디오 쓰레드가 실행되어 준비됨을 알림.
                    self._started = True
                    self._started_signal.emit()
                    self._started

                frame = cv2.flip(cv_frame, flipCode = 1)                 # 셀프 카메라처럼 좌우 반전

                # <1> 손 그리기 디스플레이 및 랜드마크 리스트 가져오기
                landmarks_list = self.draw_landmarks_on_image(frame)     # 손 디스플레이이 및 리스트 가져오기
                
                # New 손가락 카운트 검사
                # count number of fingers raised
                frame = self.fingers_raised(frame, landmarks_list)

                # <2> 터치 버튼 모두 그리기
                frame = self.draw_all_keys(frame, self.buttonlist)    # [_]버튼 모두 그리기

                # <3> 터치 버튼, 키 터치 검사
                self.key_touch_check(frame, landmarks_list)

                # <4> 손
                ########### 테스트용 #############################
                if __name__=="__main__":
                    cv2.imshow('frame',frame)
                    k = cv2.waitKey(1)
                    # 종료
                    if k == ord('q'):
                        break
                    # 1개의 손 인식 -> key = 1
                    elif k == ord('1'):
                        del self.hands
                        self.hands = self.mp_hands.Hands(max_num_hands=1)
                    # 2개의 손 인식 -> key = 2
                    elif k == ord('2'):
                        del self.hands
                        self.hands = self.mp_hands.Hands()

                    self.input_fingerCount(5)
                ########### 테스트용 #############################

                qt_img = self.convert_cv2qt(frame)
                self.change_pixmap_signal.emit(qt_img)
                
                #######################################################
                # fingerCount, thumbUpDown, fingerNone 인 경우 손의 위치 x, y 좌표 전달
                if self.input_mode != 'touch': 
                    # x, y 좌표 전달
                    if len(landmarks_list) > 0:
                        ratio_x = self.QmapViewSize.width() / frame_width
                        ratio_y = self.QmapViewSize.height() /frame_height

                        # hand 0 , 9 Point
                        frame_point_x,  frame_point_y = self.middle_of_2_points(landmarks_list[0], landmarks_list[9])

                        qmap_point_x = int(frame_point_x * ratio_x)
                        qmap_point_y = int(frame_point_y * ratio_y)

                        # hand 0 - 5 Point length
                        length = int(self.length(landmarks_list, 0, 5))

                        # print('hand point :', qmap_point_x, qmap_point_y, length )
                        self.hand_position_signal.emit([qmap_point_x, qmap_point_y, length])
                    else:
                        self.hand_position_signal.emit([])

        # shut down capture system
        cap.release()

    def middle_of_2_points(self, p1, p2):
        X = 0; Y = 1
        return (p1[X]+p2[X])/2, (p1[Y]+p2[Y])/2


    def hand_angle(self, landmarks, f1, f2):
        x = 0; y = 1
        #  각도 계산 9시 방향 0도
        x2 = landmarks[f2][x]   # x
        y2 = landmarks[f2][y]   # y
        x1 = landmarks[f1][x]   # x
        y1 = landmarks[f1][y]   # y

        dx = x2 - x1
        dy = y2 - y1
        radians = math.atan2(dy, dx)
        angle = math.degrees(radians)
        angle = round(angle, 2)

        return round(angle-90, 2)

    def convert_cv2qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # >> 화면 전체 프레임 채우기 <<
        p = convert_to_Qt_format.scaled(self.frameView_width, self.frameView_width, Qt.KeepAspectRatio)
        
        # 랜드마크 포인터 계산을 위함.
        self.QmapViewSize = p.size()    
        
        return QPixmap.fromImage(p)
        
        # return QPixmap.fromImage(convert_to_Qt_format)
    

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.quit()
        self.wait(5000) # 쓰레드가 정리 작업을 완료하고 종료될 때까지 메인 프로그램이 대기


    def draw_landmarks_on_image(self, frame):
        w = PIPE_DISPLAY_WIDTH
        h = PIPE_DISPLAY_HEIGHT

        list=[]
        '''
        [퀴즈 종료시 ERR로 멈춤 발생].
        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) 
                "self.hands" AttributeError: 'ThreadVideo' object has no attribute 'hands' ]
        del self.hands 순간에 발생하는 것으로 보임 
        '''
        try:
            results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # 이미지에서 손을 찾고 결과를 반환 < 이미지 인식
            if results.multi_hand_landmarks != None:                              # 손이 인식되었는지 확인
                # print('test f2 : ',results.multi_handedness) # 좌, 우 손 정보 출력
                # multi_hand_landmarks 손의 주요 부분에 대한 x,y,z정보를 리스트 형태도 담고 있음
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

                        # list.append([id, x, y]) # 모든 선 정보가 저장된다. | 무조건 21개의 값이 나오므로 id 불필요
                        list.append([x, y]) # 모든 선 정보가 저장된다.
        except AttributeError:
            print('[ERR PASS] self.hands : AttributeError')
        return list
    

# COLOR = (255, 255, 0) # BGR : 옥색
# RADIUS = 50     # 반지름
# THICKNESS = 10  # 두께

# #         그릴위치, 원의 중심점, 반지름, 색깔, 두께, 선 종류
# cv2.circle(img, (200, 100), RADIUS, COLOR, THICKNESS, cv2.LINE_AA)  # 속 빈 원

    def length(self, landmarks, a, b ):
        x = 0; y = 1
        length_x = landmarks[a][x] - landmarks[b][x]
        length_y = landmarks[a][y] - landmarks[b][y]
        return math.sqrt(length_x**2 + length_y**2)

    def thumb_fingers(self, landmarks):
        x = 0; y= 1
        numRaised = 0
        
        for i in range(8,21,4): # range(start, stop, step)
            tip_x = landmarks[i][x]    # 끝 1번째 (손톱마디)
            dip_x = landmarks[i-1][x]   # 끝 2번째
            pip_x = landmarks[i-2][x]   # 끝 3번째
            mcp_x = landmarks[i-3][x]   # 끝 4번째 (손바닥 마디)

            # 좌 방향
            if landmarks[5][x] - landmarks[0][x] > 0:
                if tip_x < min(dip_x,pip_x,mcp_x) or tip_x < pip_x:
                    # numRaised = 'close min'
                    pass
                else:
                    numRaised += 1
            # 우 방향
            else:
                if tip_x > max(dip_x, pip_x, mcp_x) or tip_x > pip_x:
                    # numRaised = 'close min'
                    pass
                else:
                    numRaised += 1

        if numRaised == 0:
            hand = 'close'
            # 엄지 손가락 올림 검사
            base = self.length(landmarks, 5, 13)
            thumb_value = self.length(landmarks, 4, 6)  # 4:엄지, 6:집게
            if thumb_value > base:
                # print("엄지 척")
                hand = "Thumb"
                if landmarks[4][y] < landmarks[6][y]:
                    hand = 'Thumb up'
                else:
                    hand = 'Thumb down'
        else:
            hand = 'open'

        return hand


    def fingers_raised(self, rgb_image, landmarks_list):
        x = 0; y = 1
        """Iterate through each hand, checking if fingers (and thumb) are raised.
        Hand landmark enumeration (and weird naming convention) comes from
        https://developers.google.com/mediapipe/solutions/vision/hand_landmarker."""
        if len(landmarks_list) != 0:
            angle = self.hand_angle(landmarks_list, 13 ,0 ) # (17,0) (9, 0)
            if abs(angle) > 45:
                # 엄지 위/아래 
                numRaised = self.thumb_fingers(landmarks_list)
            else:
                # 손가락 갯수
                numRaised = self.count_fingers(landmarks_list)

            # display number of fingers raised on the image
            annotated_image = np.copy(rgb_image)
            height, width, _ = annotated_image.shape
            text_x = landmarks_list[0][x] - 50
            text_y = landmarks_list[0][y] + 35
            if numRaised == ''  or numRaised == 0:
                pass
            elif type(numRaised) is int:
                # 손가락 카운트
                cv2.putText(img = annotated_image, text = str(numRaised) + " Fingers",
                                    org = (text_x, text_y), fontFace = cv2.FONT_HERSHEY_DUPLEX,
                                    fontScale = 0.8, color = (0,0,255), thickness = 1, lineType = cv2.LINE_4)
                
                if self.input_mode == 'fingerCount' and numRaised <= self.input_finger_max:
                    self.finger_repeat_signal.emit(str(numRaised))  # 손가락 인식 결과 신호 발생

            else:
                # 엄지 척
                cv2.putText(img = annotated_image, text = str(numRaised) + "",
                                    org = (text_x, text_y), fontFace = cv2.FONT_HERSHEY_DUPLEX,
                                    fontScale = 0.8, color = (255,255,255), thickness = 1, lineType = cv2.LINE_4)
            
                if self.input_mode =='thumbUpDown':
                    if numRaised == 'Thumb up':
                        self.finger_repeat_signal.emit('O')  # 손가락 인식 결과 신호 발생
                    elif numRaised == 'Thumb down':
                        self.finger_repeat_signal.emit('X')  # 손가락 인식 결과 신호 발생

            # TEST 용
            # if self.input_mode != 'touch':
            #     self.finger_repeat_signal.emit(str(numRaised))  # 손가락 인식 결과 신호 발생

            return annotated_image

        return rgb_image


    def count_fingers(self, landmarks_list):
        x = 0; y = 1
        numRaised = 0
        for i in range(8,21,4): # range(start, stop, step)
            # make sure finger is higher in image the 3 proceeding values (2 finger segments and knuckle)
            # 3가지 진행 값(2개의 손가락 부분과 관절)에서 손가락이 이미지에서 더 높은지 확인하세요.
            tip_y = landmarks_list[i][y]     # 끝 1번째
            dip_y = landmarks_list[i-1][y]   # 끝 2번째
            pip_y = landmarks_list[i-2][y]   # 끝 3번째
            mcp_y = landmarks_list[i-3][y]   # 끝 4번째
            if tip_y < min(dip_y,pip_y,mcp_y):
                numRaised += 1
        # for the thumb (엄지손가락을 위해)
        # use direction vector from wrist to base of thumb to determine "raised"
        # ( 손목에서 엄지손가락 밑부분까지의 방향 벡터를 사용하여 "올려진" 것을 결정합니다.)
        # [4] (엄지 x축 방향만 가지고 판별함.)
        tip_x = landmarks_list[4][x]
        dip_x = landmarks_list[3][x]
        pip_x = landmarks_list[2][x]
        mcp_x = landmarks_list[1][x]
        palm_x = landmarks_list[0][x]    # 손목
        if mcp_x > palm_x:  # _[1].x > _[0].x | 우 방향
            if tip_x > max(dip_x,pip_x,mcp_x):
                numRaised += 1
        else:               # _[1].x > _[0].x | 좌 방향
            if tip_x < min(dip_x,pip_x,mcp_x):
                numRaised += 1

        # 뻑유 손가락 삭제하기 (12, 11, 10, 9) hand landmark
        if numRaised == 1:
            j = 12
            tip_y = landmarks_list[j][y]     # 끝 1번째
            dip_y = landmarks_list[j-1][y]   # 끝 2번째
            pip_y = landmarks_list[j-2][y]   # 끝 3번째
            mcp_y = landmarks_list[j-3][y]   # 끝 4번째
            if tip_y < min(dip_y,pip_y,mcp_y):
                numRaised = 0

        return numRaised


    def key_touch_check(self, frame, landmarks_list):
        x = 0; y = 1
        self.keyTouchSelect = None

        while( len(landmarks_list)>20 ):
        # if len(a) != 0:
            for button in self.buttonlist:   # 모든 버튼list 을 검사
                btn_x, btn_y = button.pos
                btn_width, btn_height = button.size
                finger_x, finger_y = landmarks_list[8][x], landmarks_list[8][y]      # 검지(8) 손가락 위치
                # x2, y2 = landmarks_list[12][p_x], landmarks_list[12][p_y]    # 중지(12) 손가락 위치

                # 집게 손가락 위치에 원 그리기
                #                    위치, 반지름, 색상        ,두께, 빈원
                cv2.circle(frame, ( finger_x, finger_y), 15 , (255, 255, 0), 3, cv2.LINE_AA)

                ## <2> : 검지(8) 손가락 위치 & [버튼] 터치 여부 검사
                if btn_x < finger_x < btn_x+btn_width and btn_y < finger_y < btn_y+btn_height:
                    ''' <키보드 터치 그리기>  검지(8) 터치 [버튼] 색상변경  '''
                    # def draw_key(self, frame, button, rec_color, rec_type, txt_color):
                    self.draw_key(frame, button, (122, 0, 122), -1, (255,255,255))
                    '''                                                  '''

                    # # <2-1> 터치할 경우 입력
                    self.keyTouchSelect = button.text       # 터치된 버튼 저장
                    if self.keyTouchSelectOld == None:      # ** 터치 순간 1회만 입력이 인식한다. **

                        self.key_one_signal.emit(str(button.text))
                        print('key_one_signal.emit =', str(button.text))

            landmarks_list = landmarks_list[21:]
            
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
            # cv2.putText(frame, button.text, (x+BUTTON_TEXT_POS_X+button.font_pos, y+BUTTON_TEXT_POS_Y),cv2.FONT_HERSHEY_SIMPLEX, font_size ,(font_color), 5 , cv2.LINE_AA)   # (255,255,255)
            cv2.putText(frame, button.text, (x+BUTTON_TEXT_POS_X+10+button.font_pos, y+BUTTON_TEXT_POS_Y-10),cv2.FONT_HERSHEY_SIMPLEX, font_size ,(font_color), 2 , cv2.LINE_AA)   # (255,255,255)
        else:
            # cv2.putText(frame, button.text, (x+BUTTON_TEXT_POS_X+10+button.font_pos, y+BUTTON_TEXT_POS_Y-10),cv2.FONT_HERSHEY_SIMPLEX, font_size ,(font_color), 3 , cv2.LINE_AA)   # (255,255,255)
            cv2.putText(frame, button.text, (x+BUTTON_TEXT_POS_X+10+button.font_pos, y+BUTTON_TEXT_POS_Y-10),cv2.FONT_HERSHEY_SIMPLEX, font_size ,(font_color), 2 , cv2.LINE_AA)   # (255,255,255)



    '''  ###################  손가락 카운트 관련  ##########################  '''
    # #########################################################################
    #  m_quiz 에서 호출되어 사용됨
    # #########################################################################
    def input_touchMode(self):
        # 이전 입력모드(self.input_mode )가 1개 손 모드 안에 있다면
        if self.input_mode in self.input_mode_1_hand_list:
        # if self.input_mode != 'touch':     # 'fingerNone', 'fingerCount', 'thumbUpDown' 인 경우
            del self.hands
            self.hands = self.mp_hands.Hands() # max_num_hands=2 : 손 2개 인식
            self.input_mode = 'touch'      # None : 터치 모드로 변경 
        # print('## self.input_mode = ', self.input_mode)

    # FINGER_COUNT_INPUT_MODE
    def input_fingerCount(self, number):
        # 이전 입력모드(self.input_mode )가 1개 손 모드 안에 있다면
        if self.input_mode not in self.input_mode_1_hand_list:
        # if self.input_mode == 'touch' :    # None : 터치 모드인 경우
            del self.hands
            self.hands = self.mp_hands.Hands(max_num_hands=1)   # 손 1개 인식
        self.input_mode = 'fingerCount'
        self.input_finger_max = number
        # print('## self.input_mode = ', self.input_mode)
    
    # FINGER_COUNT_INPUT_MODE
    def input_thumbUpDown(self):
        if self.input_mode not in self.input_mode_1_hand_list:
        # if self.input_mode == 'touch' :    # None : 터치 모드인 경우
            del self.hands
            self.hands = self.mp_hands.Hands(max_num_hands=1)  # 손 1개 인식
        self.input_mode = 'thumbUpDown'
        # print('## self.input_mode = ', self.input_mode)

    # FINGER_COUNT_INPUT_MODE
    def input_fingerNone(self):
        if self.input_mode not in self.input_mode_1_hand_list:
        # if self.input_mode == 'touch' :    # None : 터치 모드인 경우
            del self.hands
            self.hands = self.mp_hands.Hands(max_num_hands=1)  # 손 1개 인식
        self.input_mode = 'fingerNone'
        # print('## self.input_mode = ', self.input_mode)


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
    a.button_ox_create()


    sys.exit(app.exec())