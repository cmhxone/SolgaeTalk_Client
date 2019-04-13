# 솔개톡 클라이언트
2019년 3학년 1학기 캡스톤디자인 솔개의선택
프로젝트 솔개톡 클라이언트 소스입니다

## PySide2(Qt) 설치 방법
- 명령 프롬프트에서 pip install PySide2 --user 입력하면 설치 완료

## PyMysql 설치 방법
- 명령 프롬프트에서 pip install PyMysql --user 입력하면 설치 완료

## 추가한 사항
### 2019-04-07
- [x] 최초 접속 시 닉네임 설정 구현(X)
- [x] 닉네임, 플래그, 메시지를 포함한 버퍼 전송의 구현

### 2019-04-08
- [x] 기본 GUI 구현
- [x] 메시지 수신 시 채팅로그 업데이트 먹통 오류 수정

### 2019-04-10
- [x] 채팅로그 출력 전 커서 이동 구현
- [x] 클라이언트 접속 시 접속메시지 출력 구현
- [x] 로그인 다이얼로그 GUI 구현
- [x] 로그인 구현 위한 MariaDB 연동 시스템 구현
- [x] 로그인 다이얼로그 기능 구현

### 2019-04-11
- [x] 회원가입 다이얼로그 구현

### 2019-04-12
- [x] 종료 시 종료 메시지 전송 구현

### 2019-04-13
- [x] 회원가입 시 아이디, 닉네임의 마스킹 구현
- [x] 메인 어플리케이션 타이틀 이름 변경
- [x] 회원가입 시 아이디, 닉네임 입력 에디터의 문자 길이제한 구현
- [x] 접속자 목록 구현

## 추가할 사항
- [ ] 이미지 전송 기능 구현
- [ ] 파일 전송 기능 구현
- [ ] MariaDB Accounts 테이블에 닉네임, 컬러값을 저장할 수 있도록 테이블 수정
- [ ] MariaDB Accounts 테이블에서 닉네임, 컬러값을 이용해 채팅 로그에 출력 구현
- [ ] 메시지 수신 시 알림음 추가
- [ ] 대화내용 캡쳐기능 추가
