
import cv2

from ini_file import *

# ini_file.setupIni_load()
setupIni_load()

# #########################################################################
DEFAULT_CAPTURE_DEVICE = ini['default_capture_deive'] # 1
# CAPTURE_DEVICE0 = ini['caputre_device_0'] # cv2.CAP_DSHOW+0    # 내부 카메라
CAPTURE_DEVICE0 = cv2.CAP_DSHOW+0    # 내부 카메라
# CAPTURE_DEVICE = 0    # 내부 카메라

# CAPTURE_DEVICE1 = ini['caputre_device_1'] # cv2.CAP_DSHOW+1    # 외부 카메라
CAPTURE_DEVICE1 = cv2.CAP_DSHOW+1    # 외부 카메라

# #########################################################################


# #########################################################################

# 켭처 사이즈 / 영상처리 사이즈
# (0) defalut
# CAP_DISPLAY_WIDTH = 640 ; CAP_DISPLAY_HEIGHT = 480    # 480p       - 15 프레임 이하
# PIPE_DISPLAY_WIDTH = 840 ; PIPE_DISPLAY_HEIGHT = 631  # 1.33

# (1) 2023.09.09 설정 
# CAP_DISPLAY_WIDTH = 1280 ; CAP_DISPLAY_HEIGHT = 720   # 720p / 1.33  - 10 프레임 이하
# PIPE_DISPLAY_WIDTH = 1280 ; PIPE_DISPLAY_HEIGHT = 720  # 1.33

# PIPE_DISPLAY_WIDTH = 840 ; PIPE_DISPLAY_HEIGHT = 631  # 1.33


# (2)
# CAP_DISPLAY_WIDTH = 960 ; CAP_DISPLAY_HEIGHT = 540      # 540p / 1.77  - 10 프레임 정도 
# PIPE_DISPLAY_WIDTH = 718 ; PIPE_DISPLAY_HEIGHT = 540    # 1.33

# (3)
# CAP_DISPLAY_WIDTH = 640 ; CAP_DISPLAY_HEIGHT = 480   # 720p / 1.33  - 10 프레임 이하
# PIPE_DISPLAY_WIDTH = 840 ; PIPE_DISPLAY_HEIGHT = 631  # 1.33

# CAP_DISPLAY_WIDTH = 720 ; CAP_DISPLAY_HEIGHT = 480      # 480p / 1.24   - 20 프레임 정도


# 영상 처리를 위한 사이즈

# PIPE_DISPLAY_WIDTH = 1280 ; PIPE_DISPLAY_HEIGHT = 720      # 1.33
# PIPE_DISPLAY_WIDTH = 960 ; PIPE_DISPLAY_HEIGHT = 540       # 1.33

# #########################################################################


# #########################################################################
RANKING_EXHIBITION_MODE = True   # exhibition (전시관) 모드, 일반 모드 선택
# #########################################################################
DB_PATH = './db/'
DB_SCHOOL_FILE = 'school_database.db'
DB_EXHIBITION_FILE = 'exhibition_database.db'

# 데이터 베이스 선택
if not RANKING_EXHIBITION_MODE:
    # 일반 학교 퀴즈 모드
    DB_BASE_FILE = DB_SCHOOL_FILE
else:
    # 전시관 퀴즈 모드인 경우
    DB_BASE_FILE = DB_EXHIBITION_FILE


# #########################################################################
## m_start_wait.py
RANKING_PATH = './quiz/'
RANKING_POST_NAME = "_ranking"                  # 랭킹 파일 뒷글자
RANKING_EXHIBITION_POST_NAME = "_ranking_exhibition"   # 랭킹 exhibition 모두 파일 뒷글자
RANKING_FILE_EXT = 'json'               # 랭킹 파일 확장자
HOW_TO_RESET_RANKING = ini['how_to_reset_ranking']                  # 1일에 랭킹 파일을 리셋함.

print('HOW_TO_RESET_RANKING =', HOW_TO_RESET_RANKING)

TIMER_MAIN_INTERVER = 3000
# #########################################################################

WAV_PATH ='./effects/'

WAV_FILE = ['0.wav','1.wav','2.wav','3.wav','4.wav','5.wav','6.wav','7.wav','8.wav','9.wav',
    'yes.wav','no.wav','pass.wav','quit.wav', 'o.wav', 'x.wav', 'start.wav', 'quiz_start.wav', 'quiz_ticktock.wav', 'quiz_end.wav',
    'quiz_correct.wav','quiz_wrong.wav', 'quiz_pass.wav', 'quiz_ready.wav', 'ok.wav' ]

WAV_DIC = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
    'YES':10, 'NO':11, 'PASS':12, 'QUIT':13, 'O':14,'X':15, 'START':16, 'Q_START': 17, 'Q_TICKTOCK': 18, 'Q_END': 19,
    'Q_CORRECT': 20, 'Q_WRONG': 21, 'Q_PASS': 22, 'Q_READY': 23, 'OK':24}

WAV_LOOP_FILE = ['quiz_ticktock1.wav', 'quiz_ticktock2.wav' ]
WAV_LOOP_DIC  = {'ticktock1':0, 'ticktock2':1 }


##################################################### 
IMG_PATH = './image/'
IMG_TITLE_DEFALUT_FILE = 'title_default.png'

IMG_TITLE_XY = ini['title_img_pos_xy']
IMG_TITLE_SIZE = ini['title_img_size']
# print(f'IMG_TITLE_XY = {IMG_TITLE_XY} , IMG_TITLE_SIZE = {IMG_TITLE_SIZE}')

IMG_HAND_FILE = 'icon_hand.png'

IMG_MODE_FINGER_COUNT5_FILE = 'mode_fingerCount5.png'
IMG_MODE_FINGER_COUNT4_FILE = 'mode_fingerCount4.png'
IMG_MODE_FINGER_COUNT3_FILE = 'mode_fingerCount3.png'
IMG_MODE_FINGER_COUNT2_FILE = 'mode_fingerCount2.png'
IMG_MODE_FINGER_COUNT1_FILE = 'mode_fingerCount1.png'
IMG_MODE_FINTER_THUMB_FILE = 'mode_thumbUpDown.png'
IMG_MODE_TOUCH = 'mode_touch.png'


IMG_FACE_FILE = 'icon_my_face.png'
IMG_FACE_FILE_XY = ini['icon_face_image_pos_xy']
IMG_FACE_FILE_SIZE = ini['icon_img_size']

## xlsx_id_load.py
ID_PATH = './user/'
ST_ID_FILE = 'student_id.xlsx'
TE_ID_FILE = 'teacher_id.xlsx'
# STUDENT_ID_MAX = 4  # 학번 최대자릿수 2318
STUDENT_ID_MAX =ini['user_id_max']

# TEMP_PATH 위치에서 생성됨.
TEMP_ID_FILE = 'temp_id.xlsx'

# LOG 파일 경로
LOG_PATH = './log/' 



##################################################### 
'''
 -> quiz*.xlsx
day_seq     : 날짜별로  순차적으로 문제 선택
day_random  : 날짜별로  랜덤으로   문제 선택

seq     : 문제 끝날때 마다 순차적으로 문제 선택
random  : 문제 끝날때 마다 랜덤으로   문제 선텍

 -> gradequiz0.xlsx  - 일반 문제 / gradequiz1.xlsx  - 1학년 문제 / gradequiz2.xlsx  - 2학년 문제
grade   : 학년별 문제 선택
학번으로 퀴즈 선택

'''
QUIZ_SELECT_MODE = ini['quiz_select_mode']  # 'day_seq'  # 퀴즈가 매일 순서대로 변경됨.
# QUIZ_SELECT_MODE = ''       # 매일 퀴즈 순서 변경없음. 동일한 퀴즈가 매일 동일하게 시작됨


## xlsx_quiz_load.py
QUIZ_PATH = './quiz/'
QUIZ_FILE = 'quiz_bank.xlsx'
QUIZ_NAME_LIST = 'quiz_name_list.txt'

# xlsx_quiz_load / m_quiz.py
# TEMP_PATH = './temp/'
QUIZ_RANDOM_FILE = 'user_quiz.xlsx'   # 문제 순서 섞기 파일
QUIZ_USER_FILE_START_ROW = 4

# ## 시작버튼 setInterval
# STARTING_TIME_END = 2000    # msec
# STARTING_INTERVAL = 100

# 전환시 화면 멈춘 현상 방지를 위해서 테스트[확인 요망]
# _main. display_ConnectChange, display_2ConnectChange
# display_QuizMental_slot, display_Quiz_slot
#   에서 화면 전화시 멈춤현상을 방지하기 위해서 disconnect 후, connect 하기 전 지연시간
DISPLAY_CHANGE_DELAY = 200      # MS

##################################################### 
# 일정시간 누름이 발생해야 동작하는 키버튼 정의 : OK, QUIT, START
PRESS_KEY_DELAY_LIST = {'OK', 'QUIT', 'START'}

# KeyPressTimer.py
KEY2_RESPOSE_TIME_OUT = 0.5  # 키입력 신호의 타임아웃 시간 (초)
KEY2_TIMER_INTERVAL = 100    # 타이머 간격 ms
KEY2_PUSH_TIME = 1000        # 누르는 대기시간 ms


# 사용자 정의 circular_progress 용도.
# # key type3 [START] 버튼 / self.startPresKey
# KEY3_RESPOSE_TIME_OUT = 0.2  # 키입력 신호의 타임아웃 시간 (초) 
#    -> thread_video 응답 fps 마다 time_out 시간이 다르게 되는 문제가 있어
#       val.key3_respose_time_out + KEY3_RESPOSE_TIME_OUT_ADD 값으로 변경함.
KEY3_RESPOSE_TIME_OUT_ADD = 0.1
KEY3_TIMER_INTERVAL = 50     # 100  # 타이머 간격 ms
KEY3_PUSH_TIME = 800         # 1200 # 누르는 대기시간 ms 
KEY3_VIEW_DELAY = 800        # 1000 # 푸쉬완료후 화면에 보여주는 시간 ms


# NEW
# # 손가락 카운터 진행용도 FINGER
FINGER_RESPOSE_TIME_OUT = 0.2  # 키입력 신호의 타임아웃 시간 (초)
FINGER_TIMER_INTERVAL = 50     # 100  # 타이머 간격 ms
FINGER_PUSH_TIME = 400         # 1200 # 누르는 대기시간 ms 
FINGER_VIEW_DELAY = 400        # 1000 # 푸쉬완료후 화면에 보여주는 시간 ms


# 학생 학번 파일이름
# STUEDNT_FILE = "student_id.xlsx"

# 새로운 퀴즈 또는 화면 전환시 버튼을 지우고 다시 보여주는 지연 시간
# VIDEO_BTN_REFLASH_DELAY = 700    # 1000
VIDEO_BTN_REFLASH_DELAY = ini['video_button_reflash_delay_ms']

# 정보       문제카운트   문제번호    정답       응답       채점       시간ms     입력방법: (T)터치/(C)카운터/(F)얼굴기울림
R_INFO = 0 ; R_QCNT = 1; R_QNUM = 2; R_ANS =3 ;R_RES = 4; R_RWP = 5; R_TIME = 6; R_HOTO = 7
# 동일한 퀴즈 사용자 몇번째 풀이
R_QREP = 8


######################################################
#  XLSX_QUIZ_파일 로딩 xlsx_quiz_load.py
Q_AREA_NAME = [1, 4]        # 퀴즈 제목 셀 위치
Q_TIME = [2, 4]             # 퀴즈 제한 시간 셀 위치
Q_TITLE_IMAGE = [3, 4]      # 퀴즈 이미지 쉘 위치
Q_QUIZ_MODE = [4, 4]        # 퀴즈 모드 셀 위치
                                #   mental arithmetic = 기울여 암산
                                #   word quiz = 영단어 퀴즈
Q_QUIZ_OPTION1 = [3, 6]     # 퀴즈 옵션1 셀 위치 | mental arithmetic -레벨 반복 횟수
Q_QUIZ_OPTION2 = [4, 6]     # 퀴즈 옵션2 셀 위치 | mental arithmetic -랜덤 시작 레벨

Q_QUIZ_MODE_WORD_AFTER = [4, 7] # "word quiz = 영단어 퀴즈" 시 질문 문장



QTIMER_INTERVAL = 500
QUIZ_TYPE = 'speed'  # golden, speed
# QUIZ_TIME_GOLDEN =  '00:20'   # golden | 골든벨 퀴즈 1문제 제한 시간 30초
SPEED_QUIZ_DEFAULT_TIME  = ini['speed_quiz_default_time'] # '2:00'   # speed  | 제한시간 스피드 퀴즈
SPEED_QUIZ_WARNING1_TIME = ini['speed_quiz_warning1_time'] # '0:30'    # 남은 시간이 1차 경고. 틱톡음
SPEED_QUIZ_WARNING2_TIME = ini['speed_quiz_warning2_time'] # '0:10'    # 남은 시간이 2차 경고. 빠른 틱톡음

QUIZ_RESULT_DELAY_TIME = 500   # 퀴즈 보여주기 전 지연 시간
QUIZ_RESULT_VIEW_TIME = 1000   # 퀴즈 결과 보여줄 시간

# m_user_reg 키입력 없으면 초기화면으로
REG_KEY_TIME_OUT = ini['quiz_reg_time_out'] # '20' # 초단위


# 퀴즈 풀이 점수 방법
Q_ANSWER_SCORE = ini['answer_score']    # 10
Q_WRONG_SCORE = ini['wrong_score']      # -10
Q_PASS_SCORE = ini['pass_score']        # -5

# 문제코드 숨기기 여부
Q_CODE_VIEW = True      # True, False

# 퀴즈 문제 풀이시 하단에 답 표시 [테스트용]
Q_TEST_HINT = ini['quiz_test_hint']

# 퀴즈 END TIME
QUIZ_END_VIEW_TIME = ini['quiz_end_view_time'] # '30'   # 초단위만 입력

### ranking table widtet
RA_RANK = 0; RA_SCORE=1; RA_TOTAL=2; RA_ID=3; RA_NAME=4; RA_DTIME=5

### ranking_table_view.py ####
RANK_TABLE_VIEW_INTERVAL = 500

### thread_sound.py ###
MUSUC_PATH = './music/'
MUSIC_VOLUME = 0.3          # Pyside6 Max = 1.0, min  = 0.0
# MUSIC_VOLUME_SAVE_MIN = 0.1   # -> ini_file.py 
MUSIC_ALL_PLAY = True      # False: 음악 1회만 재생, True: 무한 반복 재생

### 버전 정보 #####
# m_start_wait.py
PROGRAM_VER = 'v3.1-24.04.02'
QUIZ_VER = ''
PROGRAM_DEVELOPER = 'Won-gil Jeong'

### start wiat quiz 메시지 표시시간 ###
MSG_CMD_TIME = 1500
MUSIC_NEXT_DELAY_TIME = 500


## 문제, 부정문 밑줄 칠 단어 ##
# UNDERLINE_WORDS = ['아닌','못한','않은','not','Not']
UNDERLINE_WORDS = ini['question_underline_words']
# print(f'\n UNDERLINE_WORDS = {UNDERLINE_WORDS}, {type(UNDERLINE_WORDS)} \n')

### 퀴즈 에서 - 손가락카운트 /버튼 터치 모드 여부 결정
FINGER_COUNT_INPUT_MODE = True

############################################
# 이미지 변환 관련 xls_quiz_load.py , m_quiz.py

TEMP_PATH = './temp/'
Q_IMAGE_W = 511     # 511, 331
Q_IMAGE_H = 331     # 511, 331
XLS_CELL_W = 9.3
XLS_CELL_H = 50

ROW_ = 0
COL_ = 1
IN_FILE = 0
OUT_FILE = 1


#######################################################
# 기울여 계산기 
#######################################################

# ** 일반 노트북 > 테스트
# ANGLE_NONE = 9      # 응답 해제 되는 각도
# ANGLE_ANSWER = 15   # 응답으로 인식되는 각도

# 전시실 : 하단 카메라 위치 -2
# ANGLE_NONE = 11     # 응답 해제 되는 각도
# ANGLE_ANSWER = 15   # 응답으로 인식되는 각도

ANGLE_NONE = ini['angle_none']     # 응답 해제 되는 각도
ANGLE_ANSWER = ini['angle_answer']   # 응답으로 인식되는 각도


# 일반 노트북 > 테스트
# ZPOS_FORWARD_NONE = 0.6   # 고개 숙임을 해제 하는 비율
# ZPOS_FORWARD_ANSWER = 1.5    # 고개 숙임을 인식하는 비율

# 전시실 : 하단 카메라 위치 -2
# ZPOS_FORWARD_NONE = 0.8       #  0.6 고개 숙임을 해제 하는 비율
# ZPOS_FORWARD_ANSWER = 1.05    # -0.3 고개 숙임을 인식하는 비율
ZPOS_FORWARD_NONE = ini['zpos_forward_none']   # 0.6고개 숙임을 해제 하는 비율
ZPOS_FORWARD_ANSWER = ini['zpos_forward_answer']    # -0.3고개 숙임을 인식하는 비율
# print(f'{ANGLE_NONE} {ANGLE_ANSWER} {ZPOS_FORWARD_NONE} {ZPOS_FORWARD_ANSWER}')

# m_quiz_mental.py - lb_imgFile
#   gen_arithmetiec.py / m_quiz_mental.py
# 총 레벨 갯수 1 ~ 15 레벨
#  엑셀 설정 option1, option2 내용이 없거나, 잘못된 경우 기본 값.
GEN_DEFAULT_ARITHMETIC_REPEAT = 2                   # 동일 레벨 반복 횟수 : 2
GEN_DEFAULT_ARITHMETIC_OVER_RANDOM_START_LEVEL = 5  # 레벨 초과시 랜덤 시작레벨 : 5

QUIZ_MENTAL_END_WAIT_TIME = 3000            # 멘탈 퀴즈 종료후 결과만 보여주는 대기 시간 3초

QUIZ_MENTAL_INFO_IMG = 'head_tilt_info.png' # m_quiz_mental.py - lb_imgFile


#######################################################
# 빔 프로젝터 전원 관리 Scheduler
#######################################################
# PROJ_CONTROL = True                  # 빔프로젝터 프로젝터 컨트롤 ON
# PROJ_CONTROL = False                  # 빔프로젝터 프로젝터 컨트롤 OFF
PROJ_CONTROL = ini['projector_serial_control'] 
NOT_PROJ_CONTROL_TIME =  5000       # 프로젝트 컨트롤이 아닌 경우, _main.display_StartWait 에서 재생 지연시간

SCHEDULER_PATH = './scheduler/'
SCHEDULER_FILE = 'scheduler.xlsx'   # 스케쥴 설정파일

PROJ_COM_NAME = [4, 2]               # 프로젝터 시리얼포트 이름
PROJ_COM_SPEED = [5, 2]              # 프로젝터 시리얼speed

PROJ_PWR_ON_SEND_CMD = [8, 2]        # 프로젝터 PWR ON 송신
PROJ_PWR_ON_REC_CMD = [9, 2]         # 프로젝터 PWR ON 응답
PROJ_PWR_OFF_SEND_CMD = [10, 2]      # 프로젝터 PWR OFF 송신
PROJ_PWR_OFF_REC_CMD = [11, 2]       # 프로젝터 PWR OFF 응답
PROJ_PWR_REPEAT = [12, 2]            # 프로젝터 미응답시 반복 횟수

SCH_PWR_ON_PRIE_TIME = [15, 2]      # 지정 시간보다 미리 켜기 시간
SCH_PWR_OFF_AFTER_TIME = [16, 2]    # 지정 시간보다 지연 끄기 시간

SCH_SHUTDOWN_DELAY = [19, 2]          # 스케쥴 없는 경우 PC 종료 지연시간(없는 스케줄, 마지막 스케줄 이후)

SCH_TIME_TABLE = [24, 4]            # 스케쥴 테이블 시작 위치

'''
|       일       |     월     |    화
|control | time  | ctl | time |
| ON     | 08:20 |
| OFF    | 08:40 |


'''
SCH_SLEEP_SEC =  1          # 1[초] 마다 sleep 실행 (초단위)
SCH_SERIAL_SEND_SEC = 5     # 5[초] 마다 일반스케쥴 검사  (초단위)
# SCH_TIMER_CHK_CNT = int(SCH_SERIAL_SEND_SEC/SCH_SLEEP_SEC)
SERIAL_SEND_MAX = 5
SCH_QUIZ_PROGRES_DELAY_MIN = 2   # [분]단위 퀴즈가 진행중일 때, 프로젝터'OFF', 'OS_OFF' 지연되는 시간
SCH_TIME_CHECK_STEP_SEC = SCH_SERIAL_SEND_SEC * SERIAL_SEND_MAX

# LOG_PATH 경로에 생성
SCH_LOG_FILE_NAME = 'serial_log_'

# 보류 종료시간 없는 경우 보류
# SCH_DOWN_DEFAULT_TIME = 2   # 종료 설정이 없는 경우 종료 대기 시간


######################################################
# MSG_FILE_QUIZ_WIAT = 'message_quiz_wait.html'
MSG_FILE_QUIZ_WIAT = 'message_quiz_wait*.html'      # 여러개의 파일을 읽어 들이기 위함.
MSG_FILE_USER_SEARCH = 'message_user_search.html'
MSG_FILE_QUIZ_COUNTDOWN = 'message_quiz_countdown.html'


MENU_ANIMATION = ini['menu_animation']
# MENU_ANIMATION = False
MENU_INFO_TIME = ini['nenu_info_time']   # msec 단위


#######################################################
QR_SCANNER_PORT = ini['qr_scanner_port']    # 'COM9'
QR_SCANNER_SPEED = ini['qr_scanner_speed']  # 9600
QR_ENCRYPT_KEY = ini['qr_encrypt_key']      #'aesKey'

