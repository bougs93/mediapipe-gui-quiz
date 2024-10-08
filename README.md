# 2024 제70회 전국과학전람회 출품작
### 프로젝트 주제: AI모션 인식 기술 이용한 과학 퀴즈 연구
* 작성중~


## Mediapipe Quiz
### AI motion recognition with Google Mediapipe, quiz program using PySide
* 제작기간 : 2022.04. ~ 2024.05.
* 전체코드 라인수
  * 2024.05.05. 현재 : 18,328 라인
* 프로젝트 소개
  * Google MediaPipe, PySide6, OpenCV 등을 이용한 영상 제스처 인식을 이용한 퀴즈 게임( AI 학습)
    * 영상인식을 퀴즈 게임 학습에 이용 (4가지 문제 방식)
      1. 일반퀴즈 - 일반 텍스트 문제
      2. 그림 퀴즈 - 문항에 이미지가 포함 되는 문제
      3. 단어 퀴즈 - 단어, 숙어를 위한 문제, 선택 지문 자동 생성
      4. 수학암산 퀴즈 - 문제 자동 생성, 난이도 문항 수준 설정가능
    * 사용자 경험 개선 : OpenCV, MediaPipe -> PySide Widget 전달받아서 처리
    * 가상 키보드, 손가락 카운트 방법 개선
    * 얼굴 기울림 좌,우 기울림에 추가적으로 앞으로 기울림 방식추가 하여 개선 (초기 보정이 필요함)
  * 퀴즈 문제 타이틀(제목) 로그 이미지 설정 가능(png 파일)
  * 빔프로젝터 제어 및 스케쥴 관리 (시리얼 제어)
  * 뮤직박스 기능 (빔프로젝터 동작 시간에 맞추어 음악 재생)
  * 사용자 입력 및 답안 선택 방법
    * 가상키보드 터치 방식
    * 손가락 숫자 및 손모양 인식(1~5, O/X) 방식
    * 머리 움직임 인식(좌, 앞으로, 우)
  * 과자 자동지급기 : 퀴즈게임 점수 보상으로 자동 지급 - 제작중
  * 엑셀 파일을 이용한 사용자 및 퀴즈 문제 관리
  * QR 코드 리더기로 사용자 등록 및 퀴즈게임 시작 (시리얼 제어)
  * QR 코드 사용자ID 생성기 (시리얼 제어) - 제작중


### 폴더 구조
* config | 환경설정 폴더 (설정)
* db | 데이터 베이스 폴더(sqlite3) - 자동 생성
* effect | 효과음악 폴더
* font_install | 퀴즈에 사용되는 폰트 - window/font 폴더에 복사
* image | 이미지 저장
  * 퀴즈프로그램에 사용되는 이미지
  * 퀴즈 대기화면에 사용되는 퀴즈 제목 이미지
* log | 로그 저장
* music | 퀴즈 대기화면에 사용되는 배경음악
* quiz | 퀴즈 파일 폴더 (퀴즈문제 작성)
  * xlsx 파일로 작성하여 저장
* scheduler | 컴퓨터 스케쥴, 빔프로젝터 제어 스케줄 (동작 스케줄 작성)
  * xlsx 파일로 작성
* temp | 프로그램 임시 파일
* user | 학생, 교사 id 작성 파일 (id설정)


### 추후 계획 (예정)
* 글로벌(영문, 다국어) 버전으로 수정 예정
* 유튜브 소개영상 제작 예정
* 실행파일 형태로 프로그램 배포


### 게임화면
* 초상권 보호를 위해 얼굴을 캐릭터 이미지로 가림
![image](https://github.com/bougs93/mediapipe-quiz/assets/45992773/3f1505c4-63b2-4a53-9233-aa5cd44eb7d6)
![image](https://github.com/bougs93/mediapipe-quiz/assets/45992773/982a8bc1-c50f-4d71-943a-95c527067b85)
![image](https://github.com/bougs93/mediapipe-quiz/assets/45992773/3364e28d-fcd8-4d68-ac50-202d7438996f)

### 화면 전환방법
![image](https://github.com/bougs93/mediapipe-quiz/assets/45992773/3d4a4dad-77d1-41dc-b3cb-4965b25236d3)

### 퀴즈문제 등록 방법
![image](https://github.com/bougs93/mediapipe-quiz/assets/45992773/fafe327a-5083-4f52-a77c-3c65513e5bec)

### 컴퓨터 및 빔프로젝터 제어 스케쥴
![image](https://github.com/bougs93/mediapipe-quiz/assets/45992773/dd7d5d9d-a37f-4d1e-a834-d1c5611d77a6)

### Candy dispenser (사탕 자동지급기) - 제작 완료
![image](https://github.com/bougs93/mediapipe-quiz/assets/45992773/2f6ca2c5-90ba-4208-b072-c46a810391a1)


# 업데이트 현황
* 2024-05-09 일반, 전시관 순위 표시 문제 해결
* 2024-05-25 캔디 지급기 완성 및 동작 연동 완료, 기울여 퀴즈 타이머 오류 수정

