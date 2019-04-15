import sys	# 시스템 모듈을 임포트
import threading	# 스레드 모듈 임포트
import struct	# 구조체 모듈 임포트
import pymysql	# MySQL 모듈 임포트
import hashlib	# 해싱 모듈 임포트
import Client	# 소켓 클라이언트 모듈 임포트

# Qt 라이브러리 내의 필요 모듈들을 임포트한다
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
		
# 회원가입 GUI 어플리케이션 클래스
class RegistDialog(QDialog):
	__host : str	# MariaDB 호스트
	__layout : QVBoxLayout	# 다이얼로그 레이아웃
	__txtID : QLineEdit	# 아이디 입력 객체
	__txtPW : QLineEdit	# 비밀번호 입력 객체
	__txtPW_Confirm : QLineEdit	# 비밀번호 입력 확인 객체
	__txtNickname : QLineEdit	# 닉네임 입력 객체
	__btnRegist : QLineEdit	# 회원가입 시도 버튼 객체
	__lbNickname : QLabel	# 닉네임의 색상을 미리보여주는 레이블
	__sldRed : QSlider	# 닉네임의 레드값을 지정하는 슬라이더
	__sldGreen : QSlider	# 닉네임의 그린값을 지정하는 슬라이더
	__sldBlue : QSlider	# 닉네임의 블루값을 지정하는 슬라이더
	
	# 생성자
	def __init__(self, parent, host):
		# MariaDB 호스트 주소
		self.__host = host

		# 다이얼로그 초기화
		super(RegistDialog, self).__init__(parent)
		self.setWindowTitle("솔개톡 회원가입")
		self.setFixedSize(200, 240)
		
		# 다이얼로그 내의 객체 초기화
		self.__layout = QVBoxLayout()
		self.__txtID = QLineEdit()
		self.__txtPW = QLineEdit()
		self.__txtPW_Confirm = QLineEdit()
		self.__txtNickname = QLineEdit()
		self.__btnRegist = QPushButton("회원가입")
		self.__lbNickname = QLabel("닉네임 색상")
		self.__sldRed = QSlider(Qt.Horizontal)
		self.__sldGreen = QSlider(Qt.Horizontal)
		self.__sldBlue = QSlider(Qt.Horizontal)
		
		# 레이아웃에 객체 지정
		self.__layout.addWidget(self.__txtID)
		self.__layout.addWidget(self.__txtPW)
		self.__layout.addWidget(self.__txtPW_Confirm)
		self.__layout.addWidget(self.__txtNickname)
		self.__layout.addWidget(self.__lbNickname)
		self.__layout.addWidget(self.__sldRed)
		self.__layout.addWidget(self.__sldGreen)
		self.__layout.addWidget(self.__sldBlue)
		self.__layout.addWidget(self.__btnRegist)
		
		# 객체 속성 지정
		self.__txtID.setPlaceholderText("아이디")
		self.__txtPW.setPlaceholderText("비밀번호")
		self.__txtPW_Confirm.setPlaceholderText("비밀번호 확인")
		self.__txtNickname.setPlaceholderText("닉네임")
		self.__txtID.setMaxLength(32)
		self.__txtNickname.setMaxLength(32)
		self.__txtPW.setEchoMode(QLineEdit.Password)
		self.__txtPW_Confirm.setEchoMode(QLineEdit.Password)
		self.__btnRegist.clicked.connect(lambda: self.ProcessRegist())
		self.__lbNickname.setAlignment(Qt.AlignCenter)
		self.__lbNickname.setStyleSheet("background-color: #FFFFFF; font-weight: bold")
		self.__sldRed.setMinimum(0)
		self.__sldRed.setMaximum(255)
		self.__sldRed.setTickPosition(QSlider.TicksBelow)
		self.__sldRed.setTickInterval(8)
		self.__sldRed.valueChanged.connect(lambda: self.ColorChanged())
		self.__sldGreen.setMinimum(0)
		self.__sldGreen.setMaximum(255)
		self.__sldGreen.setTickPosition(QSlider.TicksBelow)
		self.__sldGreen.setTickInterval(8)
		self.__sldGreen.valueChanged.connect(lambda: self.ColorChanged())
		self.__sldBlue.setMinimum(0)
		self.__sldBlue.setMaximum(255)
		self.__sldBlue.setTickPosition(QSlider.TicksBelow)
		self.__sldBlue.setTickInterval(8)
		self.__sldBlue.valueChanged.connect(lambda: self.ColorChanged())
		
		# 다이얼로그를 출력한다
		self.setLayout(self.__layout)
		self.show()
		
	# 회원가입 버튼을 누른 경우 호출되는 함수
	def ProcessRegist(self):		
		# 아무것도 입력되지 않은 경우 오류메시지 출력
		if self.__txtID.text().strip() == "" or self.__txtPW.text().strip() == "" or self.__txtPW_Confirm.text().strip() == "" or self.__txtNickname.text().strip() == "":
			mb = QMessageBox()
			mb.setText("모든 항목을 입력해주세요")
			mb.setIcon(QMessageBox.Warning)
			mb.setWindowTitle("솔개톡 회원가입")
			mb.exec_()
		# 입력받은 아이디가 6글자 미만 인 경우 오류출력
		elif len(self.__txtID.text().strip()) < 6:
			mb = QMessageBox()
			mb.setText("아이디는 최소 6글자 이상입니다")
			mb.setIcon(QMessageBox.Warning)
			mb.setWindowTitle("솔개톡 회원가입")
			mb.exec_()
		# 입력받은 비밀번호와 비밀번호 값이 일치하지 않는 경우 오류출력
		elif self.__txtPW.text().strip() != self.__txtPW_Confirm.text().strip():
			mb = QMessageBox()
			mb.setText("비밀번호가 일치하지 않습니다")
			mb.setIcon(QMessageBox.Warning)
			mb.setWindowTitle("솔개톡 회원가입")
			mb.exec_()
		# 입력받은 경우 회원가입을 시도한다
		else:
			idAble = False			# 아이디 마스킹 변수
			nicknameAble = False	# 닉네임 마스킹 변수
			
			# 아이디 마스킹을 확인
			for c in self.__txtID.text().strip():
				if not (ord('A') <= ord(c) <= ord('Z') or ord('a') <= ord(c) <= ord('z') or ord('0') <= ord(c) <= ord('9')):
					mb = QMessageBox()
					mb.setText("아이디는 영대/소문자 및 숫자만 사용가능합니다")
					mb.setIcon(QMessageBox.Warning)
					mb.setWindowTitle("솔개톡 회원가입")
					mb.exec_()
					idAble = False
					break;
				else:
					idAble = True
					
			# 닉네임 마스킹을 확인
			for c in self.__txtNickname.text().strip():
				if not (ord('가') <= ord(c) <= ord('힣') or ord('A') <= ord(c) <= ord('Z') or ord('a') <= ord(c) <= ord('z') or ord('0') <= ord(c) <= ord('9')):
					mb = QMessageBox()
					mb.setText("닉네임은 한글, 영대/소문자 및 숫자만 사용가능합니다")
					mb.setIcon(QMessageBox.Warning)
					mb.setWindowTitle("솔개톡 회원가입")
					mb.exec_()
					idAble = False
					break;
				else:
					nicknameAble = True
		
			if idAble and nicknameAble:
				#MariaDB에 연결
				db = pymysql.connect(host=self.__host, port=3306, user="Solgae", passwd="gntech2152", db="SolgaeTalk", charset="utf8", autocommit=True)
				cursor = db.cursor()
				# 존재하는 아이디, 닉네임인지 확인한다
				cursor.execute("SELECT COUNT(*) FROM Accounts WHERE userID='" + self.__txtID.text().strip() + "' OR nickname='" + self.__txtNickname.text().strip() + "'")
				result = cursor.fetchone()
				
				# 존재하는 아이디, 닉네임이 있다면 오류메시지를 출력
				if result[0] != 0:
					mb = QMessageBox()
					mb.setText("이미 존재하는 아이디 또는 닉네임 입니다")
					mb.setIcon(QMessageBox.Warning)
					mb.setWindowTitle("솔개톡 회원가입")
					mb.exec_()
				# 없는 경우 회원가입을 시도한다
				else :
					# 입력받은 비밀번호를 암호화한다
					hashSHA = hashlib.sha256()
					hashSHA.update(self.__txtPW.text().strip().encode())
					hexSHA256 = hashSHA.hexdigest()

					# 아이디, 암호화한 비밀번호, 닉네임을 DB에 저장한다
					cursor.execute("INSERT INTO Accounts(userID, userPW, Nickname, red, green, blue) VALUES('" + self.__txtID.text().strip() + "', '" + hexSHA256  + "', '" + self.__txtNickname.text().strip() + "', " + str(self.__sldRed.value()) + ", " + str(self.__sldGreen.value()) + ", " + str(self.__sldBlue.value()) + ")")

					# 회원가입이 완료된경우 메시지와 함께 입력박스를 초기화 한다
					mb = QMessageBox()
					mb.setText("회원가입이 완료되었습니다")
					mb.setIcon(QMessageBox.Information)
					mb.setWindowTitle("솔개톡 회원가입")
					mb.exec_()

					self.__txtID.setText("")
					self.__txtPW.setText("")
					self.__txtPW_Confirm.setText("")
					self.__txtNickname.setText("")
					
	# 닉네임 컬러 슬라이더가 이동 될 때 호출되는 함수
	def ColorChanged(self):
		r = str(self.__sldRed.value())
		g = str(self.__sldGreen.value())
		b = str(self.__sldBlue.value())
		self.__lbNickname.setStyleSheet("background-color: #FFFFFF; font-weight: bold; color: rgb(" + r + "," + g + "," + b + ")")

# 클라이언트 GUI 어플리케이션 클래스
class ClientApp:
	__frame : QFrame	# 어플리케이션의 메인 프레임
	__chatlog : QPlainTextEdit	# 채팅로그
	__msgEdit : QLineEdit	# 사용자의 메시지를 입력받는 곳
	__btnSend : QPushButton	# 전송 버튼
	__clientSocket : Client.ClientSocket	# 클라이언트 소켓 클래스 객체
	__lock : threading.Lock
	__cursor : QTextCursor	# 채팅로그의 텍스트 커서
	__nickname : str	# 사용자의 닉네임
	__listUser : QListWidget	# 접속한 유저를 보여주는 리스트위젯
	# 사용자의 닉네임 색상값
	__red : int
	__green : int
	__blue : int
	
	# 생성자 (인자값으로 호스트명, 포트, 닉네임, 컬러값을 전달받는다)
	def __init__(self, host : str, port : int, nickname : str, r : int, g : int, b : int):
		self.__nickname = nickname
		self.__red = r
		self.__green = g
		self.__blue = b
		self.__lock = threading.Lock()
	
		self.__frame = QFrame()	# 메인 프레임을 생성한다
		self.__frame.setWindowTitle("솔개톡")
		
		# 프레임 내의 자식객체 생성
		self.__chatlog = QPlainTextEdit()	# 채팅로그를 생성한다
		self.__msgEdit = QLineEdit()	# 메시지 입력창을 생성한다
		self.__btnSend = QPushButton("전송")	# 메시지 전송 버튼을 생성한다
		self.__cursor = QTextCursor(self.__chatlog.document())	# 채팅로그 커서를 생성한다
		self.__listUser = QListWidget()	# 접속자 목록 리스트위젯을 생성한다
		listLabel = QLabel("접속자 목록")	# 목록 리스트 위에 보여질 레이블
		
		# 프레임과 자식객체의 연동
		self.__chatlog.setParent(self.__frame)
		self.__msgEdit.setParent(self.__frame)
		self.__btnSend.setParent(self.__frame)
		self.__listUser.setParent(self.__frame)
		listLabel.setParent(self.__frame)
		
		# 자식객체들의 속성 지정
		self.__chatlog.setFont("돋움")	# 채팅로그의 폰트 조정
		self.__chatlog.setFixedSize(480, 240)	# 채팅로그의 크기 조정
		self.__chatlog.move(10, 10)		# 채팅로그의 위치 조정
		self.__chatlog.setReadOnly(True)	# 채팅로그 읽기전용 모드 지정
		self.__msgEdit.move(10, 260)	# 메시지 입력창 위치 조정
		self.__msgEdit.setFixedSize(405, 21)	# 메시지 입력창 크기 조정
		self.__btnSend.move(415, 259)	# 메시지 전송 버튼 위치 조정
		self.__listUser.move(500, 25)	# 리스트 위젯의 위치 조정
		self.__listUser.setFixedSize(130, 255)	# 리스트 위젯의 크기 조정
		listLabel.move(500, 10)	# 목록 리스트 위에 레이블을 위치시킨다
		
		# 이벤트 발생 시 호출할 함수의 지정
		self.__msgEdit.returnPressed.connect(lambda: self.SendMessage())
		self.__btnSend.clicked.connect(lambda: self.SendMessage())
		
		self.InitSocket(host, port)	# 클라이언트 소켓 클래스를 초기화한다
		
		self.__frame.setFixedSize(640, 480)	# 프레임의 크기를 지정한다
		self.__frame.show()	# 메인 프레임을 보여준다
	
	# 소켓을 초기화, 접속 하는 함수
	def InitSocket(self, host : str, port : int):
		self.__clientSocket = Client.ClientSocket(host, port)
		# 서버에 접속을 실패한 경우 프로그램을 종료한다
		if not self.__clientSocket.Connect():
			exit(-1)
		# 접속에 성공한 경우 메시지 처리 함수를 별도의 스레드로 처리해준 뒤  접속 플래그를 담은 메시지를 전송
		else:
			processThread = threading.Thread(target=self.__clientSocket.ProcessMessage, args=([self.__cursor], [self.__chatlog], [self.__listUser]))
			processThread.daemon = True
			processThread.start()
			self.__clientSocket.SendMessage(1996, [self.__msgEdit], self.__nickname, self.__red, self.__green, self.__blue)
			
	# 전송버튼 또는 입력창에서 엔터를 누른경우 실행되는 함수
	def SendMessage(self):
		if not self.__msgEdit.text().strip() == "":
			self.__clientSocket.SendMessage(5002, [self.__msgEdit], self.__nickname, self.__red, self.__green, self.__blue)
			
	# 종료 되는 경우 실행되는 함수
	def QuitMessage(self):
		self.__clientSocket.SendMessage(2015, [self.__msgEdit], self.__nickname, self.__red, self.__green, self.__blue)

# 클라이언트 로그인 GUI 폼
class LoginDialog(QDialog):
	__txtID : QLineEdit	# 아이디 입력 창
	__txtPW : QLineEdit	# 비밀번호 입력 창
	__btnLogin : QPushButton	# 로그인 버튼
	__btnRegist : QPushButton	# 회원가입 버튼
	__layout : QVBoxLayout	# 다이얼로그 레이아웃
	__host : str	# 호스트 주소
	__port : int	# 포트번호
	__app : QApplication	# 어플리케이션
	__clientApp : ClientApp # 클라이언트 어플리케이션

	# 다이얼로그 생성자
	def __init__(self, host : str, port : int, parent=None):
		self.__host = host
		self.__port = port
	
		self.__app = QApplication(sys.argv)
		# 다이얼로그 초기화
		super(LoginDialog, self).__init__(parent)
		self.setWindowTitle("솔개톡 로그인")
		self.setFixedSize(200, 130)
		
		# 다이얼로그에 객체 생성
		self.__layout = QVBoxLayout()
		self.__txtID = QLineEdit()
		self.__txtPW = QLineEdit()
		self.__btnLogin = QPushButton("로그인")
		self.__btnRegist = QPushButton("회원가입")
		self.__btnLogin.clicked.connect(lambda: self.ProcessLogin())
		self.__btnRegist.clicked.connect(lambda: self.ShowRegister())
		
		# 다이얼로그 객체의 속성을 지정한다
		self.__txtID.setPlaceholderText("아이디")
		self.__txtPW.setPlaceholderText("비밀번호")
		self.__txtPW.setEchoMode(QLineEdit.Password)
		
		# 다이얼로그 메인프레임에 에딧 연결
		self.__layout.addWidget(self.__txtID)
		self.__layout.addWidget(self.__txtPW)
		self.__layout.addWidget(self.__btnLogin)
		self.__layout.addWidget(self.__btnRegist)
		self.setLayout(self.__layout)
		
		# 디이얼로그를 보여준다
		self.show()
		self.__app.exec_()
		
		# 실행이 종료 된 후 발생
		try:
			self.__clientApp.QuitMessage()
		except Exception as e:
			pass

	# 로그인 버튼을 누른 경우 호출되는 함수
	def ProcessLogin(self):
		#MariaDB와 연동하여 ID/PW 정보를 가져와 로그인을 시도한다
		self.__txtID.setReadOnly(True)
		self.__txtPW.setReadOnly(True)
		
		# MySQL(MariaDB) 서버에 접속한다
		db = pymysql.connect(host=self.__host, port=3306, user="Solgae", passwd="gntech2152", db="SolgaeTalk", charset="utf8", autocommit=True)
		cursor = db.cursor()
		
		# 입력받은 비밀번호를 암호화한다
		hashSHA = hashlib.sha256()
		hashSHA.update(self.__txtPW.text().strip().encode())
		hexSHA256 = hashSHA.hexdigest()
		
		# 입력받은 아이디, 암호화한 비밀번호와 동일한 레코드를 검색한다
		cursor.execute("SELECT COUNT(*) FROM Accounts WHERE userID='" + self.__txtID.text().strip() + "' AND userPW='" + hexSHA256 + "'")
		result = cursor.fetchone()
		
		# 로그인 정보가 존재하는 경우 어플리케이션을 실행한다
		if result[0] == 1:
			cursor.execute("SELECT COUNT(*) FROM Accounts WHERE userID='" + self.__txtID.text().strip() + "' AND userPW='" + hexSHA256 + "' AND online=False")
			result = cursor.fetchone()
			
			# 이미 로그인 되어 있지 않은 경우 어플리케이션을 실행한다
			if result[0] == 1:
				cursor.execute("SELECT nickname, red, green, blue FROM Accounts WHERE userID='" + self.__txtID.text().strip() + "' AND userPW='" + hexSHA256 + "'")
				result = cursor.fetchone()
				cursor.execute("UPDATE Accounts SET online=True WHERE userID='" + self.__txtID.text().strip() + "' AND userPW='" + hexSHA256 + "'")

				self.__clientApp = ClientApp(self.__host, self.__port, result[0], result[1], result[2], result[3])
				self.hide()
			
			# 이미 로그인 되어 있는 경우 오류메시지를 출력한다
			else:	
				mb = QMessageBox()
				mb.setText("이미 접속중인 계정입니다")
				mb.setIcon(QMessageBox.Warning)
				mb.setWindowTitle("솔개톡 로그인")
				mb.exec_()
				self.__txtID.setReadOnly(False)
				self.__txtPW.setReadOnly(False)
			
		# 로그인 정보가 존재하지 않는 경우 오류메시지를 출력한다
		else :
			mb = QMessageBox()
			mb.setText("아이디 또는 패스워드가 일치하지 않습니다")
			mb.setIcon(QMessageBox.Warning)
			mb.setWindowTitle("솔개톡 로그인")
			mb.exec_()
			self.__txtID.setReadOnly(False)
			self.__txtPW.setReadOnly(False)
	
	# 회원가입 버튼을 누른 경우 호출되는 함수
	def ShowRegister(self):
		# 회원가입 다이얼로그를 실행중엔 버튼 및 텍스트 에디터 사용을 막는다
		self.__txtID.setReadOnly(True)
		self.__txtPW.setReadOnly(True)
		self.__btnLogin.setEnabled(False)
		self.__btnRegist.setEnabled(False)
		
		# 회원가입 다이얼로그 생성
		registDialog = RegistDialog(self, self.__host)
		registDialog.exec_()
		
		# 다이얼로그가 닫힌 경우 버튼 및 텍스트 사용을 재개한다
		self.__txtID.setReadOnly(False)
		self.__txtPW.setReadOnly(False)
		self.__btnLogin.setEnabled(True)
		self.__btnRegist.setEnabled(True)
