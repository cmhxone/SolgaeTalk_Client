import socket	# 소켓 모듈 임포트
import threading	# 스레드 모듈 임포트
import struct # 구조체 모듈 임포트

# Qt 라이브러리 내의 필요 모듈들을 임포트
from PySide2.QtWidgets import QMessageBox, QPlainTextEdit, QLineEdit, QMessageBox

class ClientSocket:
	__host : str	# 호스트를 저장할 변수(URL or IP)
	__port : int	# 포트를 저장할 변수
	__socket : socket.socket	# 클라이언트 소켓
	__running : bool	# 클라이언트 실행 여부를 저장하는 변수
	__nickname : str	# 클라이언트의 닉네임을 저장하는 변수
	
	# 클래스 생성자
	def __init__(self, host, port):
		self.__host = host
		self.__port = port
		
	# 소켓 서버에 접속을 시도하는 함수
	def Connect(self):
		# 소켓을 생성한다
		try:
			self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print("소켓 생성 완료")
		except socket.error as er:
			print("소켓 생성 실패 : ", er)
			mb = QMessageBox()
			mb.setText("소켓 생성에 실패하였습니다")
			mb.setIcon(QMessageBox.Warning)
			mb.setWindowTitle("솔개톡")
			mb.exec_()
			return False
			
		# 소켓에 접속한다
		try:
			self.__socket.connect((self.__host, self.__port))
			print("서버 접속 성공")
			return True
		except socket.error as er:
			print("서버 접속 실패 : ", er)
			mb = QMessageBox()
			mb.setText("서버 접속에 실패하였습니다")
			mb.setIcon(QMessageBox.Warning)
			mb.setWindowTitle("솔개톡")
			mb.exec_()
			return False
	
	# 소켓 서버에서 정보를 받아오는 함수
	def ProcessMessage(self, chatlog : QPlainTextEdit):
		while True:	# 실행상태라면 계속 반복한다
			# 소켓에서 정보를 읽어온다
			data = self.__socket.recv(1024)	# 사이즈만큼의 데이터를 받아온 뒤 data 변수에 전달
			message = struct.unpack("I32s512s", data)	# 데이터를 언 패킹한다
			
			# 메시지 수신 플래그를 전달 받은 경우 메시지를 출력한다
			if message[0] == 5002:
				chatlog.appendHtml("<id style='color: #FF0000'> [" + message[1].decode().replace("\0", "") + "]</id> : <message style='color:#000000'>" + message[2].decode().replace("\0", "") + "</message>")
			# 접속 플래그를 전달 받은 경우 환영 메시지를 출력한다
			elif message[0] == 1996:
				chatlog.appendHtml("<center><id style='color: #FF0000;'>" + message[1].decode().replace("\0", "") + "</id> 님이 접속하였습니다</center>")
		
	# 소켓 서버에 메시지를 전달하는 함수
	def SendMessage(self, flag : int, msgEdit : QLineEdit):
		try:
			# 메시지를 패킹 후 서버에 전송한다
			data = struct.pack("I32s512s", flag, "테스터".encode(), msgEdit[0].text().encode())
			msgEdit[0].clear()
			msgEdit[0].setFocus()
			self.__socket.send(data)
		except struct.error as er:
			print(er)