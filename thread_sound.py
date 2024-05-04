'''
https://stackoverflow.com/questions/69415713/playing-sounds-with-pyqt6

https://doc.qt.io/qtforpython-6/PySide6/QtMultimedia/QMediaPlayer.html

playlist 제거됨.
https://doc.qt.io/qtforpython-6/overviews/qtmultimedia-changes-qt6.html


state code : https://doc.qt.io/qt-5/qmediaplayer.html

'''

from PySide6.QtCore import *
# import mediapipe as mp
import numpy as np
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
import cv2, os, random
import math, time, sys
from PySide6.QtWidgets import *
# from PySide6 import QtGui

from setup import *
import val

# #########################################################################
#  ThreadSound
# #########################################################################
class ThreadSound(QThread):

    music_play_signal = Signal(str)

    def __init__(self):

        super().__init__()

        ''' ############  effict sound play ####################### '''
        # ## PyQt sound play
        #   https://stackoverflow.com/questions/69415713/playing-sounds-with-pyqt6
        #   https://doc.qt.io/qtforpython-5/PySide2/QtMultimedia/QSoundEffect.html
        #   https://doc.qt.io/qtforpython-6/PySide6/QtMultimedia/QSoundEffect.html#PySide6.QtMultimedia.PySide6.QtMultimedia.QSoundEffect.setLoopCount
        
        # 재생 않되는 문제
        #   https://stackoverflow.com/questions/64794912/qsoundeffect-doesnt-play-sounds-when-its-out-of-global-scope

        # 배경음악용 mp3 플레이어
        print('[1] ERR')    # 
        self.effect = QSoundEffect(QCoreApplication.instance())
        print('[2]')
        self.effectLoop = QSoundEffect(QCoreApplication.instance())

        # 파이썬으로 날짜가 무슨 요일인지 구하기
        #   https://domdom.tistory.com/237
        # self.soundDict = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'YES':10, 'NO':11, 'PASS':12, 'QUIT':13, 'O':14,'X':15}
    

        ''' ############  music sound play  ####################### '''
        # Python에서 확장자가 .wav .mp3 인 디렉토리의 모든 파일 찾기
        #   https://www.todaymart.com/440
        # 1) mp3 파일 검색
        files = os.listdir(MUSUC_PATH)
        self.playlist = [i for i in files if i.endswith('.mp3')]
        # self.playlist = [i for i in files if i.endswith('.ogg')]
        # self.playlist = [i for i in files if i.endswith('.wav')]

        # self.playlist = [i for i in files if i.endswith('.wav')]
        # self.playlist.__add__([i for i in files if i.endswith('.ogg')])
        # self.playlist.__add__([i for i in files if i.endswith('.mp3')])

        print( 'music file List = ', self.playlist)

        # 2) musicPlayer
        print('[3] ERR')
        self.musicPlayer = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.musicPlayer.setAudioOutput(self.audio_output)

        #    musicPlayer -> self.next
        self.musicPlayer.mediaStatusChanged.connect(self.next)

        self.mediaDevice = QMediaDevices()
        self.mediaDevice.audioOutputsChanged.connect(self.audioOutputChanged)
        # 3) music count
        # val.playlist_index = 0    # 초기화
        val.musicVolume = MUSIC_VOLUME

        # 
        val.music_all_play = MUSIC_ALL_PLAY


    # 1. 단일 플레이
    def effectPlay(self, text):
        try:
            self.effect.setSource(QUrl.fromLocalFile(f'{WAV_PATH}{WAV_FILE[WAV_DIC[text]]}'))
            self.effect.play()
            print(f'>> effect play : {text}')
        except KeyError:
            pass

    # 2. 반복 효과음
    def effectLoopPlay(self, text):
        if text != 'effectLoop_stop':
            self.effectLoop.setSource(QUrl.fromLocalFile(f'{WAV_PATH}{WAV_LOOP_FILE[WAV_LOOP_DIC[text]]}'))
            self.effectLoop.setLoopCount(-2)
            self.effectLoop.play()
            print(f'>> effect loop play : {text}')
        else:
            try:
                self.effectLoop.stop()
            except:
                pass
            print(f'>> effect loop stop : {text}')


    def run(self):
        print(' > Sound Thread run...')
        self.musicAllPlay()


    @Slot(str)
    def sound_play_slot(self, text):
        print(' sound text =', text)
        if text == 'effectLoop_stop':
            self.effectLoopPlay('effectLoop_stop')

        elif text == 'music_allPlay':
            self.musicAllPlay()

        elif text == 'music_stop':
            try:
                self.musicPlayer.stop()
            except RuntimeError:
                pass
            print('음악 종료')
            try:
                self.start_wait_to_msg_signal.emit(f'')
            except AttributeError:
                pass

        else:
            if text in WAV_LOOP_DIC.keys():
                # 루프 플레이 /  stop 해야만 함.
                self.effectLoopPlay(text)
            else:
                # 단일 플레이
                self.effectPlay(text)


    def musicAllPlay(self):
        # 파일이 없으면 종료
        if len(self.playlist) <= 0:
            return
        
        if val.playlist_index > len(self.playlist) - 1:
            val.playlist_index = 0

        playfile = self.playlist[val.playlist_index]
        
        print(' val.playlist_index = ', val.playlist_index)

        self.musicFilePlay(playfile)


    # https://doc.qt.io/qtforpython-6/PySide6/QtMultimedia/QMediaPlayer.html#PySide6.QtMultimedia.PySide6.QtMultimedia.QMediaPlayer.MediaStatus
    # https://doc.qt.io/qt-5/qmediaplayer.html
    def next(self, state):
        # print(f'call next - state : {state}')

        if state == QMediaPlayer.EndOfMedia:     # 시스템 멈춤 의심? 삼성노트북
            # print( ' .EndOfMedia')
            if val.playlist_index > len(self.playlist) - 1:
                val.playlist_index = 0
       
            if val.music_all_play == False:
                print(' Music STOP')
                return

            playfile = self.playlist[val.playlist_index]
            print(playfile)
            self.musicFilePlay(playfile)


    def musicFilePlay(self, file):
        # print(f' call musicFilePlay {file}')
        # print(f' call musicFilePlay {self.musicPlayer.playbackState()}')
        # if self.musicPlayer.playbackState() == QMediaPlayer.PlayingState:
        #     print(' Playing State : STOP')
        #     self.musicPlayer.stop()

        # if self.musicPlayer.playbackState() == QMediaPlayer.PlaybackState.StoppedState:

        if self.musicPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            print(' Playing State : STOP')
        QTimer.singleShot(1, lambda: self.musicFilePlay_sub(file))
    def musicFilePlay_sub(self, file):
        time.sleep(2)   # [중요] stop() 또는 준비 시간 없이 바로 재생하는 경우 멈춤 에러 발생
        ################################################################
        self.musicPlayer.setSource(QUrl.fromLocalFile(f'{MUSUC_PATH}{file}'))
        # self.musicPlayer.setSource(QUrl.fromLocalFile(f'{MUSUC_PATH}{file}'.encode('utf-8')))
        ################################################################
        
        self.audio_output.setVolume(val.musicVolume)
        self.musicPlayer.play()        # [에러] 초기 동작& 단축키 'o' 사용시 멈춤
        val.playlist_index += 1

        print(' 재생 file : ', file )
        val.musicFileName  = file       # 대기화면에서 파일 재생 파일 이름 전달용 변수
        self.music_play_signal.emit(f'재생 : {file}')


    def audioOutputChanged(self):
        print(' >> 오디오 변경')
        if self.musicPlayer.playbackState() != QMediaPlayer.StoppedState:
            self.audio_output.setDevice(QMediaDevices.defaultAudioOutput())
        else:
            ### 버그 : 출력장치 변경시, 1회 재생못하는 문제 해결책 ###
            del self.audio_output   # 객체 삭제후 재생성하여 사용
            del self.musicPlayer

            self.musicPlayer = QMediaPlayer()
            self.audio_output = QAudioOutput()
            self.musicPlayer.setAudioOutput(self.audio_output)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    sound = ThreadSound()

    #########################################################
    # 개별 파일 테스트
    #########################################################
    # sound.musicFilePlay("Mena Massoud, Naomi Scott - A Whole New World - 알라딘OST.mp3")
    sound.musicFilePlay("슬의사2_20 미도와 파라솔 - 언젠가는.mp3")
    # sound.musicFilePlay("Pachelbel - Canon.mp3")
    sound.start()
    #########################################################

    #########################################################
    # 폴더내 모든 파일 테스트
    #########################################################
    # files = os.listdir(MUSUC_PATH)
    # flie_list  = [i for i in files if i.endswith('.mp3')]
    # cnt = len(flie_list)
    # while cnt:
    #     print('테스트 cnt = ', cnt)
    #     sound.musicAllPlay()
    #     time.sleep(3)
    #     cnt -= 1
    # time.sleep(3)
    # print('테스트 종료')
    # sound.musicPlayer.stop()
    #########################################################

    sys.exit(app.exec())

'''
오류 해결 .musicAllPlay()
  반복시 멈춤

프로젝터 기능 on / off
 프로젝터 스케줄 X
    program 처음 시작시 음악 시작

 프로젝터 스케줄 O
    program 처음 시작시 음악 중지

'''
