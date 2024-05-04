'''
640* 480 해상도 사용
2024.02.26
    mediapipe.tasks.vision.HandLandmarker 이용한 손 인식 ( 2024. 업데이트 된 0.10.10 )

    https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
    https://github.com/google/mediapipe
    
    [결과] 사용 보류
    mediapipe.solutions.hands 방식보다 40% 정도 느리고, 인식률도 매우 떨어짐.
    (1) 랜드마크가 비동기 방식으로 전달되어서 기존 방식보다 결과 프레임이 느림
    (2) 랜드마크 인식률이 매우 떨어짐.
    아직, Python macOS, Linux 만 GPU 지원함. 윈도우 GPU 미지원


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
from mediapipe.framework.formats import landmark_pb2

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
        # # find_postion(self, frame) / MediaPipe 패키지에서 사용할 기능들.
        # self.mp_drawing = mp.solutions.drawing_utils
        # self.mp_drawing_styles = mp.solutions.drawing_styles
        # self.mp_hands = mp.solutions.hands           # 손 인식을 위한 객체
        # self.hands = self.mp_hands.Hands()           # 손 인식 객체 생성
        ##################################################################
        # NEW
        self.result = mp.tasks.vision.HandLandmarkerResult    # 결과
        self.landmarker = mp.tasks.vision.HandLandmarker      # 랜드마크
        self.createLandmarker()                               # 초기화 함수

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

    # NEW
    def createLandmarker(self):
        
        # callback function 콜백 함수 (비동기식 처리)
        def update_result(result: mp.tasks.vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
            ######################## 프레임 수계산하기 #######################
            curTime = time.time() # 현재 시간 가져오기 (초단위로 가져옴)
            sec = curTime - self.prevTime
            self.prevTime = curTime
            fps = 1/(sec)               # 1 / time per frame
            fps_str = "FPS : %0.1f" % fps    # 프레임 수를 문자열에 저장
            self.fps_signal.emit(fps_str)
            ################################################################
            self.result = result

        # HandLandmarkerOptions (details here: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker/python#live-stream)
        # gpu 미지원 https://github.com/google/mediapipe/issues/5126
        options = mp.tasks.vision.HandLandmarkerOptions( 
            base_options = mp.tasks.BaseOptions(model_asset_path="hand_landmarker.task"), # path to model (running_mode 모델 경로) # , delegate=mp.tasks.BaseOptions.Delegate.GPU <- python 윈도우 미지원
            running_mode = mp.tasks.vision.RunningMode.LIVE_STREAM, # running on a live stream (라이브 스트림에서 실행)
            num_hands = 2, # track both hands (양손 추적)
            min_hand_detection_confidence = 0.3, # lower than value to get predictions more often (더 자주 예측을 얻으려면 값보다 낮음)
            min_hand_presence_confidence = 0.3, # lower than value to get predictions more often (더 자주 예측을 얻으려면 값보다 낮음 종종)
            min_tracking_confidence = 0.3, # lower than value to get predictions more often (더 자주 예측을 얻으려면 값보다 낮음)
            result_callback = update_result) # result_callback 인수로 전달하는 함수에 결과를 제공 *비동기적 수신처리
        
        # initialize landmarker (랜드마크 초기화)
        self.landmarker = self.landmarker.create_from_options(options)  

    # NEW
    # 실제로 라이브 스트림의 각 이미지에 대한 랜드마크 감지를 실행
    def detect_async(self, frame):
        # convert np frame to mp image (np 프레임을 mp 이미지로 변환)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # detect landmarks (랜드마크 감지)
        self.landmarker.detect_async(image = mp_image, timestamp_ms = int(time.time() * 1000))

    # NEW
    def close(self):
        # close landmarker
        self.landmarker.close()
     
    # NEW
    def draw_landmarks_on_image(self, rgb_image, detection_result: mp.tasks.vision.HandLandmarkerResult):
        """Courtesy of https://github.com/googlesamples/mediapipe/blob/main/examples/hand_landmarker/python/hand_landmarker.ipynb"""
        try:
            if detection_result.hand_landmarks == []:
                return rgb_image
            else:
                hand_landmarks_list = detection_result.hand_landmarks
                handedness_list = detection_result.handedness
                annotated_image = np.copy(rgb_image)

                # Loop through the detected hands to visualize.
                for idx in range(len(hand_landmarks_list)):
                    hand_landmarks = hand_landmarks_list[idx]
                    
                    # Draw the hand landmarks.
                    hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
                    hand_landmarks_proto.landmark.extend([
                    landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks])
                    mp.solutions.drawing_utils.draw_landmarks(
                    annotated_image,
                    hand_landmarks_proto,
                    mp.solutions.hands.HAND_CONNECTIONS,
                    mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                    mp.solutions.drawing_styles.get_default_hand_connections_style())

                return annotated_image
        except:
            return rgb_image

    # NEW
    def count_fingers_raised(self, rgb_image, detection_result: mp.tasks.vision.HandLandmarkerResult):

        touchFingers = []
        _touchFingers = []  # 임시 [0.1, 0.2]
        # self.result = mediapipe.tasks.vision.HandLandmarkerResult

        """Iterate through each hand, checking if fingers (and thumb) are raised.
        Hand landmark enumeration (and weird naming convention) comes from
        https://developers.google.com/mediapipe/solutions/vision/hand_landmarker."""
        try:
            # Get Data
            hand_landmarks_list = detection_result.hand_landmarks
            # Counter
            numRaised = 0
            # for each hand... | len(hand_landmarks_list) = 손의 갯수 | 미인식=0, 한손=1, 두손=2
            for idx in range(len(hand_landmarks_list)):
                # hand landmarks is a list of landmarks where each entry in the list has an x, y, and z in normalized image coordinates
                # ( 손 랜드마크는 목록의 각 항목이 정규화된 이미지 좌표에 x, y, z를 갖는 랜드마크 목록입니다. )
                hand_landmarks = hand_landmarks_list[idx] # 21개의 랜드마크가 들어 있음.
                # for each fingertip... (hand_landmarks 4, 8, 12, and 16)
                # 8, 12, 16, 20 (엄지 제외, y축 방향만 가지고 판별함)
                for i in range(8,21,4):
                    # make sure finger is higher in image the 3 proceeding values (2 finger segments and knuckle)
                    tip_y = hand_landmarks[i].y
                    dip_y = hand_landmarks[i-1].y
                    pip_y = hand_landmarks[i-2].y
                    mcp_y = hand_landmarks[i-3].y
                    if tip_y < min(dip_y,pip_y,mcp_y):
                        numRaised += 1
                # for the thumb
                # use direction vector from wrist to base of thumb to determine "raised"
                # ( 손목에서 엄지손가락 밑부분까지의 방향 벡터를 사용하여 "올려진" 것을 결정합니다.)
                # [4] (엄지 x축 방향만 가지고 판별함.)
                tip_x = hand_landmarks[4].x
                dip_x = hand_landmarks[3].x
                pip_x = hand_landmarks[2].x
                mcp_x = hand_landmarks[1].x
                palm_x = hand_landmarks[0].x
                if mcp_x > palm_x:
                    if tip_x > max(dip_x,pip_x,mcp_x):
                        numRaised += 1
                else:
                    if tip_x < min(dip_x,pip_x,mcp_x):
                        numRaised += 1

                # 집게 손가락 SAVE
                _touchFingers.append([hand_landmarks[8].x, hand_landmarks[8].y, hand_landmarks[8].z])

            # display number of fingers raised on the image
            # (이미지 위에 올려진 손가락 수 표시)
            annotated_image = np.copy(rgb_image)
            height, width, _ = annotated_image.shape
            text_x = int(hand_landmarks[0].x * width) - 10
            text_y = int(hand_landmarks[0].y * height) + 35
            cv2.putText(img = annotated_image, text = str(numRaised) + "",
                                org = (text_x, text_y), fontFace = cv2.FONT_HERSHEY_DUPLEX,
                                fontScale = 1, color = (0,0,255), thickness = 2, lineType = cv2.LINE_4)
            
            # 집게 손가락 좌표로 변환, 리턴 리스트에 저장
            for idx in range(len(_touchFingers)):
                touchFingers.append([int(_touchFingers[idx][0]*width), int(_touchFingers[idx][1]*height)])

            return annotated_image, touchFingers
        except:
            return rgb_image, touchFingers


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

        # new
        # create landmarker (객체를 초기화)
        # hand_landmarker = landmarker_and_result()

        # prevTime = 0 #frame 계산 : 이전 시간을 저장할 변수
        self.prevTime = 0 #frame 계산 : 이전 시간을 저장할 변수
        while self._run_flag:

            ret, frame = cap.read() # 카메라 데이터 읽기
            # print('frame : ', type(frame))
            h, w, c = frame.shape
            # if prevTime == 0 : 
            #     print('capture size =',w ,'*', h)

            # ######################## 프레임 수계산하기 #######################
            # curTime = time.time() # 현재 시간 가져오기 (초단위로 가져옴)
            # sec = curTime - prevTime
            # prevTime = curTime
            # fps = 1/(sec)               # 1 / time per frame
            # fps_str = "FPS : %0.1f" % fps    # 프레임 수를 문자열에 저장
            # self.fps_signal.emit(fps_str)
            # self.fps_signal.emit('')
            # ################################################################

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

                frame = cv2.flip(cv_frame, flipCode = 1)                 # 셀프 카메라처럼 좌우 반전
                # cv_frame = cv2.resize(cv_frame, (PIPE_DISPLAY_WIDTH, PIPE_DISPLAY_HEIGHT))  # 과정을 거치면 비율이 변함
                # cv2.putText(cv_frame, fps_str, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),1) # frame 표시

                # new
                # 1. update landmarker results
                self.detect_async(frame)
                # new
                # 2 draw landmarks on frame
                frame = self.draw_landmarks_on_image(frame, self.result)
                # new
                # count number of fingers raised
                frame, touchFingers = self.count_fingers_raised(frame, self.result)

                # <2> 터치버튼 모두 그리기 #
                frame = self.draw_all_keys(frame, self.buttonlist)    # [_]버튼 모두 그리기

                # <3> 터치 그리기 및 손 키보드 검사
                self.draw_touch_check(frame, touchFingers)

                ########### 테스트용 #############################
                if __name__=="__main__":
                    cv2.imshow('frame',frame)
                    if cv2.waitKey(1) == ord('q'):
                        break
                ########### 테스트용 #############################
                    
                qt_img = self.convert_cv2qt(frame)

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


    def find_postion(self, rgb_image, detection_result: mp.tasks.vision.HandLandmarkerResult):
        w = PIPE_DISPLAY_WIDTH
        h = PIPE_DISPLAY_HEIGHT

        list=[]
        # self.result = mediapipe.tasks.vision.HandLandmarkerResult
        try:
            # Get Data
            hand_landmarks_list = detection_result.hand_landmarks
            # Counter
            numRaised = 0
            # for each hand..
            # for each hand...
            for idx in range(len(hand_landmarks_list)):
                # hand landmarks is a list of landmarks where each entry in the list has an x, y, and z in normalized image coordinates
                hand_landmarks = hand_landmarks_list[idx]
                # for each fingertip... (hand_landmarks 4, 8, 12, and 16)
                for i in range(8,21,4):
                    # make sure finger is higher in image the 3 proceeding values (2 finger segments and knuckle)
                    tip_y = hand_landmarks[i].y
                    dip_y = hand_landmarks[i-1].y
                    pip_y = hand_landmarks[i-2].y
                    mcp_y = hand_landmarks[i-3].y
                    if tip_y < min(dip_y,pip_y,mcp_y):
                        numRaised += 1

                # for the thumb (엄지손가락을 위해)
                # use direction vector from wrist to base of thumb to determine "raised"
                tip_x = hand_landmarks[4].x
                dip_x = hand_landmarks[3].x
                pip_x = hand_landmarks[2].x
                mcp_x = hand_landmarks[1].x
                palm_x = hand_landmarks[0].x    # 손목
                if mcp_x > palm_x:  # _[1].x > _[0].x | 우 방향
                    if tip_x > max(dip_x,pip_x,mcp_x):
                        numRaised += 1
                else:               # _[1].x > _[0].x | 좌 방향
                    if tip_x < min(dip_x,pip_x,mcp_x):
                        numRaised += 1

            # display number of fingers raised on the image
            annotated_image = np.copy(rgb_image)
            height, width, _ = annotated_image.shape
            text_x = int(hand_landmarks[0].x * width) - 100
            text_y = int(hand_landmarks[0].y * height) + 50
            cv2.putText(img = annotated_image, text = str(numRaised) + " Fingers Raised *",
                                org = (text_x, text_y), fontFace = cv2.FONT_HERSHEY_DUPLEX,
                                fontScale = 1, color = (0,0,255), thickness = 2, lineType = cv2.LINE_4)
            return annotated_image
        except:
            return rgb_image


            # multi_hand_landmarks 손의 주요 부분에 대한 x,yz정보를 리스트 형태도 담고 있음
            # index를 사용하여 해당 부분에 접근이 가능함.
            print(self.result.multi_hand_landmarks)
            for handLandmarks in result.multi_hand_landmarks:          # 반복문을 활용해 인식된 손의 주요 부분을 그림으로 그려 표현
                self.mp_drawing.draw_landmarks(
                    rgb_image,                              # 프레임
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
        # except:
        #     return list 
# COLOR = (255, 255, 0) # BGR : 옥색
# RADIUS = 50     # 반지름
# THICKNESS = 10  # 두께

# #         그릴위치, 원의 중심점, 반지름, 색깔, 두께, 선 종류
# cv2.circle(img, (200, 100), RADIUS, COLOR, THICKNESS, cv2.LINE_AA)  # 속 빈 원

    def draw_touch_check(self, frame, touchFingers):
        self.keyTouchSelect = None

        # while( len(touchFingers) > 0 ):
        if len(touchFingers) == 0:
            return
        for touchFinger in touchFingers:
        # if len(a) != 0:
            for button in self.buttonlist:   # 모든 버튼list 을 검사
                x, y = button.pos
                w, h = button.size
                x1, y1 = touchFinger[0], touchFinger[1]      # 검지(8) 손가락 위치
                # x2, y2 = a[12][1], a[12][2]    # 중지(12) 손가락 위치

                # 집게 손가락 위치에 원 그리기
                #                    위치, 반지름, 색상        ,두께, 빈원
                cv2.circle(frame, ( x1, y1), 15 , (255, 255, 0), 3, cv2.LINE_AA)


                ## <1> : 손가락 거리 계산
                # length = math.hypot(x2-x1, y2-y1)    # 중지(12)-검지(8): 사이 거리계산
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

            # a = a[21:]
            
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