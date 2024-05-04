# 제38회 광주광역시과학전람회 출품작
### AI모션 인식 기술 이용한 과학 퀴즈 연구
* 설치방법, 환경설정, 사용법 문서 작성중

## Mediapipe Quiz
### AI motion recognition with Google Mediapipe, quiz program using PySide
* 제작기간 : 2022.04. ~ 2024.05.
* 프로그램 소개
  * Google MediaPipe, PySide6, OpenCV 등을 이용한 영상 제스처 인식을 이용한 퀴즈 게임( AI 학습)
  * 빔프로젝터 제어 및 스케쥴 관리
  * 모션 인식 방법 : 가상키보드, 손가락 카운터, 머리 움직임
  * 과자 자동지급기 : 시리얼 제적 - 제작중
  * QR 코드 리더기로 사용자 등록 및 퀴즈게임 시작
  * QR 코드 사용자ID 생성기 - 제작중

### 폴더 구조
* config | 환경설정 폴더 (설정)
* db | 데이터 베이스 폴더 - 자동 생성
* effect | 효과음악 폴더
* font_install | 퀴즈에 사용되는 폰트 - window/font 폴더에 복사
* image
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

### 게임화면
![image](https://github.com/bougs93/mediapipe-quiz/assets/45992773/982a8bc1-c50f-4d71-943a-95c527067b85)
![image](https://github.com/bougs93/mediapipe-quiz/assets/45992773/3364e28d-fcd8-4d68-ac50-202d7438996f)

### 화면 전환방법
![image](https://github.com/bougs93/mediapipe-quiz/assets/45992773/3d4a4dad-77d1-41dc-b3cb-4965b25236d3)

### 퀴즈문제 등록 방법
![image](https://github.com/bougs93/mediapipe-quiz/assets/45992773/fafe327a-5083-4f52-a77c-3c65513e5bec)

### 컴퓨터 및 빔프로젝터 제어 스케쥴
![image](https://github.com/bougs93/mediapipe-quiz/assets/45992773/dd7d5d9d-a37f-4d1e-a834-d1c5611d77a6)

### 과자 자동지급기 - 제작중
![image](https://github.com/bougs93/mediapipe-quiz/assets/45992773/2f6ca2c5-90ba-4208-b072-c46a810391a1)


