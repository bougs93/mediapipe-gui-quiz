'''
시리얼 QR코드 스캐너
시리얼 포트용

'''

from setup import *
import re, datetime, time, sys, os
from PySide6.QtCore import QTime
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

from enum import Enum
import qr_encrypt

# import logging
# logging.basicConfig(level=logging.DEBUG)

# DATA : ad/del, id, school, grade, class, number, name, gender, etc (,:8개)
DATA_SPLIT_CHAR_CNT = 8
SCAN_HEADER = 0
SCAN_ID = 1
SCAN_SCHOOL = 2
SCAN_GRADE = 3
SCAN_CLASS = 4
SCAN_NUMBER = 5
SCAN_NAME = 6
SCAN_GENDER = 7
SCAN_ETC = 8


# class ThreadQRScanner(QThread):
class QRScanner(QObject):
    qrScanner_signal = Signal(list)

    def __init__(self):
        super().__init__()

        self.scan_port_name = QR_SCANNER_PORT
        self.scan_port_speed = QR_SCANNER_SPEED 
        self.key = QR_ENCRYPT_KEY 

        self.aes = qr_encrypt.AESCipher(self.key)

        self.ignore_flag = False  # 데이터를 무시할지 여부를 결정하는 플래그

    def stop(self):
        self.quit()
        self.wait(5000)

    # def run(self):
    def open(self):

        print('**************************************')
        print('**  QR Scanner 시리얼 포트 Check    **')
        print('**************************************')

        # serial port 초기화
        self.serial_init()

        # 시그널 슬롯 연결 (QtCore.QIODevice)
        # 시리얼 포트로 데이터를 수신 가능하게 되었을 때에 발행> readyRead 시그널
        #  https://doc.qt.io/qtforpython/PySide6/QtCore/QIODevice.html
        #  https://doc.qt.io/qtforpython/PySide6/QtCore/QIODevice.html#PySide6.QtCore.PySide6.QtCore.QIODevice.readyRead
        self.port.readyRead.connect(self.read_from_port)


    def serial_init(self):
        # 시리얼포트 선택 : 4800, 9600, 19200, 38400, 115200
        if self.scan_port_speed == 4800:
            self.baudrate = QSerialPort.Baud4800
        elif  self.scan_port_speed == 9600:
            self.baudrate = QSerialPort.Baud9600
        elif  self.scan_port_speed == 19200:
            self.baudrate = QSerialPort.Baud19200
        elif  self.scan_port_speed == 38400:
            self.baudrate = QSerialPort.Baud38400
        elif  self.scan_port_speed == 115200:
            self.baudrate = QSerialPort.Baud115200

        # 시리얼 포트 환경변수 설정
        self.port = QSerialPort()
        self.port.setBaudRate( self.baudrate )
        self.port.setPortName( self.scan_port_name )
        self.port.setDataBits( QSerialPort.Data8 )
        self.port.setParity( QSerialPort.NoParity )
        self.port.setStopBits( QSerialPort.OneStop )
        self.port.setFlowControl( QSerialPort.NoFlowControl )


        # 시리얼 포트 OPEN
        ret = self.port.open(QIODevice.ReadWrite)

        # self.port.setDataTerminalReady(True)
        

        if ret:
            print(f" SCANNER | Port {self.scan_port_name} Open [OK] : {self.scan_port_speed}\n")
            return True
        else:
            print(f" SCANNER | Port {self.scan_port_name} Open [ERR] : {self.scan_port_speed}\n")
            self.serial_stop()
            return False

    def serial_stop(self):
        self.port.close()
        print(f'\n SCANNER | Port {self.scan_port_name} Port Close')


    def read_from_port(self):
        if self.ignore_flag:
            self.port.readAll()  # 데이터를 읽지만 처리하지 않음. 무시함.
            return
        
        ### 수신 데이터 처리
        # QThread 에서 send는 되는데, receive가 안되는 문제 
        # https://opentutorials.org/module/544/19046
        received_data = self.port.readAll()

        # 1) \r 코드를 빈 문자열로 대체
        cleaned_data = received_data.replace(b"\r", b"")
        # print(f'\n SCANNER | Port data recive : {cleaned_data}')

        # 2) 암호화 해제
        restore_data = self.aes.decrypt(cleaned_data)
        if restore_data == None:
            print(f'[복호화 ERR]')
        else:
            print(f' SCANNER | restore data recive : {restore_data}')
            self.analysis(restore_data)


    def pause_reception(self):
        self.ignore_flag = True

    def continue_reception(self):
        self.ignore_flag = False

    # ##################################################################

    def analysis(self, _string):
        #
        # ad/del, id, school, grade, class, number, name, gender, etc (,:8개)
        # ex) add,1234,고실초,2,6,30,홍길순,남,테스트1

        # err = False
        # 1) ',' 문자 개수 확인
        if _string.count(',') != DATA_SPLIT_CHAR_CNT:
            print(" [SCAN DATA ERR] : ',' 갯수 에러 error ")
            return

        # 2) ',' 분리 후, 문자 개수 확인
        str_list = _string.split(',')
        # print(f' [SCAN DATA LIST] = {str_list}')

        # 추가 모드
        if str_list[SCAN_HEADER] == 'add':
            pass

        # 삭제 모드
        elif str_list[SCAN_HEADER] == 'del':
            pass

        # 기타
        else:
            print(" [SCAN DATA ERR] : data[0] = add/del 이 아님")
            return
        
        # print(f" [SCAN DATA OK] : {str_list}")
        self.qrScanner_signal.emit(str_list)



if __name__ == "__main__":
    app = QCoreApplication([])
    # a = ThreadQRScanner()
    # a.run()

    b= QRScanner()
    b.open()
    sys.exit(app.exec())