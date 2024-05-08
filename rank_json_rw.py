'''
https://codechacha.com/ko/python-read-write-json-file/
json 라이브러리는 파이썬의 dict, list 객체를 바로 JSON 파일로 저장할 수 있게 도와줍니다.


https://codechacha.com/ko/python-read-write-json-file/#json-파일-읽기
'''



import json, os
from PySide6.QtCore import *
from setup import *

class RankJsonRW():
    
    def __init__(self):
        pass
    
    def getFileName(self):
        # 파일에서 확장자 구분하기  https://chancoding.tistory.com/182
        xlsFileName = os.path.splitext(val.quizFileList[val.quizFileNum])
        if RANKING_EXHIBITION_MODE:
            self.rankFile = f'{RANKING_PATH}{xlsFileName[0]}{RANKING_EXHIBITION_POST_NAME}.{RANKING_FILE_EXT}'
        else:
            self.rankFile = f'{RANKING_PATH}{xlsFileName[0]}{RANKING_POST_NAME}.{RANKING_FILE_EXT}'
            # print(f' 랭킹 파일 이름 : {self.rankFile}')

    # 화면뷰용 로딩
    def viewLoad(self):
        self.getFileName()
        # print(f' 랭킹파일 로드 : {self.rankFile}')

        try:
            with open(f'{self.rankFile}','r', encoding='UTF-8') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            # print('Rank viewLoad : 랭킹 기록 파일이 없습니다')
            json_data = []

        for i in range(len(json_data)):

            if '손님' != json_data[i][RANK_NAME] :
                # 1.문자열 변경하기 : 홍*동
                #   원하는 위치 문자 변경하기 https://gbjeong96.tistory.com/25
                _name = json_data[i][RANK_NAME]     # 홍길동
                nameList = list(_name)
                nameList[1] = '*'       # 홍*동
                _name =''.join(nameList)
                # print(name)

                # data.append(f'{str(loaded[i][RANK_RANK])}위 ({loaded[i][RANK_DTIME].toString("yy.MM.dd hh:mm")}) {loaded[i][RANK_NAME][0]}-{loaded[i][RANK_NAME][1]} {name}')
                json_data[i][RANK_NAME] = _name

            # 2.날짜 변경하기 : 5.14 20:22
            _datetime = QDateTime.fromString(json_data[i][RANK_DTIME],"yyyy-MM-dd hh:mm:ss")
            json_data[i][RANK_DTIME] = _datetime.toString('MM.dd hh:mm')

        # print(json_data[1])

        return json_data

    # 최종 랭킹 기록 날짜
    def lastDate(self):
        self.getFileName()
        # print(f' 랭킹파일 로드 : {self.rankFile}')
        print('[debug] self.rankFile = ', self.rankFile)
        try:
            with open(f'{self.rankFile}','r', encoding='UTF-8') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            # print('Rank viewLoad : 랭킹 기록 파일이 없습니다')
            json_data = []
            return None

        _datetimes = []
        for i in range(len(json_data)):
            _datetime = QDateTime.fromString(json_data[i][RANK_DTIME],"yyyy-MM-dd hh:mm:ss")
            _datetimes.append(_datetime)

        # 최근 날짜순
        _datetimes.sort(reverse = True)
        return _datetimes[0].date() # 날짜 정보만 리턴

    # 원본 형태로 로드
    def read(self):
        self.getFileName()
        try:
            with open(f'{self.rankFile}','r', encoding='UTF-8') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            print('Rank read : 랭킹 기록 파일이 없습니다')
            json_data = []
        return json_data
    
    # 원본 형태로 저장
    def write(self, ranking_data):
        self.getFileName()
        with open(f'{self.rankFile}', 'w', encoding='UTF-8') as f:
            json.dump(ranking_data, f, indent="\t", ensure_ascii=False)
        print("Rank write : 랭킹 파일 기록 했습니다.")


if __name__=="__main__":
    a = RankJsonRW()
    print(a.read())