from setup import *

# 모듈간 글로벌 변수
#########################

# 학생 정보 관련 초기화
st_id = ''           # 문자로
st_school = ''       # exhibition 모드에서 사용
st_grade = ''
st_name = '손님'

# 학생 점수 관련 초기화
st_score = 0
st_quiz_cnt = 0
st_right_cnt = 0
st_wrong_cnt = 0
st_pass_cnt = 0
st_quizStartTime = None
st_rank = None  # 0 또는 None 으로 해야  q_quiz_end.quizEnd_resultView() 에서 순위 표시 하지 않음.
#########################
quiz_total = 0

musicVolume = 0

musicAllPlay = False
musicFileName = ''
playlist_index = 0
quizFile =''
quizFileBefore =''
quizFileNum = -1      # 0 부터 시작 시키기 위함
quizFileList = []
quizNameList = []
# previous_quiz_load_date = ''
# image_cell_row_dic = {}      # 이미지가 포함된 문항 번호, 이미지 딕셔너리

visitor_DayCount = 0    # 오늘 방문자 카운트
visitor_TotalCount = 0  # 누적 방문자

speedQuizTime = '0:0'
quizTitleImage = None
quizMode = None
quizOption1 = None
quizOption2 = None

quiz_in_progress_date_change = False     # 퀴즈 진행중 날짜 변화

how_to_reset_ranking = None

key3_respose_time_out = 0.2
#########################
# m_quiz.py
# 결과 저장

# self.count += 1
# self.user_quiz_data[SEQ][self.count] = self.count
# self.user_quiz_data[QNO][self.count] = '문항번호'
# self.user_quiz_data[ANS][self.count] = '정답'
# self.user_quiz_data[YNP][self.count] = 'Y/N/P'
# self.user_quiz_data[REQ][self.count] = '응답'
