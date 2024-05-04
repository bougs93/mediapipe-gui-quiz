'''
코와 이마를 잇는 각도를 계산하는 방법
https://github.com/google/mediapipe/blob/master/docs/solutions/face_mesh.md
https://developers.google.com/mediapipe/solutions/vision/face_landmarker/
https://developers.google.com/mediapipe/solutions/vision/face_landmarker/python

랜드마크
    https://stackoverflow.com/questions/59782648/get-landmark-points-for-arscnfacegeometry
    https://www.analyticsvidhya.com/blog/2021/07/facial-landmark-detection-simplified-with-opencv/

'''
from PySide6.QtCore import *
from PySide6.QtGui import *
from setup import *

import cv2
import mediapipe as mp
import numpy as np, sys

import math, time

# from setup import *

CAP_DISPLAY_WIDTH = 640
CAP_DISPLAY_HEIGHT = 480
AVERAGE_WINDOW_SIZE = 4

EXTENSION_LEN_RATIO = 0.85   # 길이확장 비율 조절(마인트 위젯 높이 조절)

class Average():
    def __init__(self):
        # movingAverage:
        self.buffer = []
        self.cumulative_sum = 0

    def putData(self, value, window_size):
        self.buffer.append(value)
        self.cumulative_sum += value

        if len(self.buffer) > window_size:
            self.cumulative_sum -= self.buffer.pop(0)

        if len(self.buffer) >= window_size:
            average = self.cumulative_sum / window_size
            return average

        return 0 # None  # 윈도우 크기에 도달하기 전까지는 None을 반환

# #########################################################################
#  ThreadVideo
# #########################################################################
class ThreadFaceTilt(QThread):

    change_pixmap_signal = Signal(np.ndarray)   # 시그널 정의
    fps_signal = Signal(str)
    foreheadxy_angle_signal = Signal(list)
    _started_signal = Signal()                   # thread 실행됨을 알림.

    def __init__(self, frameView_width, frameView_height):
        super().__init__()

        # 기본적으로 외부 장치 선택
        if DEFAULT_CAPTURE_DEVICE == 0:
            self.captureDevice = CAPTURE_DEVICE0
        elif DEFAULT_CAPTURE_DEVICE == 1:
            self.captureDevice = CAPTURE_DEVICE1

        self.frameView_width = frameView_width
        self.frameView_height = frameView_height

        self.averageAngel = Average()
        self.averageX = Average()
        self.averageY = Average()
        self.averageLen = Average()

        self.averageZpos = Average()

        self._started = False    # started_signal = Signal()
    
    # def calculate_eye_chin_position(self, face_landmarks):
    #     # 코와 이마 랜드마크의 인덱스
    #     eye1_landmark_index = 190         # 눈사이 랜드마크 인덱스
    #     eye2_landmark_index = 414         # 
    #     chin1_landmark_index = 0 #17         # 코의 랜드마크 인덱스
    #     chin2_landmark_index = 2 #199        # 175

    #     eye1_landmark = face_landmarks.landmark[eye1_landmark_index]
    #     eye2_landmark = face_landmarks.landmark[eye2_landmark_index]
    #     chin1_landmark = face_landmarks.landmark[chin1_landmark_index]
    #     chin2_landmark = face_landmarks.landmark[chin2_landmark_index]

    #     print(eye1_landmark)
    #     eye1_x = int(eye1_landmark.x * self.frame_width)
    #     eye1_y = int(eye1_landmark.y * self.frame_height)
    #     eye2_x = int(eye2_landmark.x * self.frame_width)
    #     eye2_y = int(eye2_landmark.y * self.frame_height)
    #     chin1_x = int(chin1_landmark.x * self.frame_width)
    #     chin1_y = int(chin1_landmark.y * self.frame_height)
    #     chin2_x = int(chin2_landmark.x * self.frame_width)
    #     chin2_y = int(chin2_landmark.y * self.frame_height)

    #     return (eye1_x, eye1_y), (eye2_x, eye2_y), (chin1_x, chin1_y), (chin2_x, chin2_y)

    # def calculate_length_ratio(self, eye1, eye2, chin1, chin2):
    #     # istance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    #     x = 0
    #     y = 1
    #     eye_distance = math.sqrt((eye2[x] - eye1[x]) ** 2 + (eye2[y] - eye1[y]) ** 2)
    #     chin_distance = math.sqrt((chin2[x] - chin1[x]) ** 2 + (chin2[y] - chin1[y]) ** 2)
    #     # print(int(eye_distance), int(chin_distance))

    #     return round((chin_distance*2)/eye_distance, 2)

    def calculate_forehead_zpos_forward(self, face_landmarks):
        # 코와 이마 랜드마크의 인덱스
        nose_landmark_index = 4         # 코의 랜드마크 인덱스
        forehead_landmark_index = 10    # 10 이마 끝
        # forehead_landmark_index = 151    # 151 이마 중앙

        # 코와 이마 랜드마크의 위치 계산
        nose_landmark = face_landmarks.landmark[nose_landmark_index]
        forehead_landmark = face_landmarks.landmark[forehead_landmark_index]
        
        # 연장선 포인트
        forehead_z =  forehead_landmark.z * 100
        nose_z =  nose_landmark.z * 100
        # 코와 이마의 전체 길이를 계산

        # print(round(forehead_z/nose_z, 2))
        return round(forehead_z/nose_z, 2)
        


    def calculate_forehead_position(self, face_landmarks):
        # 코와 이마 랜드마크의 인덱스
        nose_landmark_index = 4         # 코의 랜드마크 인덱스
        forehead_landmark_index = 10    # 10 이마 끝
        # forehead_landmark_index = 151    # 151 이마 중앙

        # 코와 이마 랜드마크의 위치 계산
        nose_landmark = face_landmarks.landmark[nose_landmark_index]
        forehead_landmark = face_landmarks.landmark[forehead_landmark_index]
        
        # 연장선 포인트
        length_x =  forehead_landmark.x - nose_landmark.x
        length_y =  forehead_landmark.y - nose_landmark.y
        # 코와 이마의 전체 길이를 계산
        length = math.sqrt(length_x**2 + length_y**2)
        # 연장선의 방향을 계산합니다.
        angle = math.atan2(length_y, length_x)
        # 연장선의 포인트를 계산합니다.
        extension_landmark_x = forehead_landmark.x + length*EXTENSION_LEN_RATIO * math.cos(angle)
        extension_landmark_y = forehead_landmark.y + length*EXTENSION_LEN_RATIO * math.sin(angle)

        nose_x = int(nose_landmark.x * self.frame_width)
        nose_y = int(nose_landmark.y * self.frame_height)
        forehead_x = int(forehead_landmark.x * self.frame_width)
        forehead_y = int(forehead_landmark.y * self.frame_height)
        extension_x = int(extension_landmark_x * self.frame_width)
        extension_y = int(extension_landmark_y * self.frame_height)

        return nose_x, nose_y, forehead_x, forehead_y, extension_x, extension_y, length
    
    # def movingAverage(self, value, window_size):
    #     self.buffer.append(value)
    #     self.cumulative_sum += value

    #     if len(self.buffer) > window_size:
    #         self.cumulative_sum -= self.buffer.pop(0)

    #     if len(self.buffer) >= window_size:
    #         average = self.cumulative_sum / window_size
    #         return average

    #     return 0 # None  # 윈도우 크기에 도달하기 전까지는 None을 반환

    def calculate_angle(self, nose_x, nose_y, forehead_x, forehead_y):
        # 코와 이마 사이의 각도 계산
        # dx = forehead_x - nose_x
        # dy = forehead_y - nose_y
        dx = nose_x - forehead_x
        dy = nose_y - forehead_y
        radians = math.atan2(dy, dx)
        angle = math.degrees(radians)

        angle = round(angle, 2)

        return round(angle-90, 2)
    
    def find_foreheadAngle(self, frame):
        # 이미지를 RGB로 변환
        #   frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 얼굴 랜드마크 검출
        #   results = face_mesh.process(frame_rgb)
        results = self.face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        nose_x, nose_y = None, None
        forehead_x, forehead_y = None, None
        extension_x, extension_y = None, None
        angle, length, zpos_forward = None, None, None
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # 코와 이마 위치 계산
                nose_x, nose_y, forehead_x, forehead_y, extension_x, extension_y, length = self.calculate_forehead_position(face_landmarks)

                # 코와 이마 사이의 각도 계산
                angle = self.calculate_angle(nose_x, nose_y, forehead_x, forehead_y)

                # 코와 이마 위치 표시
                # cv2.circle(frame, (nose_x, nose_y), 5, (0, 0, 255), -1)
                # cv2.circle(frame, (forehead_x, forehead_y), 5, (0, 255, 0), -1)
                cv2.circle(frame, (extension_x, extension_y), 5, (255, 0, 0), -1)

                # 각도 표시
                # cv2.putText(frame, f"Angle: {angle}", (forehead_x, forehead_y + 20),
                            # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                # cv2.putText(frame, f"Angle: {angle}", (nose_x, nose_y + 20),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                zpos_forward = self.calculate_forehead_zpos_forward(face_landmarks)
                #----------------------------------------------------------------
                # TEXT 표시 : 코 옆에 표시
                # cv2.putText(frame, f"Angle: {angle}, Ratio: {zpos_forward}", (nose_x, nose_y + 20),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                #----------------------------------------------------------------
                # TEXT 표시 : 화면 좌측
                # 각도 표시
                txt_size = 0.4
                w = 5
                l = 14 #int(self.frame_height/30)
                h = int(self.frame_height/2)
                COR_NONE = (0, 255, 0)   #주의 RGB - BGR 순서 green 
                COR_ACT = (0, 81, 230)   # red (230, 81, 0) -> (0, 230, 81)
                ang_cor_none = (0, 255, 0) 
                ang_cor_act = (0, 255, 0) 
                ratio_cor_none = (0, 255, 0) 
                ratio_cor_act = (0, 255, 0) 
                
                if abs(angle) < ANGLE_NONE:
                    ang_cor_none = COR_ACT
                    ang_cor_act = COR_NONE
                elif abs(angle) > ANGLE_ANSWER:
                    ang_cor_none = COR_NONE
                    ang_cor_act = COR_ACT

                if abs(zpos_forward) < ZPOS_FORWARD_NONE:
                    ratio_cor_none = COR_ACT
                    ratio_cor_act = COR_NONE
                elif abs(zpos_forward) > ZPOS_FORWARD_ANSWER:
                    ratio_cor_none = COR_NONE
                    ratio_cor_act = COR_ACT

                # angel
                cv2.putText(frame, f"Angle: {angle}", (w, h),
                            cv2.FONT_HERSHEY_SIMPLEX, txt_size, COR_NONE, 1)
                cv2.putText(frame, f"  NONE: {ANGLE_NONE}", (w, h+l),
                            cv2.FONT_HERSHEY_SIMPLEX, txt_size, ang_cor_none, 1)
                cv2.putText(frame, f"  ACT : {ANGLE_ANSWER}", (w, h+2*l),
                            cv2.FONT_HERSHEY_SIMPLEX, txt_size, ang_cor_act, 1)
                # forward
                cv2.putText(frame, f"Forward: {zpos_forward}", (w, h+3*l), 
                            cv2.FONT_HERSHEY_SIMPLEX, txt_size, COR_NONE, 1)
                cv2.putText(frame, f"  NONE: {ZPOS_FORWARD_NONE}", (w, h+4*l),
                            cv2.FONT_HERSHEY_SIMPLEX, txt_size, ratio_cor_none, 1)
                cv2.putText(frame, f"  ACT : {ZPOS_FORWARD_ANSWER}", (w, h+5*l),
                            cv2.FONT_HERSHEY_SIMPLEX, txt_size, ratio_cor_act, 1)
                # length
                cv2.putText(frame, f"length : {round(length, 2)}", (w, h+6*l),
                            cv2.FONT_HERSHEY_SIMPLEX, txt_size, ratio_cor_act, 1)

            # cv2.imshow('Face Landmarks', frame)
        # 에러: 검출 값이 없다면
        return extension_x, extension_y, angle, length, zpos_forward, nose_x
    
    def convert_cv2qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # >> 화면 전체 프레임 채우기 <<
        p = convert_to_Qt_format.scaled(self.frameView_width, self.frameView_height, Qt.KeepAspectRatio)
        # p = convert_to_Qt_format.scaled(self.frame_width, self.frame_width, Qt.KeepAspectRatio)
        
        # 랜드마크 포인터 계산을 위함.
        self.QmapViewSize = p.size()    

        return QPixmap.fromImage(p)
        # return QPixmap.fromImage(convert_to_Qt_format)


    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.quit()
        self.wait(5000)


    def run(self):
        self._run_flag = True

        mp_drawing = mp.solutions.drawing_utils
        mp_face_mesh = mp.solutions.face_mesh

        # Face Mesh 모델 초기화
        self.face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

        # 카메라 열기
        cap = cv2.VideoCapture(self.captureDevice)

        # <1> 캡쳐 사이즈 결정
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAP_DISPLAY_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAP_DISPLAY_HEIGHT)

        prevTime = 0 #frame 계산 : 이전 시간을 저장할 변수
        while self._run_flag:
            # 프레임 읽기
            success, frame = cap.read()
            if not success:
                break

            # 이미지 크기 얻기
            self.frame_height, self.frame_width, _ = frame.shape
            if prevTime == 0 : 
                print('capture size =', self.frame_width ,'*', self.frame_height)

            ######################## 프레임 수계산하기 #######################
            curTime = time.time() # 현재 시간 가져오기 (초단위로 가져옴)
            sec = curTime - prevTime
            prevTime = curTime
            fps = 1/(sec)               # 1 / time per frame
            fps_str = "FPS : %0.1f" % fps    # 프레임 수를 문자열에 저장
            self.fps_signal.emit(fps_str)
            ################################################################

            frame = cv2.flip(frame, flipCode = 1)                 # 셀프 카메라처럼 좌우 반전

            extension_x, extension_y, angle, length, zpos_forward, nose_x = self.find_foreheadAngle(frame)

            if self._started == False:   # 비디오 쓰레드가 실행되어 준비됨을 알림.
                self._started = True
                self._started_signal.emit()
                self._started
            qt_img = self.convert_cv2qt(frame)
            self.change_pixmap_signal.emit(qt_img)

            # x, y 좌표와, 각도를 전달
            ratio_x = self.QmapViewSize.width() / self.frame_width
            ratio_y = self.QmapViewSize.height() / self.frame_height

            if not (extension_x == None or extension_y == None ):
                extension_x = int(extension_x * ratio_x)
                extension_y = int(extension_y * ratio_y)

                extension_x = self.averageX.putData(extension_x, AVERAGE_WINDOW_SIZE)
                extension_y = self.averageY.putData(extension_y, AVERAGE_WINDOW_SIZE)
                angle = round(self.averageAngel.putData(angle, AVERAGE_WINDOW_SIZE), 2)
                length = self.averageLen.putData(length, AVERAGE_WINDOW_SIZE)

                nose_x = int (nose_x * ratio_x)
            
            if zpos_forward != None:
                zpos_forward = self.averageZpos.putData(zpos_forward, AVERAGE_WINDOW_SIZE)
                
            self.foreheadxy_angle_signal.emit([extension_x, extension_y, angle, length, zpos_forward, nose_x])

            ########### 테스트용 #############################
            if __name__=="__main__":
                cv2.imshow('frame',frame)
                k = cv2.waitKey(1)
                # 종료
                if k == ord('q'):
                    break
            ########### 테스트용 #############################
        # 자원 해제
        cap.release()

if __name__=="__main__":
    from PySide6.QtWidgets import *

    app = QApplication(sys.argv)
    a = ThreadFaceTilt(640, 480)

    a.start()
    sys.exit(app.exec())