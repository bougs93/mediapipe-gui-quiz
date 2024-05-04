import val
from setup import *
from ini_file import *

from PySide6.QtWidgets import *

###############
from thread_face_tilt import *
from ui_quiz_mental import Ui_quizMentalView
from ui_mental_arithmetic import Ui_widget
from ui_mental_test import Ui_widget as Ui_widget_test
from xlsx_quiz_load import *

from gen_arithmetiec import *

MENTAL_TEST = False      # True or False : 멘탈 그림의 위치 테스트 하는 부분
# MENTAL_TEST = True      # True or False : 멘탈 그림의 위치 테스트 하는 부분
MENTAL_POS_ADD_X = 20    # cam 640*480 사이즈 보정 : +20
MENTAL_POS_ADD_Y = -20   # cam 640*480 사이즈 보정 : -20

MENTAL_WIDGET_SIZE_W = 1000
MENTAL_WIDGET_SIZE_H = 1000

MEN_COLOR_BLACK = "background-color: rgb(0, 0, 0); border-radius: 45px; border: 8px solid rgb(232, 232, 232); color: rgb(255, 255, 255);"
MEN_COLOR_GREEN = "background-color: rgb(117, 183, 108); border-radius: 45px; border: 8px solid rgb(232, 232, 232); color: rgb(255, 255, 255);"
MEN_COLOR_RED = "background-color: rgb(229, 71, 67); border-radius: 45px; border: 8px solid rgb(232, 232, 232); color: rgb(255, 255, 255);"

QUIZ_TYPE = 'quizTite'

ANSWER_RADIUS = "border-radius: 45px"
ANSWER_STY_DEFAULT = "background-color: rgb(0, 0, 0); border-radius: 45px; border: 8px solid rgb(232, 232, 232); color: rgb(255, 255, 255);"
ANSWER_STY_CORRECT = "background-color: rgb(117, 183, 108); border-radius: 45px; border: 8px solid rgb(232, 232, 232); color: rgb(255, 255, 255);"
ANSWER_STY_WRONG = "background-color: rgb(229, 71, 67); border-radius: 45px; border: 8px solid rgb(232, 232, 232); color: rgb(255, 255, 255);"
ANSWER_SIZE_UP = 30 # 짝수

PROGRESS_BAR_GREEN = "QProgressBar::chunk { background-color: rgb(6, 175, 37); }"
PROGRESS_BAR_ORANGE = "QProgressBar::chunk { background-color: rgb(255, 170, 0); }"
PROGRESS_BAR_RED = "QProgressBar::chunk { background-color: rgb(229, 71, 67); }"

NEXT_QUIZ_TIMER = 1000/QTIMER_INTERVAL  # 1초

# 경고 메시지, 화면의 분할하여 중앙에 위치하도록 x|o|x
FRAME_X_CENTOR_AREA_DIV = 3

# 경고 메시지, 너무 가까운 경우
WARING_LENGTH = 0.25

class Mental(QWidget, Ui_widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Ui_quizView

class MentalTest(QWidget, Ui_widget_test):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Ui_quizView

class MentalGView(QWidget):
    def __init__(self):
        super().__init__()

        self.graphicsview = QGraphicsView()
        self.scene = QGraphicsScene(self.graphicsview)
        self.graphicsview.setScene(self.scene) 

        self.graphicsview.setStyleSheet("background: transparent; ")

        self.graphicsview.setFrameShape(QGraphicsView.NoFrame)
        self.graphicsview.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphicsview.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        if MENTAL_TEST == True:
            print(' > MENTAL_TEST')
            self.mental = MentalTest()
        else:
            print(' > NOT MENTAL_TEST')
            self.mental = Mental()
        self.mental.setStyleSheet("background-color: transparent; ")

        self.proxy = QGraphicsProxyWidget()
        self.proxy.setWidget(self.mental)

        # 중앙을 변환 기준점으로 설정
        self.proxy.setTransformOriginPoint(self.proxy.boundingRect().center())
        # 하단 중앙을 변환 기준점으로 설정
        # self.proxy.setTransformOriginPoint(self.proxy.boundingRect().center().x(), self.proxy.boundingRect().bottom())
        self.scene.addItem(self.proxy)

        # 나머지 설정(1)
        layout = QVBoxLayout(self)
        layout.addWidget(self.graphicsview)

        #########################################
        if not MENTAL_TEST:
            self.lb_score = self.mental.lb_m_score
            self.lb_question = self.mental.lb_m_question
            self.lb_answer1 = self.mental.lb_m_answer1
            self.lb_answer2 = self.mental.lb_m_answer2
            self.lb_answer3 = self.mental.lb_m_answer3
            self.progressBar = self.mental.pb_m_progressBar
            self.lb_end_score = self.mental.lb_m_end_score
            self.lb_end_score.hide()
            self.mental.lb_m_waring.hide()

            self.lb_id = self.mental.lb_m_id
            self.lb_name = self.mental.lb_m_name

            self.lb_score.setText('')
            self.lb_question.setText('')
            self.lb_answer1.setText('')
            self.lb_answer2.setText('')
            self.lb_answer3.setText('')
            self.lb_end_score.setText('')
            self.mental.lb_m_waring.setText('')

            self.lb_id.setText('')
            self.lb_name.setText('')

            self.lb_answer1.setStyleSheet(MEN_COLOR_BLACK)
            self.lb_answer2.setStyleSheet(MEN_COLOR_BLACK)
            self.lb_answer3.setStyleSheet(MEN_COLOR_BLACK)


    def setMove(self, _x, _y):
        # 위젯의 위치와 크기 정보를 가져옵니다.
        # size = self.size()
        size = self.mental.size()
        # print(size.width()/4)
        _x = _x - size.width()/2
        _y = _y - size.height()/2
        # self.move( center_x, center_y)
        self.move( _x, _y)

    def setAngle(self, angle):
        # 각도
        self.proxy.setRotation(angle)

    def setZoom(self, zoom):
        # 줌
        #########################################################################
        # 1) .resetTransform() : 원래 사이즈 복원이 정상적으로 되지 않음
        # 2) .setGeometry() 또는 .setFixedSize() 만으로 사이즈 지정하면 보이지 않음
        # 3) 2)사이즈 사용후, .resetTransform() 를 사용시 화면에 표시되고, 정상 동작

        # self.graphicsview.setGeometry(0,0, MENTAL_WIDGET_SIZE_W, MENTAL_WIDGET_SIZE_H)  # 원래 사이즈 지정
        self.graphicsview.setFixedSize(MENTAL_WIDGET_SIZE_W, MENTAL_WIDGET_SIZE_H)
        self.graphicsview.resetTransform()      # 원래의 사이즈로 복원(이상 동작)
        self.graphicsview.scale(zoom, zoom)     #    1.0 기준
        self.proxy.setTransformOriginPoint(self.proxy.boundingRect().center())



class QuizMentalDisplay(QWidget, Ui_quizMentalView):

    sound_play_signal = Signal(str)
    main_to_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Ui_quizView

        self.displayInt()   # 초기화
        self.createMentalWidget()   # 멘탈 위젯 생성

        ##### 버전 정보 표시 #####
        try:
            self.lb_verInfo.setText( f'프로그램 {PROGRAM_VER}  |  퀴즈 {QUIZ_VER}  |  Program developer : {PROGRAM_DEVELOPER}')
        except:
            pass

        # 1. 캡쳐 이미지가 보여줄 창의 사이즈 정보
        # https://www.geeksforgeeks.org/pyqt5-access-the-size-of-the-label/
        self.imageView_width, self.imageView_height = self.lb_imageView.size().width(), self.lb_imageView.size().height()
        print('1 frameView Size:',self.imageView_width, self.imageView_height)

        self.anglePreState = None       # None, left, right
        self.anglStateStart = False     # *해결방법 : 초기 > -90 right 발생 문제 해결책, 최초 None 만 인식하도록

        # 남은 시간을 가지고 타이머 색상 변경하기
        self.timeWarning = 0

        self.generateArithmetic = GenerateArithmetic()   # 암산문제 생성 객체

        val.st_quiz_cnt = 0
        self.quiz_level = 0
        self.correct_idx = None # 답에 해당하는 인덱스 [0 or 1]

        file_path = f"{IMG_PATH}{QUIZ_MENTAL_INFO_IMG}"
        pixmap = QPixmap(file_path)
        self.lb_imgFile.setPixmap(pixmap)

        self.test_hint = False
        self.lb_test_hint.setStyleSheet('')

        self.quizTimer_next = 0

        # 퀴즈 진행상태
        self.quiz_in_progress = 'stop'       # 'stop' : 중지, 'quiz_progress': 퀴즈중, 'quiz_end' 퀴즈 종료
        # 퀴즈 종료후 대기시간 타이머       
        self.timer_wait_end = int(QUIZ_MENTAL_END_WAIT_TIME/QTIMER_INTERVAL)

    def displayInt(self):
        # clear
        self.lb_no.setText('문제: ' )
        self.lb_code.setText('CODE: ' )
        self.lb_type.setText('영역: ')

        self.lb_usrName.setText(f'{val.st_id} {val.st_name}')
        self.lb_timeView.setText(QTime.fromString(val.speedQuizTime, 'm:s').toString('mm:ss'))

        if QUIZ_TYPE == 'speed':
            self.lb_type2.setText('퀴즈 유형: ' + '스피드 퀴즈')
        elif QUIZ_TYPE == 'golden':
            self.lb_type2.setText('퀴즈 유형: ' + '골든벨 퀴즈')
        elif QUIZ_TYPE == 'quizTite':
            self.lb_type2.setText('퀴즈 유형: ' + '암산')

        # 오답/PASS -> 오답
        self.lb_wrongpassTitle.setText('오답: ')

        if Q_CODE_VIEW :
            self.lb_code.show()
        else:
            self.lb_code.hide()
        self.lb_correct.setText(str(val.st_right_cnt))
        # 오답/PASS
        self.lb_wrongpass.setText(f'{str(val.st_wrong_cnt)}')
        # 점수
        self.lb_score.setText(str(val.st_score))

        self.lb_question.hide()
        self.lb_question2.hide()
        self.lb_question2Img.hide()
        self.lb_waitMsg.hide()

        self.anglStateStart = False     # *해결방법 : 초기 > -90 right 발생 문제 해결책, 최초 None 만 인식하도록


    def createMentalWidget(self):
        #################################################
        # 현재 ui 에 다른 ui 를 넣는 방법
        #################################################
        # 1. OK : 맨 아래에 삽입됨
        # self.layout().addWidget(mental)
        # mental.raise_()
        
        # 2. OK : 맨 상단에 삽입됨
        # mental.setParent(self.quizMentalDisplay)
        # 3. OK : 프레임 안에 삽입됨
        # mental.setParent(self.quizMentalDisplay.fr_main_quiz)
        #################################################

        #################################################
        # [중요] 위젯에 다른 위젯 넣기
        #################################################
        self.mentalGView = MentalGView()
        self.mentalGView.setStyleSheet("QScrollBar { width:0; }")

        # Ui "self.fr_main_quiz" QFrame 안에 "self.mentalGView" 위젯 넣기
        self.mentalGView.setParent(self.fr_main_quiz)   
        self.mentalGView.hide()     # 초기화면 숨기기
        #################################################
        # 사이즈 확대/복구 를 위한 기본값 저장
        self.answer1geo = self.mentalGView.lb_answer1.geometry()
        self.answer2geo = self.mentalGView.lb_answer2.geometry()
        self.answer3geo = self.mentalGView.lb_answer3.geometry()
        #################################################


    def mainViewUpdate(self):
        # view update
        self.lb_score.setText(str(val.st_score))
        self.lb_correct.setText(str(val.st_right_cnt))
        self.lb_wrongpass.setText(f'{str(val.st_wrong_cnt)}')
        self.mentalGView.lb_score.setText(str(val.st_score))

    def mentalGView_QuizView(self):
        # 멘탈 위젯 보이기
        self.mentalGView.mental.lb_m_score.show()
        self.mentalGView.mental.lb_m_question.show()
        self.mentalGView.mental.lb_m_answer1.show()
        self.mentalGView.mental.lb_m_answer2.show()
        self.mentalGView.mental.lb_m_answer3.show()
        self.mentalGView.mental.lb_m_id.show()
        self.mentalGView.mental.lb_m_name.show()
        self.mentalGView.mental.lb_m_frame.show()
        self.mentalGView.mental.pb_m_progressBar.show()
        # 멘탈 위젯에서 점수판 숨기기
        self.mentalGView.lb_end_score.hide()
        self.mentalGView.lb_end_score.setText(str(0))

    def mentalGView_EndView(self):
        # 멘탈 위젯 보이기
        self.mentalGView.mental.lb_m_score.hide()
        self.mentalGView.mental.lb_m_question.hide()
        self.mentalGView.mental.lb_m_answer1.hide()
        self.mentalGView.mental.lb_m_answer2.hide()
        self.mentalGView.mental.lb_m_answer3.hide()
        self.mentalGView.mental.lb_m_id.hide()
        self.mentalGView.mental.lb_m_name.hide()
        self.mentalGView.mental.lb_m_frame.hide()
        self.mentalGView.mental.pb_m_progressBar.hide()
        self.mentalGView.mental.lb_m_waring.hide()

        self.lb_waring.hide()
        # 멘탈 위젯에서 점수판 숨기기
        self.mentalGView.lb_end_score.show()
        self.mentalGView.lb_end_score.setText(str(val.st_score))

    def quiz1_CreatePreView(self, value):
        self.mentalGView_QuizView()

        self.lb_waitMsg.show()
        self.lb_question.setText('')
        self.lb_question.hide()

        self.mentalGView.hide()
        self.lb_question.hide()
        self.lb_question2.hide()
        self.lb_question2Img.hide()

        msg_show ='<html><head/><body><p align="center">_msg</p><p align="center"> 잠시만 기다려주세요</p></body></html>'
        if value == 'start':
            msg = "얼굴 인식을 위한 영상처리 준비중 입니다."
            msg_show = msg_show.replace("_msg", msg)
            self.lb_waring.show()
            self.lb_waring.setText('<html><head/><body><p><span style=" font-size:22pt; color:#ff0000;">화면 중앙에 위치하고 <br/>카메라에 얼굴이 잘 보이도록 하세요.</span></p><p><span style=" font-size:18pt; color:#0000ff;">어둡거나, 마스크, 모자</span><span style=" font-size:18pt; color:#000000;"> 등을 착용하는 경우<br/>얼굴 인식이 어렵습니다.</span></p></body></html>')
        elif value == 'end':
            msg = "손 인식을 위한 영상처리 준비중 입니다."
            msg_show = msg_show.replace("_msg", msg)
            self.lb_waring.hide()
        self.lb_waitMsg.setText(msg_show)

    # def quiz2_FileLoadSave(self, random_seq_mode):
    #     self.xlsxQuizLoad = XlsxQuizLoad(val.quizFileNum, random_seq_mode)
    #     self.xlsxQuizLoad.finished.connect(self.quiz2_LoadReady_slot)
    #     self.xlsxQuizLoad.start()

    def quiz3_ReadyCount_Start(self):
        # 안내문 표시
        self.lb_waitMsg.hide()
        text = f' <p> &nbsp;&nbsp;&nbsp; 기울여 암산 퀴즈를 시작합니다. </p> \
                  <p> &nbsp;&nbsp;&nbsp; 제한 시간({val.speedQuizTime}) 안에 최대한 많은 답을 맞추어야 합니다. </p>\
                  <p> &nbsp;&nbsp;&nbsp; - 점수 계산 방법 </p> \
                  <p> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 정답: +{Q_ANSWER_SCORE}점, 오답 : {Q_WRONG_SCORE}점</p>'
        quiz_view = quiz_format.replace('_quiz', text)
        # 도전자
        self.lb_usrName.setText(f'{val.st_id} {val.st_name}')
        
        self.lb_question.setText(quiz_view)
        self.lb_question.hide() # self.lb_question.show()
        self.lb_question2.hide()
        self.lb_question2Img.hide()
        self.lb_quizResult.show()   # 결과
        self.lb_imgFile.show()
        self.lb_test_hint.hide()

        self.mentalGView.progressBar.setStyleSheet(PROGRESS_BAR_GREEN)

        ##################################################################################
        # QProgressBar
        # 타이머 시간
        # timer_duration = QTime.fromString(val.speedQuizTime, 'm:s').second() / QTIMER_INTERVAL
        _time = QTime.fromString(val.speedQuizTime, 'm:s')
        timer_duration = _time.minute()*60 + _time.second()
        self.mentalGView.progressBar.setMaximum(timer_duration) # 최대값 설정
        self.mentalGView.progressBar.setValue(timer_duration)

        self.mentalGView.lb_id.setText(val.st_id)
        self.mentalGView.lb_name.setText(val.st_name)
        self.mentalGView.lb_score.setText('')
        self.mentalGView.lb_question.setText('')
        self.mentalGView.lb_answer1.setText('')
        self.mentalGView.lb_answer2.setText('')
        self.mentalGView.lb_answer3.setText('')

        # 응답 위젯 처음 상태로 복구 / 퀴즈 시작 3초 대기 시간 
        self.answerLeftDefault()
        self.answerCenterDefault()
        self.answerRightDefault()

        ##################################################################################

        # self.quiz4_Start()
        self.lb_quizResult.setStyleSheet("color: yellow; font: 700 200pt ;")
        self.lb_quizResult.setText('Ready')
        self.sound_play_signal.emit('Q_READY')
        # 1 sec
        QTimer.singleShot(1000, lambda : self.lb_quizResult.setStyleSheet("color: yellow; font: 700 300pt ;"))
        QTimer.singleShot(1000, lambda : self.lb_quizResult.setText('3'))
        QTimer.singleShot(1000, lambda : self.mentalGView.lb_question.setText('준비: 3'))
        # 2 sec
        QTimer.singleShot(2000, lambda : self.lb_quizResult.setText('2'))
        QTimer.singleShot(2000, lambda : self.mentalGView.lb_question.setText('준비: 2'))
        # 3 sec
        QTimer.singleShot(3000, lambda : self.lb_quizResult.setText('1'))
        QTimer.singleShot(3000, lambda : self.mentalGView.lb_question.setText('준비: 1'))
        # 4 sec
        QTimer.singleShot(4000, lambda : self.lb_quizResult.setText(''))
        # 퀴즈 시작
        QTimer.singleShot(4000, self.quiz4_Start)

        # if self.test_hint:
        #     self.lb_test_hint.show()
        # else:
        #     self.lb_test_hint.hide()


    def quiz4_Start(self):
        self.quiz41_Init('start')
        self.quiz42_Next()

    def quiz41_Init(self, mode):
        self.lb_question.hide()
        self.lb_waitMsg.hide()  # 준비 메시지 숨기기

        self.lb_no.show()   # 문제 번호 보이기
        self.lb_type.hide()
        self.lb_type2.show()
        self.lb_type2.setText("퀴즈유형: 기울여 암산")

        val.st_quiz_cnt = 0  # 문제생성 카운더 초기화
        self.quiz_level = 0

        # 응답 위젯 처음 상태로 복구 / TEST 모드시
        self.answerLeftDefault()
        self.answerCenterDefault()
        self.answerRightDefault()

        self.mainViewUpdate()

        ##################################################################################################
        # # QProgressBar
        # # 타이머 시간
        # # timer_duration = QTime.fromString(val.speedQuizTime, 'm:s').second() / QTIMER_INTERVAL
        # _time = QTime.fromString(val.speedQuizTime, 'm:s')
        # timer_duration = _time.minute()*60 + _time.second()
        # self.mentalGView.progressBar.setMaximum(timer_duration) # 최대값 설정

        # self.mentalGView.lb_id.setText(val.st_id)
        # self.mentalGView.lb_name.setText(val.st_name)


        ##################################################################################################
        # Qtimer 스탑워치
        # if mode == "start":
        #     self.test_hint = False
        #     self.timerSpeedQ = QTimer()
        #     self.timerSpeedQ_rem = QTime.fromString(val.speedQuizTime, 'm:s')
        #     self.timerSpeedQ.setInterval(QTIMER_INTERVAL)
        #     self.timerSpeedQ.timeout.connect(self.timerSpeedQ_timeout)
        #     self.timerSpeedQ.start()

        self.timerSpeedQ = QTimer()
        self.timerSpeedQ_rem = QTime.fromString(val.speedQuizTime, 'm:s')
        self.timerSpeedQ.setInterval(QTIMER_INTERVAL)
        self.timerSpeedQ.timeout.connect(self.timerSpeedQ_timeout)
        self.timerSpeedQ.start()
        
        if mode == "start":
            if Q_TEST_HINT:
                self.test_hint = True
            else:
                self.test_hint = False
        elif mode == "test":
            self.test_hint = True
        

        # 다음 문제까지의 타이머
        self.quizTimer_next = 0         # 첫문제는 바로 시작할 수 있도록
        self.quiz_in_progress = 'quiz_progress'



    def timerSpeedQ_timeout(self):
        #------------------------------------------------------------------
        # 멘탈 퀴즈 다음 문제까지 지연시간
        if self.quizTimer_next > 0:
            self.quizTimer_next -= 1
        #------------------------------------------------------------------
        if self.test_hint:
            return
        #------------------------------------------------------------------
        if self.quiz_in_progress == 'quiz_progress':  # 'stop' : 중지, 'quiz_progress': 퀴즈중, 'quiz_end' 퀴즈 종료
            self.timerSpeedQ_timeout_quizTimer()
        elif self.quiz_in_progress == 'quiz_end':
            self.timerSpeedQ_timeout_quizEndWait()


    def timerSpeedQ_timeout_quizTimer(self):
        # <주의> QTime 은 Qtime과 연산이 되지 않음
        #   self.timerSpeedRemainingTime = QTime.currentTime() - self.timerSpeedStartTime
        # 대신 addsec(), addMSec() 가능
        #   https://doc.qt.io/qtforpython-5/PySide2/QtCore/QTime.html#PySide2.QtCore.PySide2.QtCore.QTime.addMSecs
        
        self.timerSpeedQ_rem = self.timerSpeedQ_rem.addMSecs(-QTIMER_INTERVAL)
        self.lb_timeView.setText(self.timerSpeedQ_rem.toString('mm:ss'))

        _time = self.timerSpeedQ_rem
        self.mentalGView.progressBar.setValue(_time.minute()*60 + _time.second())
        
        # qtime 비교 연산
        #   https://doc.qt.io/qtforpython-6/PySide6/QtCore/QTime.html
        # print( self.timerSpeedQ_rem.__eq__(QTime.fromString('0:0', 'm:s')) or
        #       self.timerSpeedQ_rem.__ge__(QTime.fromString(SPEED_QUIZ_TIME, 'm:s')) )
        
        # SPEED_QUIZ_WARNING1_TIME
        # 남은 시간을 가지고 타이머 색상 변경하기
        if self.timerSpeedQ_rem.__le__(QTime.fromString(SPEED_QUIZ_WARNING2_TIME, 'm:s')):
            if self.timeWarning != 2:
                self.lb_timeView.setStyleSheet('background-color: rgb(255, 170, 127); color: rgb(170, 0, 127);')
                self.sound_play_signal.emit('stop')
                self.sound_play_signal.emit('ticktock2')
                self.timeWarning = 2
                self.mentalGView.progressBar.setStyleSheet(PROGRESS_BAR_RED)

        elif self.timerSpeedQ_rem.__le__(QTime.fromString(SPEED_QUIZ_WARNING1_TIME, 'm:s')):
            if self.timeWarning != 1:
                self.lb_timeView.setStyleSheet('background-color: rgb(255, 170, 127); color: rgb(170, 0, 127);')
                self.sound_play_signal.emit('ticktock1')
                self.timeWarning = 1
                self.mentalGView.progressBar.setStyleSheet(PROGRESS_BAR_ORANGE)

        else:
            self.lb_timeView.setStyleSheet('color : white;')

        timeOverChk = ( self.timerSpeedQ_rem.__eq__(QTime.fromString('0:0', 'm:s')) or
              self.timerSpeedQ_rem.__ge__(QTime.fromString(val.speedQuizTime, 'm:s')) )

        #------------------------------------------------------------------
        if timeOverChk :
            self.lb_timeView.setStyleSheet('color : white;')    # 타이머 색상 복원
            # self.timerSpeedQ.stop()
            # print(" >> timer stop ")
            # self.main_to_signal.emit("quizMental_end")

            self.sound_play_signal.emit('effectLoop_stop')  # 틱톡 소리 중지
            # self.quiz_in_progress = False   # None: 중지(미시작), True: 퀴즈중, False : 종료후 대기 
            self.quiz_in_progress = 'quiz_end' # 'stop' : 중지, 'quiz_progress': 퀴즈중, 'quiz_end' 퀴즈 종료

            # 멘탈 위젯 숨기고 점수판만 보이기
            self.mentalGView_EndView()

    def timerSpeedQ_timeout_quizEndWait(self):
        self.timer_wait_end -= 1
        if self.timer_wait_end < 0:
            self.timer_wait_end = int(QUIZ_MENTAL_END_WAIT_TIME/QTIMER_INTERVAL)
            # self.quiz_in_progress = 'stop'    # 'stop' : 중지, 'quiz_progress': 퀴즈중, 'quiz_end' 퀴즈 종료
            self.timerSpeedQ.stop()
            print(" >> timer stop ")

            self.main_to_signal.emit("quizMental_end")

    def timerSpeedQ_stop(self):
        print(' >> timerSpeedQ_stop : stop')
        try:
            self.timerSpeedQ.stop()
        except:
            pass

    def quiz42_Next(self):
        # 퀴즈 진행 상태가 아니면, pass
        if self.quiz_in_progress != 'quiz_progress':   # 'stop' : 중지, 'quiz_progress': 퀴즈중, 'quiz_end' 퀴즈 종료
            return 

        # 틀릴때 까지 반복하는 모드
        val.st_quiz_cnt += 1

        # 문제() 퀴즈 보여주기
        # self.sound_play_signal.emit('Q_START')
        # self.quizLoadNo(val.st_quiz_cnt)
        
        # (1) GEN_DEFAULT_ARITHMETIC_REPEAT 반복후 다음 레벨로
        # val.quizOption1 값 검사
        if val.quizOption1 == None or not isinstance(val.quizOption1, int):    # 값이 없가나 and 숫자인 경우 -> 기본 설정값으로 GEN_DEFAULT_ARITHMETIC_REPEAT
            val.quizOption1 = GEN_DEFAULT_ARITHMETIC_REPEAT
        if (val.st_quiz_cnt - 1) % val.quizOption1 == 0:
            self.quiz_level += 1

        # if (val.st_quiz_cnt - 1) % GEN_DEFAULT_ARITHMETIC_REPEAT == 0:
        #     self.quiz_level += 1

        # (2) levels 리스트 갯수만큼 초과한 경우. 랜덤
        level_total = len(self.generateArithmetic.levels)
        if val.quizOption2 == None or not isinstance(val.quizOption2, int):    # 값이 없가나 and 숫자인 경우 -> 기본 설정값으로 GEN_DEFAULT_ARITHMETIC_OVER_RANDOM_START_LEVEL
            val.quizOption2 = GEN_DEFAULT_ARITHMETIC_OVER_RANDOM_START_LEVEL
        if self.quiz_level > level_total:
            self.quiz_level = random.randint(val.quizOption2 , level_total)

        # if self.quiz_level > level_total:
        #     self.quiz_level = random.randint(GEN_DEFAULT_ARITHMETIC_OVER_RANDOM_START_LEVEL , level_total)

        self.lb_no.setText(f'문제: {str(val.st_quiz_cnt)}')
        self.lb_code.setText(f'CODE: {str(self.quiz_level)}')

        print(f' > 반복설정:{val.quizOption1} 랜덤시작:{val.quizOption2} | level:{self.quiz_level} | quiz cnt:{val.st_quiz_cnt}')

        self.quizLoadNo(self.quiz_level)
        # self.quizLoadNo(15)

        # 다음 문제까지의 타이머
        self.quizTimer_next = NEXT_QUIZ_TIMER


    def quizLoadNo(self, level):

        problem, answer = self.generateArithmetic.create(level)
        wrong1, wrong2 = self.generateArithmetic.wrong(answer)
        # 문제 종료후 결과 보이기
        print(problem, answer, wrong1, wrong2)

        ansList = [answer, wrong1, wrong2]
        random.shuffle(ansList)
        
        # 문제 표시전 전처리
        self.mentalGView.lb_question.setTextFormat(Qt.RichText)  # RichText 형식으로 설정하여 HTML 태그를 사용할 수 있도록 함
        
        f1 = problem.find("√(")
        if f1 != -1:
            # 인덱스 이후 첫 번째 문자만 교체
            idx = problem.find("√(")
            problem = problem[:idx] + "√<span style='text-decoration: overline'>" + problem[idx+2:]
            idx = problem.find(")", idx)
            problem = problem[:idx] + "</span>" + problem[idx+1:]
            
        f2 = problem.find("**(")
        if f2 != -1:
            # 인덱스 이후 첫 번째 문자만 교체
            idx = problem.find("**(")
            problem = problem[:idx] + "<sup>" + problem[idx+3:]
            idx = problem.find(")", idx)
            problem = problem[:idx] + "</sup>" + problem[idx+1:]
        
        problem = problem.replace("*", "×")

        # 문제 표시하기
        self.mentalGView.lb_question.setText(problem)
        # 답안 표시
        self.mentalGView.lb_answer1.setText(str(ansList[0]))    # left
        self.mentalGView.lb_answer2.setText(str(ansList[1]))    # center
        self.mentalGView.lb_answer3.setText(str(ansList[2]))    # right

        # 정답 위치 찾아서 인덱스변수에 저장하기 0: left, 1: center, 2: right
        self.correct_idx = ansList.index(answer)
        # print(f'정답 index :{self.correct_idx} / {answer}')

        # 테스트 모드시 정답 표시
        if self.test_hint:
            self.lb_test_hint.show()
            ansText = ''
            for i in range(self.correct_idx + 1):
                ansText = ansText + '.'
            self.lb_test_hint.setText(ansText)
        else:
            self.lb_test_hint.hide()

    def show_waring(self, waring):
        if self.quiz_in_progress == 'quiz_end':     # 'stop' : 중지, 'quiz_progress': 퀴즈중, 'quiz_end' 퀴즈 종료
            return
        
        msg = ''
        msg2 = ''
        if waring == 'no_face':
            msg = '<html><head/><body><p><span style=" color:#ff0000;">얼굴 인식이 되지 않습니다.</span></p><p><span style=" font-size:20pt; color:#0000ff;">카메라와 적절한 거리를 유지하세요.</span><span style=" font-size:20pt;"><br/>조명이 </span><span style=" font-size:20pt; color:#ff0000;">어둡거나, 마스크, 모자</span><span style=" font-size:20pt;"> 등을 착용하는<br/>경우 얼굴 인식이 어렵습니다.</span></p></body></html>'
        elif waring == 'no_center_left':
            msg = '<html><head/><body><p><span style=" color:#ff0000;">화면 중앙에 위치해 주세요</span></p><p><span style=" font-size:20pt;">옆에 위치하면 얼굴 각도, 기울림 인식에<br/> 오류가 발생할 가능성이 있습니다.</span></p></body></html>'
            msg2 = '화면 중앙으로 이동하세요 ⇒'
        elif waring == 'no_center_right':
            msg = '<html><head/><body><p><span style=" color:#ff0000;">화면 중앙에 위치해 주세요</span></p><p><span style=" font-size:20pt;">옆에 위치하면 얼굴 각도, 기울림 인식에<br/> 오류가 발생할 가능성이 있습니다.</span></p></body></html>'
            msg2 = '⇐ 화면 중앙으로 이동하세요'
        elif waring == 'no_length':
            msg = '<html><head/><body><p><span style=" font-size:22pt; color:#ff0000;">카메라와 너무 가깝습니다.</span></p><p><span style=" font-size:18pt;">카메라와 약간의 더 떨어진 거리를 유지하세요.</span></p></body></html>'
            msg2 = '카메라와 너무 가깝습니다.'
        self.lb_waring.show()
        self.lb_waring.setText(msg)

        if msg2 != '':
            self.mentalGView.mental.lb_m_waring.show()
            self.mentalGView.mental.lb_m_waring.setText(msg2)

    @Slot(np.ndarray)
    def update_image_slot(self, qt_img):
        """ X:주의 슬롯에 넣으면, 처리 못함.가상 키보드 """
        # self.vr_keyboard(cv_img)

        """Updates the image_label with a new opencv image"""
        # qt_img = self.convert_cv2qt(cv_img) -> thread 에서 처리하는 것으로 변경함.
        self.lb_imageView.setPixmap(qt_img)

    @Slot(str)
    def fps_slot(self, fps_str):
        self.lb_fps.setText(fps_str)

    @Slot(list)
    def foreheadxy_angle_slot(self, value):
        if value[0] == None or value[1] == None or value[2] == None:
            self.mentalGView.hide()
            # print("경고1: 얼굴인식이 되지 않습니다")
            self.show_waring('no_face')
        else:
            self.metalViewEnable(value)

    def metalViewEnable(self, value):
        self.mentalGView.show()
        x = value[0]
        y = value[1]
        self.angel = value[2]
        length = value[3]
        zpos_ratio = value[4]
        nose_x = value[5]

        # self.anglePreState : 이전 상태값
        # if self.angel < -ANGLE_ANSWER:
        #     if self.anglePreState == None:
        #         self.angleProgress('left')
        # elif self.angel > ANGLE_ANSWER:
        #     if self.anglePreState == None:
        #         self.angleProgress('right')
        # elif (abs(self.angel) < ANGLE_NONE) and (zpos_ratio > ZPOS_RATIO_ACT):
        #     if self.anglePreState == None:
        #         self.angleProgress('center')
        # elif (abs(self.angel) < ANGLE_NONE) and (zpos_ratio < ZPOS_RATIO_NONE):
        #     self.angleProgress(None)


        #------------------------------------
        # 위젯 보이기
        #   위젯 각도 변경
        self.mentalGView.setAngle(self.angel)
        #   위젯 크기 변경
        w_length = length * 5
        w_length = round(w_length, 2)
        self.mentalGView.setZoom(w_length)
        #   위치 보정
        frame_x = x + MENTAL_POS_ADD_X  # cam 640*480 사이즈 보정 : +20 zoom(1,1)
        frame_y = y + MENTAL_POS_ADD_Y  # cam 640*480 사이즈 보정 : -20 zoom(1,1)
        self.mentalGView.setMove(frame_x, frame_y)

        #------------------------------------
        # 경고 메시지 처리
        frame_x_center_min = int(self.imageView_width / FRAME_X_CENTOR_AREA_DIV)
        frame_x_center_max = self.imageView_width - int(self.imageView_width/FRAME_X_CENTOR_AREA_DIV)
        # if nose_x < frame_x_center_min or nose_x> frame_x_center_max :
        #     # print("경고2: 화면 중앙에 위치하세요")
        #     self.show_waring("no_center")
        if nose_x < frame_x_center_min :
            self.show_waring("no_center_left")
        elif nose_x> frame_x_center_max :
            # print("경고2: 화면 중앙에 위치하세요")
            self.show_waring("no_center_right")
        elif length > WARING_LENGTH:
            # print(length)
            self.show_waring("no_length")
        else:
            self.lb_waring.hide()
            self.mentalGView.mental.lb_m_waring.hide()

        #------------------------------------
        # 퀴즈 타이머가 시작중이 아니면, pass
        if self.quiz_in_progress != 'quiz_progress':   # 'stop' : 중지, 'quiz_progress': 퀴즈중, 'quiz_end' 퀴즈 종료
            return

        #-------------------------------------
        # 좌, 중앙, 우 정답 판단
        if self.angel < -ANGLE_ANSWER:
            self.angleProgress('left')
        elif self.angel > ANGLE_ANSWER:
            self.angleProgress('right')
        elif (abs(self.angel) < ANGLE_NONE) and (zpos_ratio > ZPOS_FORWARD_ANSWER):
            self.angleProgress('center')
        elif (abs(self.angel) < ANGLE_NONE) and (zpos_ratio < ZPOS_FORWARD_NONE):
            self.angleProgress(None)

    def angleProgress(self, state):
        # print(self.anglStateStart , self.anglePreState, state)

        # *해결방법 : 초기 > -90 right 발생 문제 해결책, 최초 None 만 인식하도록
        if self.anglStateStart == False:
            if state == None:
                self.anglStateStart = True
            return
        
        ###> *None -> left, right : 발생
        if state != None \
            and self.anglePreState != state \
            and self.anglePreState == None:
            # 문제점 : thread_face_tilt 시작 초기 > -90 right 가 발생함.
            self.anglePreState = state

            # 왼쪽 0
            if state == 'left' and self.correct_idx == 0:
                val.st_right_cnt += 1
                self.answerLeft('corrent')
                val.st_score += Q_ANSWER_SCORE
                self.sound_play_signal.emit('Q_CORRECT')

            elif state == 'left' and self.correct_idx != 0:
                val.st_wrong_cnt +=1
                self.answerLeft('wrong')
                val.st_score += Q_WRONG_SCORE
                self.sound_play_signal.emit('Q_WRONG')

            # 중앙 1
            if state == 'center' and self.correct_idx == 1:
                val.st_right_cnt += 1
                self.answerCenter('corrent')
                val.st_score += Q_ANSWER_SCORE
                self.sound_play_signal.emit('Q_CORRECT')

            elif state == 'center' and self.correct_idx != 1:
                val.st_wrong_cnt +=1
                self.answerCenter('wrong')
                val.st_score += Q_WRONG_SCORE
                self.sound_play_signal.emit('Q_WRONG')

            # 오른쪽 2
            elif state == 'right' and self.correct_idx == 2:
                val.st_wrong_cnt +=1
                self.answerRight('corrent')
                val.st_score += Q_ANSWER_SCORE
                self.sound_play_signal.emit('Q_CORRECT')

            elif state == 'right' and self.correct_idx != 2:
                val.st_right_cnt += 1
                self.answerRight('wrong')
                val.st_score += Q_WRONG_SCORE
                self.sound_play_signal.emit('Q_WRONG')

            self.mainViewUpdate()


        ###> *left, right -> None : 발생
        elif state == None \
            and (self.anglePreState == 'left' or self.anglePreState == 'center' or self.anglePreState == 'right') :

            self.answerRightDefault()
            self.answerCenterDefault()
            self.answerLeftDefault()
            self.mentalGView.lb_question.setText('')
            self.mentalGView.lb_answer1.setText('')
            self.mentalGView.lb_answer2.setText('')
            self.mentalGView.lb_answer3.setText('')

            if self.quizTimer_next == 0:
                self.quiz42_Next()
                self.anglePreState = state


    #-----------------------------------------------------------------------------------------------------------------------#
    def answerLeft(self, co_wr):
        # self.answer1geo = self.mentalGView.lb_answer1.geometry()
        # self.answer2geo = self.mentalGView.lb_answer2.geometry()
        # self.answer3geo = self.mentalGView.lb_answer3.geometry()
        if co_wr == 'corrent':
            ans_style = ANSWER_STY_CORRECT
        elif co_wr == 'wrong':
            ans_style = ANSWER_STY_WRONG
        # Size UP
        self.mentalGView.lb_answer1.setGeometry(self.answer1geo.left()-ANSWER_SIZE_UP/2, self.answer1geo.top()-ANSWER_SIZE_UP/2, \
                                                 self.answer1geo.width()+ANSWER_SIZE_UP, self.answer1geo.height()+ANSWER_SIZE_UP)
        # Style apply. 
        height = self.mentalGView.lb_answer1.size().height()
        ans_style = ans_style.replace(ANSWER_RADIUS, f"border-radius: {int(height/2)}px")
        self.mentalGView.lb_answer1.setStyleSheet(ans_style)
    def answerLeftDefault(self):
        self.mentalGView.lb_answer1.setGeometry(self.answer1geo.left(), self.answer1geo.top(), \
                                                 self.answer1geo.width(), self.answer1geo.height())
        self.mentalGView.lb_answer1.setStyleSheet(ANSWER_STY_DEFAULT)
    #-----------------------------------------------------------------------------------------------------------------------#
    def answerCenter(self, co_wr):
        # self.answer1geo = self.mentalGView.lb_answer1.geometry()
        # self.answer2geo = self.mentalGView.lb_answer2.geometry()
        # self.answer3geo = self.mentalGView.lb_answer3.geometry()
        if co_wr == 'corrent':
            ans_style = ANSWER_STY_CORRECT
        elif co_wr == 'wrong':
            ans_style = ANSWER_STY_WRONG
        # Size UP
        self.mentalGView.lb_answer2.setGeometry(self.answer2geo.left()-ANSWER_SIZE_UP/2, self.answer2geo.top()-ANSWER_SIZE_UP/2, \
                                                 self.answer2geo.width()+ANSWER_SIZE_UP, self.answer2geo.height()+ANSWER_SIZE_UP)
        # Style apply. 
        height = self.mentalGView.lb_answer2.size().height()
        ans_style = ans_style.replace(ANSWER_RADIUS, f"border-radius: {int(height/2)}px")
        self.mentalGView.lb_answer2.setStyleSheet(ans_style)
    def answerCenterDefault(self):
        self.mentalGView.lb_answer2.setGeometry(self.answer2geo.left(), self.answer2geo.top(), \
                                                 self.answer2geo.width(), self.answer2geo.height())
        self.mentalGView.lb_answer2.setStyleSheet(ANSWER_STY_DEFAULT)
    #-----------------------------------------------------------------------------------------------------------------------#
    def answerRight(self, co_wr):
        # self.answer1geo = self.mentalGView.lb_answer1.geometry()
        # self.answer2geo = self.mentalGView.lb_answer2.geometry()
        # self.answer3geo = self.mentalGView.lb_answer3.geometry()
        if co_wr == 'corrent':
            ans_style = ANSWER_STY_CORRECT
        elif co_wr == 'wrong':
            ans_style = ANSWER_STY_WRONG
        # Size UP
        self.mentalGView.lb_answer3.setGeometry(self.answer3geo.left()-ANSWER_SIZE_UP/2, self.answer3geo.top()-ANSWER_SIZE_UP/2, \
                                                 self.answer3geo.width()+ANSWER_SIZE_UP, self.answer3geo.height()+ANSWER_SIZE_UP)
        # Style apply. 
        height = self.mentalGView.lb_answer3.size().height()
        ans_style = ans_style.replace(ANSWER_RADIUS, f"border-radius: {int(height/2)}px")
        self.mentalGView.lb_answer3.setStyleSheet(ans_style)
    def answerRightDefault(self):
        self.mentalGView.lb_answer3.setGeometry(self.answer3geo.left(), self.answer3geo.top(), \
                                                 self.answer3geo.width(), self.answer3geo.height())
        self.mentalGView.lb_answer3.setStyleSheet(ANSWER_STY_DEFAULT)
    #-----------------------------------------------------------------------------------------------------------------------#
 

###########################################################################################


class TestMain(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.quizMentalDisplay = QuizMentalDisplay()
        self.quizMentalDisplay.lb_quizResult.hide()
        self.quizMentalDisplay.lb_quizResult.hide()
        self.quizMentalDisplay.lb_question.hide()
        self.quizMentalDisplay.lb_question2.hide()
        self.quizMentalDisplay.lb_question2Img.hide()
        self.quizMentalDisplay.lb_waitMsg.hide()

        self.mentalGView = self.quizMentalDisplay.mentalGView     # 위젯 속성 축약


            # 남은 시간을 가지고 타이머 색상 변경하기
        self.timeWarning = 0

        # 퀴즈 파일 정보(val.quizFileList 에 저장)
        self.xlsxQuizPreLoad = XlsxQuizPreLoad(QUIZ_SELECT_MODE)    #  'day_seq' , 파일 리스트 반환

        #################################################################
        # 2. 퀴즈파일의 영역이름 불려오기
        qArea =''
        qArea, val.speedQuizTime, val.quizTitleImage, val.quizMode, val.quizOption1, val.quizOption2 = self.xlsxQuizPreLoad.getQuizInfo(val.quizFileNum)
        ########################################################################
        
        '''
        편집!
        '''

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.quizMentalDisplay)
        # self.setLayout(self.vbox)

        self.widget = QWidget()
        self.widget.setLayout(self.vbox)

        self.setCentralWidget(self.widget)

        self.setFixedSize(1280, 1024)
        # <> 윈도우 센터에 뛰우기 / PYSIDE6 CENTER WINDOW. 
        #   https://www.loekvandenouweland.com/content/pyside6-center-window.html
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)

        #  1) create the video capture thread
        self.threadFaceTitle = ThreadFaceTilt(self.quizMentalDisplay.imageView_width, self.quizMentalDisplay.imageView_height)

        #  2) signal connect
        self.threadFaceTitle.change_pixmap_signal.connect(self.update_image_slot)
        self.threadFaceTitle.fps_signal.connect(self.fps_slot)
        self.threadFaceTitle.foreheadxy_angle_signal.connect(self.foreheadxy_angle_slot)

        #  3) start the thread
        self.threadFaceTitle.start()

        ########################################################################
        self.anglePreState = None       # None, left, right
        self.anglStateStart = False


    @Slot(np.ndarray)
    def update_image_slot(self, qt_img):
        """ X:주의 슬롯에 넣으면, 처리 못함.가상 키보드 """
        # self.vr_keyboard(cv_img)

        """Updates the image_label with a new opencv image"""
        # qt_img = self.convert_cv2qt(cv_img) -> thread 에서 처리하는 것으로 변경함.
        self.quizMentalDisplay.lb_imageView.setPixmap(qt_img)

    @Slot(str)
    def fps_slot(self, fps_str):
        self.quizMentalDisplay.lb_fps.setText(fps_str)

    @Slot(list)
    def foreheadxy_angle_slot(self, value):
        if value[0] == None or value[1] == None or value[2] == None:
            self.mentalGView.hide()
        else:
            self.metalViewEnable(value)
    def metalViewEnable(self, value):
        self.mentalGView.show()
        x = value[0]
        y = value[1]
        self.angel = value[2]
        length = value[3]

        # 위젯 각도 변경
        self.mentalGView.setAngle(self.angel)

        # ANGLE_NONE: 응답해제 각도, ANGLE_ANSWER:응답각도
        if self.angel < -ANGLE_ANSWER:
            self.angleProgress('left')
        elif self.angel > ANGLE_ANSWER:
            self.angleProgress('right')
        elif abs(self.angel) < ANGLE_NONE:
            self.angleProgress(None)

        # 위젯 크기 변경
        length = length * 5
        length= round(length, 2)
        self.mentalGView.setZoom(length)

        # 위치
        frame_x = x + MENTAL_POS_ADD_X  # cam 640*480 사이즈 보정 : +20 zoom(1,1)
        frame_y = y + MENTAL_POS_ADD_Y  # cam 640*480 사이즈 보정 : -20 zoom(1,1)
        
        self.mentalGView.setMove(frame_x, frame_y)


    # def angleProgress(self, state):
    #     # 해결책 : 초기 > -90 right 발생 문제 해결책 , 최초 None 만 인식하도록
    #     if self.anglStateStart == False:
    #         if state == None:
    #             self.anglStateStart = True
    #         return

    #     # None -> left, center, right 시 발생
    #     if state != None and self.anglePreState != state:
    #         self.anglePreState = state
    #         # 문제점 : thread_face_tilt 시작 초기 > -90 right 가 발생함.
    #         print(self.angel, state)
    #         if state == 'left': 
    #             self.answerLeft('corrent')  # current , wrong
    #         elif state == 'right':  # 오른쪽
    #             self.answerRight('wrong')  # current , wrong

    #     # None -> left, right 시 발생
    #     elif state == None and (self.anglePreState == 'left' or self.anglePreState == 'right'):
    #         self.anglePreState = state
    #         print(self.angel, state)
    #         self.answerRightDefault()
    #         self.answerLeftDefault()

    #-----------------------------------------------------------------------------------------------------------------------#
    def answerLeft(self, co_wr):
        self.answer1geo = self.mentalGView.lb_answer1.geometry()
        self.answer2geo = self.mentalGView.lb_answer2.geometry()
        if co_wr == 'corrent':
            ans_style = ANSWER_STY_CORRECT
        elif co_wr == 'wrong':
            ans_style = ANSWER_STY_WRONG
        # Size UP
        self.mentalGView.lb_answer1.setGeometry(self.answer1geo.left()-ANSWER_SIZE_UP/2, self.answer1geo.top()-ANSWER_SIZE_UP/2, \
                                                 self.answer1geo.width()+ANSWER_SIZE_UP, self.answer1geo.height()+ANSWER_SIZE_UP)
        # Style apply. 
        height = self.mentalGView.lb_answer1.size().height()
        ans_style = ans_style.replace(ANSWER_RADIUS, f"border-radius: {int(height/2)}px")
        self.mentalGView.lb_answer1.setStyleSheet(ans_style)
    def answerLeftDefault(self):
        self.mentalGView.lb_answer1.setGeometry(self.answer1geo.left(), self.answer1geo.top(), \
                                                 self.answer1geo.width(), self.answer1geo.height())
        self.mentalGView.lb_answer1.setStyleSheet(ANSWER_STY_DEFAULT)
    #-----------------------------------------------------------------------------------------------------------------------#
    def answerRight(self, co_wr):
        self.answer1geo = self.mentalGView.lb_answer1.geometry()
        self.answer2geo = self.mentalGView.lb_answer2.geometry()
        if co_wr == 'corrent':
            ans_style = ANSWER_STY_CORRECT
        elif co_wr == 'wrong':
            ans_style = ANSWER_STY_WRONG
        # Size UP
        self.mentalGView.lb_answer2.setGeometry(self.answer2geo.left()-ANSWER_SIZE_UP/2, self.answer2geo.top()-ANSWER_SIZE_UP/2, \
                                                 self.answer2geo.width()+ANSWER_SIZE_UP, self.answer2geo.height()+ANSWER_SIZE_UP)
        # Style apply. 
        height = self.mentalGView.lb_answer2.size().height()
        ans_style = ans_style.replace(ANSWER_RADIUS, f"border-radius: {int(height/2)}px")
        self.mentalGView.lb_answer2.setStyleSheet(ans_style)
    def answerRightDefault(self):
        self.mentalGView.lb_answer2.setGeometry(self.answer2geo.left(), self.answer2geo.top(), \
                                                 self.answer2geo.width(), self.answer2geo.height())
        self.mentalGView.lb_answer2.setStyleSheet(ANSWER_STY_DEFAULT)
    #-----------------------------------------------------------------------------------------------------------------------#
    

#######################################################################
# 퀴즈 텍스트 형식 지정 | quiz_format.replace('_quiz', '안녕하세요')

quiz_format = '<style type=text/css> \
p.margin { \
    margin-top: 30px; \
    margin-bottom: 30px; \
    margin-right: 30px; \
    margin-left: 30px; \
    line-height: 110%; \
} \
</style> \
<p class="margin">_quiz</p>'


if __name__=="__main__":
    from _main import *
    from thread_face_tilt import ThreadFaceTilt

    app = QApplication(sys.argv)
    # a = TestMain()
    a = MyWidonws()
    a.display_QuizMental()

    # NEW
    QTimer.singleShot(1000, a.quizMentalDisplay.quiz4_Start)

    a.show()
    sys.exit(app.exec())