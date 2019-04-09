import sys	# 시스템 모듈을 임포트
import threading	# 스레드 모듈 임포트
import struct	# 구조체 모듈 임포트
import Client	# 소켓 클라이언트 모듈 임포트

# Qt 라이브러리 내의 필요 모듈들을 임포트한다
from PySide2.QtWidgets import QApplication, QFrame, QPlainTextEdit, QLineEdit, QPushButton, QMessageBox
from PySide2.QtGui import QTextCursor, QTextDocument, QAbstractTextDocumentLayout

# 클라이언트 GUI 어플리케이션 클래스
class ClientApp:
	__app : QApplication	# 어플리케이션
	__frame : QFrame	# 어플리케이션의 메인 프레임
	__chatlog : QPlainTextEdit	# 채팅로그
	__msgEdit : QLineEdit	# 사용자의 메시지를 입력받는 곳
	__btnSend : QPushButton	# 전송 버튼
	__clientSocket : Client.ClientSocket	# 클라이언트 소켓 클래스 객체
	__lock : threading.Lock
	__cursor : QTextCursor	# 채팅로그의 텍스트 커서
	
	# 생성자 (인자값으로 호스트명과 포트를 전달받는다)
	def __init__(self, host : str, port : int):
		self.__lock = threading.Lock()
	
		self.__app = QApplication(sys.argv)	# 어플리케이션을 생성한다
		self.__frame = QFrame()	# 메인 프레임을 생성한다
		
		# 프레임 내의 자식객체 생성
		self.__chatlog = QPlainTextEdit()	# 채팅로그를 생성한다
		self.__msgEdit = QLineEdit()	# 메시지 입력창을 생성한다
		self.__btnSend = QPushButton("전송")	# 메시지 전송 버튼을 생성한다
		self.__cursor = QTextCursor(self.__chatlog.document())	# 채팅로그 커서를 생성한다
		
		# 프레임과 자식객체의 연동
		self.__chatlog.setParent(self.__frame)
		self.__msgEdit.setParent(self.__frame)
		self.__btnSend.setParent(self.__frame)
		
		# 자식객체들의 속성 지정
		self.__chatlog.setFont("돋움")	# 채팅로그의 폰트 조정
		self.__chatlog.setFixedSize(480, 240)	# 채팅로그의 크기 조정
		self.__chatlog.move(10, 10)		# 채팅로그의 위치 조정
		self.__chatlog.setReadOnly(True)	# 채팅로그 읽기전용 모드 지정
		self.__msgEdit.move(10, 260)	# 메시지 입력창 위치 조정
		self.__msgEdit.setFixedSize(405, 21)	# 메시지 입력창 크기 조정
		self.__btnSend.move(415, 259)	# 메시지 전송 버튼 위치 조정
		
		# 이벤트 발생 시 호출할 함수의 지정
		self.__msgEdit.returnPressed.connect(lambda: self.SendMessage())
		self.__btnSend.clicked.connect(lambda: self.SendMessage())
		
		self.InitSocket(host, port)	# 클라이언트 소켓 클래스를 초기화한다
		
		self.__frame.setFixedSize(500, 480)	# 프레임의 크기를 지정한다
		self.__frame.show()	# 메인 프레임을 보여준다
		self.__app.exec_()	# 초기화가 끝나면 어플리케이션을 실행한다
	
	# 소켓을 초기화, 접속 하는 함수
	def InitSocket(self, host : str, port : int):
		self.__clientSocket = Client.ClientSocket(host, port)
		# 서버에 접속을 실패한 경우 프로그램을 종료한다
		if not self.__clientSocket.Connect():
			exit(-1)
		# 접속에 성공한 경우 메시지 처리 함수를 별도의 스레드로 처리해준 뒤  접속 플래그를 담은 메시지를 전송
		else:
			processThread = threading.Thread(target=self.__clientSocket.ProcessMessage, args=([self.__cursor]))
			processThread.daemon = True
			processThread.start()
			self.__clientSocket.SendMessage(1996, [self.__msgEdit])
			
	# 전송버튼 또는 입력창에서 엔터를 누른경우 실행되는 함수
	def SendMessage(self):
		if not self.__msgEdit.text().strip() == "":
			self.__clientSocket.SendMessage(5002, [self.__msgEdit])