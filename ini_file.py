
'''
읽고 쓰기 기본
    https://devnauts.tistory.com/197
일고 쓰기 간편화 코드
    https://devnauts.tistory.com/200

기본 소스
    https://webnautes.tistory.com/1718

Configparser 사용법
    https://bab-dev-study.tistory.com/18
    ini 파일을 생성하겠습니다. 파일 내용은 각 섹션이라고 하는 큰 분류값이 있으며
    그 안에는 Key-value 형태로 구성되어 있습니다.
    보통 섹션 key값은 대문자로 입력을하고 세부내용은 소문자로 입력을 합니다.
        [DEFAULT]
        config = 0
        textfile = config.ini

    
# 텍스트 형태로만 저장이 되므로 전 처리가 필요함.
'''
# https://jeong-f.tistory.com/132
# https://deep-eye.tistory.com/17
#   config 파일을 생성한 뒤, config[ '오브젝트 명'  ] = {} 으로 섹션을 생성할 수 있습니다
# https://markim94.tistory.com/113


import val
# from setup import *       # 활성화시 다른 파일에서 함수를 불러오지 못함
import configparser
from PySide6.QtCore import *

#################################################
### ini 파일 이름 ##
CONFIG_PATH = './config/'
STATE_INI_FILE = 'state.ini'
SETUP_INI_FILE = 'setup.ini'

### log 파일 : 저장위치 LOG_PATH = './log/'
LOG_PATH = './log/'
VISITOR_COUNT_LOG = "visitor_count_log.txt"


MUSIC_VOLUME_SAVE_MIN = 0.1

IMG_TITLE_XY_DEFAULT = [30, -70] 
IMG_TITLE_SIZE_DEFALUT = 730

IMG_FACE_FILE_XY_DEFAULT = [1140, 860]
IMG_FACE_FILE_SIZE_DEFAULT = 100

QUESTION_UNDERLINE_WORDS_DEFAULT = ['아닌','못한','않은','not','Not','NOT']

ANGLE_NONE_DEFAULT = 11     # 응답 해제 되는 각도
ANGLE_ANSWERE_DEFAULT = 15   # 응답으로 인식되는 각도
ZPOS_FORWARD_NONE_DEFAULT = 0.8       #  0.6 고개 숙임을 해제 하는 비율
ZPOS_FORWARD_ANSWER_DEFAULT = 1.05    # -0.3 고개 숙임을 인식하는 비율


# 설정
def stateIni_save():
    # https://jeong-f.tistory.com/132
    # https://deep-eye.tistory.com/17
    stateIni = configparser.ConfigParser()  ## 클래스 객체 생성

    ###############################################################
    # [로드] 날짜 변화 검사
    stateIni.read(f'{CONFIG_PATH}{STATE_INI_FILE}', encoding='utf-8')
    KEY = 'DEFAULT' #    설정파일 색션 확인
    iniDate = stateIni[KEY]['date'] # 날짜 로드

    currentDate = QDate.currentDate().toString("yyyy-MM-dd")

    if currentDate != iniDate:      # 현재 날짜 = ini 파일 날짜 비교
        val.visitor_DayCount = 0    # 날짜 변화시 day 카운트 = 0
        val.quiz_in_progress_date_change = True
    ###############################################################

    if val.musicVolume <= MUSIC_VOLUME_SAVE_MIN:
        volume = MUSIC_VOLUME_SAVE_MIN
    else:
        volume = val.musicVolume

    # 현재 날짜 계산 저장-> 로딩 현재와 다르면, visitor_DayCount = 0 

    # 오프젝트 DEFAULT
    KEY = 'DEFAULT'
    stateIni[KEY] = {}   # 섹션 생성
    stateIni[KEY]['date'] = QDate.currentDate().toString("yyyy-MM-dd")
    # if date_change == True:     # 프로그램 실행중 날짜가 바뀐경우 day 카운터 초기화
    #     val.visitor_DayCount = 0
    #     date_change == False
    stateIni[KEY]['visitor_day_count'] = str(val.visitor_DayCount)
    stateIni[KEY]['visitor_total_count'] = str(val.visitor_TotalCount)
    stateIni[KEY]['music_volume'] = str(volume)
    # stateIni[KEY]['music_all_play'] = str(val.music_all_play)
    stateIni[KEY]['quiz_file'] = str(val.quizFileList[val.quizFileNum])
    stateIni[KEY]['quiz_File_Num'] = str(val.quizFileNum)
    stateIni[KEY]['playlist_index'] = str(val.playlist_index)

    # 설정파일 저장
    with open(f'{CONFIG_PATH}{STATE_INI_FILE}', 'w', encoding='utf-8') as sateFile:
        stateIni.write(sateFile)


def stateIni_load(option):
    # 설정 파일 읽기
    stateIni = configparser.ConfigParser()
    stateIni.read(f'{CONFIG_PATH}{STATE_INI_FILE}', encoding='utf-8')

    # 설정파일 색션 확인
    KEY = 'DEFAULT'
    iniDate = stateIni[KEY]['date'] # 날짜 로드
    # val.previous_quiz_load_date = iniDate     # 글로벌 변수에 저장
    currentDate = QDate.currentDate().toString("yyyy-MM-dd")

    if option == 'date':    # 'date' 는 여기 까지만 로드.
        return
    # else 'all' 로 동작

    val.visitor_DayCount = int(stateIni[KEY]['visitor_day_count'])  # 방문자 숫자 로드

    # 현재날짜 != ini 날짜 비교
    if currentDate != iniDate:
        text = f'{iniDate} : {val.visitor_DayCount}\n'
        # 날짜가 다르면, 방문자 카운트를 0으로 변경한다.
        vistorLogWrite(text)
        val.visitor_DayCount = 0
        val.quiz_in_progress_date_change = True

    val.visitor_TotalCount = int(stateIni[KEY]['visitor_total_count'])


    val.musicVolume = float(stateIni[KEY]['music_volume'])

    val.quizFileBefore = stateIni[KEY]['quiz_file']
    val.quizFileNum = int(stateIni[KEY]['quiz_File_Num'])
    val.playlist_index = int(stateIni[KEY]['playlist_index'])

    print(f'{val.visitor_DayCount}, {val.musicVolume}, {val.music_all_play}')
    print(f'{val.visitor_TotalCount} {iniDate}')


def stateIni_create():
    # https://jeong-f.tistory.com/132
    # https://deep-eye.tistory.com/17
    stateIni = configparser.ConfigParser()  ## 클래스 객체 생성

    volume = val.musicVolume

    # 현재 날짜 계산 저장-> 로딩 현재와 다르면, visitor_DayCount = 0 

    # 오프젝트 DEFAULT
    KEY = 'DEFAULT'
    stateIni[KEY] = {}   # 섹션 생성
    stateIni[KEY]['date'] = QDate.currentDate().toString("yyyy-MM-dd")
    stateIni[KEY]['visitor_day_count'] = str(val.visitor_DayCount)
    stateIni[KEY]['visitor_total_count'] = str(val.visitor_TotalCount)
    stateIni[KEY]['music_volume'] = str(volume)
    stateIni[KEY]['music_all_play'] = str(val.music_all_play)
    stateIni[KEY]['quiz_file'] = str(val.quizFile)
    # stateIni[KEY]['quiz_file_count'] = str(val.quizFileCount)
    stateIni[KEY]['quiz_File_Num'] = str(0)


    # 설정파일 저장
    with open(f'{CONFIG_PATH}{STATE_INI_FILE}', 'w', encoding='utf-8') as sateFile:
        stateIni.write(sateFile)
    print('state.ini save')

def setupIni_create():
    #### setup.ini 기본 설정파일 생성
    setupIni = configparser.ConfigParser()  ## 클래스 객체 생성

    # 오프젝트 DEFAULT
    KEY = 'SETUP'
    setupIni[KEY] = {}   # 섹션 생성
    setupIni[KEY]['default_capture_deive'] = '0'
    # setupIni[KEY]['caputre_device_0'] = 'cv2.CAP_DSHOW+0'
    # setupIni[KEY]['caputre_device_1'] = 'cv2.CAP_DSHOW+1'
    setupIni[KEY]['user_id_max'] = '4'

    setupIni[KEY]['speed_quiz_default_time'] = '1:30'
    setupIni[KEY]['speed_quiz_warning1_time'] = '0:30'
    setupIni[KEY]['speed_quiz_warning2_time'] = '0:10'
    setupIni[KEY]['quiz_reg_time_out'] = '20'   # 초단위

    KEY2 = 'QUIZ'
    setupIni[KEY2] = {}   # 섹션 생성
    setupIni[KEY2]['quiz_select_mode'] = 'day_seq'
    setupIni[KEY2]['answer_score'] = '10'
    setupIni[KEY2]['wrong_score'] = '-10'
    setupIni[KEY2]['pass_score'] = '-5'
    setupIni[KEY2]['quiz_code_view'] = 'True'
    setupIni[KEY2]['quiz_end_view_time'] = '30'              # 초단위 숫자만 입력
    setupIni[KEY2]['video_button_reflash_delay_ms'] = '700'  # msec 단위
    setupIni[KEY2]['ranking_reset_new_days'] = '[]'                # 랭킹 초기화 날짜
    setupIni[KEY2]['question_underline_words'] = f'{QUESTION_UNDERLINE_WORDS_DEFAULT}'

    KEY3 = 'START_WAIT_VIEW'
    setupIni[KEY3] = {}
    setupIni[KEY3]['message_cmd_view_time'] = '1500'
    setupIni[KEY3]['rank_batle_view_interval'] ='500'   # msec 단위 입력

    KEY4 = 'PROJECTOR_CONTROL'
    setupIni[KEY4] = {}
    setupIni[KEY4]['projector_serial_control'] = 'True'

    KEY5 = 'TITLE_IMAGE'
    setupIni[KEY5] = {}
    setupIni[KEY5]['title_img_pos_xy'] = f'{IMG_TITLE_XY_DEFAULT}' 
    setupIni[KEY5]['title_img_size'] = f'{IMG_TITLE_SIZE_DEFALUT}'

    KEY6 = 'ICON_FACE_IMAGE'
    setupIni[KEY6] = {}
    setupIni[KEY6]['icon_face_image_pos_xy'] = f'{IMG_FACE_FILE_XY_DEFAULT}' 
    setupIni[KEY6]['icon_img_size'] = f'{IMG_FACE_FILE_SIZE_DEFAULT}'

    KEY7 = 'MENTAL_QUIZ'
    setupIni[KEY7] = {}
    setupIni[KEY7]['angle_none'] = f'{ANGLE_NONE_DEFAULT}'
    setupIni[KEY7]['angle_answer'] = f'{ANGLE_ANSWERE_DEFAULT}'
    setupIni[KEY7]['zpos_forward_none'] = f'{ZPOS_FORWARD_NONE_DEFAULT}' 
    setupIni[KEY7]['zpos_forward_answer'] = f'{ZPOS_FORWARD_ANSWER_DEFAULT}' 

    with open(f'{CONFIG_PATH}{SETUP_INI_FILE}', 'w', encoding='utf-8') as setupFile:
        setupIni.write(setupFile)


ini = {}

def setupIni_load():
    #### setup.ini 기본 설정파일 생성
    setupIni = configparser.ConfigParser()  ## 클래스 객체 생성
    setupIni.read(f'{CONFIG_PATH}{SETUP_INI_FILE}', encoding='utf-8')
    
    # 오프젝트 DEFAULT
    KEY = 'SETUP'
    # setupIni[KEY] = {}   # 섹션 생성
    ini['default_capture_deive'] = int(setupIni[KEY]['default_capture_deive']) # = '1'  # int
    # ini['caputre_device_0'] = setupIni[KEY]['caputre_device_0'] # = 'cv2.CAP_DSHOW+0'   # str
    # ini['caputre_device_1'] = setupIni[KEY]['caputre_device_1'] # = 'cv2.CAP_DSHOW+1'   # str

    ini['user_id_max'] = int(setupIni[KEY]['user_id_max'])
    ini['speed_quiz_default_time'] = setupIni[KEY]['speed_quiz_default_time'] # = '2:00'                # str
    ini['speed_quiz_warning1_time'] = setupIni[KEY]['speed_quiz_warning1_time'] # = '0:30' # str
    ini['speed_quiz_warning2_time'] = setupIni[KEY]['speed_quiz_warning2_time'] # = '0:10' # str
    ini['quiz_reg_time_out'] = setupIni[KEY]['quiz_reg_time_out'] # = '20'   # 초단위       # str


    KEY2 = 'QUIZ'
    # setupIni[KEY2] = {}   # 섹션 생성
    ini['quiz_select_mode'] = setupIni[KEY2]['quiz_select_mode'] # = 'day_seq'
    ini['answer_score'] = int(setupIni[KEY2]['answer_score']) # = '1'    # int
    ini['wrong_score'] = int(setupIni[KEY2]['wrong_score']) # = '-1'     # int
    ini['pass_score'] = int(setupIni[KEY2]['pass_score']) # = '-0.5'     # int
    if setupIni[KEY2]['quiz_code_view'] == 'True':
        ini['quiz_code_view'] = True
    elif setupIni[KEY2]['quiz_code_view'] == 'False':
        ini['quiz_code_view'] = False
    ini['quiz_end_view_time'] = setupIni[KEY2]['quiz_end_view_time'] # = '30' # str 초단위 숫자만 입력
    ini['video_button_reflash_delay_ms'] = int(setupIni[KEY2]['video_button_reflash_delay_ms'])      # VIDEO_BTN_REFLASH_DELAY
    
    ini['how_to_reset_ranking'] = setupIni[KEY2]['how_to_reset_ranking']

    str_underline_swrds = setupIni[KEY2]['question_underline_words']
    ini['question_underline_words'] = str_underline_swrds.strip('][').split(',')
    
    if setupIni[KEY2]['quiz_test_hint'] == 'True':
        ini['quiz_test_hint'] = True
    elif setupIni[KEY2]['quiz_test_hint'] == 'False':
        ini['quiz_test_hint'] = False

    KEY3 = 'START_WAIT_VIEW'
    # setupIni[KEY3] = {}
    ini['message_cmd_view_time'] = int(setupIni[KEY3]['message_cmd_view_time']) # = '1500'
    ini['rank_batle_view_interval'] = int(setupIni[KEY3]['rank_batle_view_interval']) # ='500'   # msec 단위 입력


    KEY4 = 'PROJECTOR_CONTROL'
    # setupIni[KEY4] = {}
    if setupIni[KEY4]['projector_serial_control'] == 'True':
        ini['projector_serial_control'] = True
    elif setupIni[KEY4]['projector_serial_control'] == 'False':
        ini['projector_serial_control'] = False


    KEY5 = 'MENU_QUIZ_WAIT'
    # setupIni[KEY5] = {}
    ini['title_img_pos_xy'] = setupIni[KEY5]['title_img_pos_xy']
    str_pos_xy = ini['title_img_pos_xy'].strip('][').split(',')
    try:
        pos_xy = [int (i) for i in str_pos_xy]
        ini['title_img_pos_xy'] = pos_xy
    except ValueError:
        ini['title_img_pos_xy'] = IMG_TITLE_XY_DEFAULT # 기본값
    try:
        ini['title_img_size'] = int(setupIni[KEY5]['title_img_size'])
    except ValueError:
        ini['title_img_size'] = IMG_TITLE_SIZE_DEFALUT # 기본값
    if setupIni[KEY5]['menu_animation'] == 'True':
        ini['menu_animation'] = True
    elif setupIni[KEY5]['menu_animation'] == 'False':
        ini['menu_animation'] = False
    ini['nenu_info_time'] = int(setupIni[KEY5]['nenu_info_time'])


    KEY6 = 'ICON_FACE_IMAGE'
    # setupIni[KEY5] = {}
    ini['icon_face_image_pos_xy'] = setupIni[KEY6]['icon_face_image_pos_xy']
    str_pos_xy = ini['icon_face_image_pos_xy'].strip('][').split(',')
    try:
        pos_xy = [int (i) for i in str_pos_xy]
        ini['icon_face_image_pos_xy'] = pos_xy
    except ValueError:
        ini['icon_face_image_pos_xy'] = IMG_FACE_FILE_XY_DEFAULT # 기본값
    try:
        ini['icon_img_size'] = int(setupIni[KEY6]['icon_img_size'])
    except ValueError:
        ini['icon_img_size'] = IMG_FACE_FILE_SIZE_DEFAULT # 기본값

    with open(f'{CONFIG_PATH}{SETUP_INI_FILE}', 'w', encoding='utf-8') as setupFile:
        setupIni.write(setupFile)

    KEY7 = 'MENTAL_QUIZ'
    ini['angle_none'] = float(setupIni[KEY7]['angle_none'])
    ini['angle_answer'] = float(setupIni[KEY7]['angle_answer'])
    ini['zpos_forward_none'] = float(setupIni[KEY7]['zpos_forward_none'])
    ini['zpos_forward_answer'] = float(setupIni[KEY7]['zpos_forward_answer'])


    KEY8 = 'QR_SCANNER'
    ini['qr_scanner_port'] = setupIni[KEY8]['qr_scanner_port']
    ini['qr_scanner_speed'] = int(setupIni[KEY8]['qr_scanner_speed'])
    ini['qr_encrypt_key'] = setupIni[KEY8]['qr_encrypt_key']
    


def vistorLogWrite(text):
    line = text
    with open(f'{LOG_PATH}{VISITOR_COUNT_LOG}', 'a') as file:
        file.write(line)

if __name__ == "__main__":
    # 테스트
    # val.visitor_DayCount = 4
    # val.musicVolume = 0.05
    # val.music_all_play = True

    # stateIni_create()
    # stateIni_save()
    # stateIni_load()

    # setupIni_create()
    # setupIni_load()
    # setupIni_load()

    # print(ini)
    pass

    
