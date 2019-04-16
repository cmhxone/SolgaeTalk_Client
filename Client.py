import socket	# 소켓 모듈 임포트
import threading	# 스레드 모듈 임포트
import struct # 구조체 모듈 임포트
import pymysql	# MySQL 모듈 임포트

# 알림음을 재생하기 위한 모듈 임포트
from playsound import playsound

# Qt 라이브러리 내의 필요 모듈들을 임포트
from PySide2.QtWidgets import QMessageBox, QPlainTextEdit, QLineEdit, QMessageBox, QListWidget
from PySide2.QtGui import QTextCharFormat, QBrush, QColor, QTextCursor
from PySide2.QtCore import Qt

class ClientSocket:
	__host : str	# 호스트를 저장할 변수(URL or IP)
	__port : int	# 포트를 저장할 변수
	__socket : socket.socket	# 클라이언트 소켓
	__running : bool	# 클라이언트 실행 여부를 저장하는 변수
	__nickname : str	# 클라이언트의 닉네임을 저장하는 변수
	__lock : threading.Lock	# 스레드 락
	
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
	def ProcessMessage(self, cursor : QTextCursor, chatlog : QPlainTextEdit, list : QListWidget):
		while True:	# 실행상태라면 계속 반복한다
			# 소켓에서 정보를 읽어온다
			data = self.__socket.recv(1024)	# 사이즈만큼의 데이터를 받아온 뒤 data 변수에 전달
			message = struct.unpack("I32s512sIII", data)	# 데이터를 언 패킹한다
			
			# 메시지 수신 플래그를 전달 받은 경우 메시지를 출력한다
			if message[0] == 5002:
				# 알림음 재생
				wavThread = threading.Thread(target=lambda: playsound("Alert.wav"), args=())
				wavThread.daemon = True
				wavThread.start()
				
				cursor[0].movePosition(cursor[0].End)
				cursor[0].beginEditBlock()
				cursor[0].insertHtml("<id style='color:rgb(" + str(message[3]) + "," + str(message[4]) + "," + str(message[5]) + "); font-weight: bold'>[" + message[1].decode().strip().replace("\0", "") + "]</id> ")
				cursor[0].movePosition(cursor[0].End)
				# HTML 태그를 이용해 프로그램 오류 유도를 방지하기 위해 메시지는 일반 텍스트로 출력한다
				cursor[0].insertText(message[2].decode().strip().replace("\0", "") + "\n")
				chatlog[0].moveCursor(chatlog[0].textCursor().End)
				cursor[0].endEditBlock()
				
				
			# 접속 플래그를 전달 받은 경우 환영 메시지를 출력한다
			elif message[0] == 1996:
				# 알림음 재생
				wavThread = threading.Thread(target=lambda: playsound("Hello.wav"), args=())
				wavThread.daemon = True
				wavThread.start()
				
				cursor[0].movePosition(cursor[0].End)
				cursor[0].beginEditBlock()
				cursor[0].insertHtml("<strong><message style='color:#707070'>[솔개톡] <id style='color:rgb(" + str(message[3]) + "," + str(message[4]) + "," + str(message[5]) + "); font-weight: bold'>" + message[1].decode().strip().replace("\0", "") + "</id>" + " 님이 솔개톡에 입장하셨습니다</message></strong>")
				cursor[0].movePosition(cursor[0].End)
				cursor[0].insertText("\n")
				chatlog[0].moveCursor(chatlog[0].textCursor().End)
				cursor[0].endEditBlock()
				
				# MySQL에 접속해 접속 중인 사용자들의 정보를 가져와 리스트에 업데이트 시킨다
				db = pymysql.connect(host=self.__host, port=3306, user="Solgae", passwd="gntech2152", db="SolgaeTalk", charset="utf8", autocommit=True)
				cur = db.cursor()
				cur.execute("SELECT nickname FROM Accounts WHERE online=True ORDER BY id DESC")
				rows = cur.fetchall()
				
				# 리스트 초기화 후 접속자 명단만 읽어들인다
				try:
					list[0].clear()
					for element in rows:
						list[0].insertItem(0, element[0])
				except:
					pass
			
			# 접속 종료 플래그를 전달 받은 경우 접속 종료 메시지를 출력한다
			elif message[0] == 2015:
				# 알림음 재생
				wavThread = threading.Thread(target=lambda: playsound("Bye.wav"), args=())
				wavThread.daemon = True
				wavThread.start()
			
				cursor[0].movePosition(cursor[0].End)
				cursor[0].beginEditBlock()
				cursor[0].insertHtml("<strong><message style='color:#707070'>[솔개톡] <id style='color: rgb(" + str(message[3]) + "," + str(message[4]) + "," + str(message[5]) + "); font-weight: bold'>" + message[1].decode().strip().replace("\0", "") + "</id>" + " 님이 솔개톡에서 퇴장하셨습니다</strong>")
				cursor[0].movePosition(cursor[0].End)
				cursor[0].insertText("\n")
				chatlog[0].moveCursor(chatlog[0].textCursor().End)
				cursor[0].endEditBlock()
				
				# MySQL에 접속해 접속 중인 사용자들의 정보를 가져와 리스트에 업데이트 시킨다
				db = pymysql.connect(host=self.__host, port=3306, user="Solgae", passwd="gntech2152", db="SolgaeTalk", charset="utf8", autocommit=True)
				cur = db.cursor()
				cur.execute("SELECT nickname FROM Accounts WHERE online=True ORDER BY id DESC")
				rows = cur.fetchall()
				
				# 리스트 초기화 후 접속자 명단만 읽어들인다
				try:
					list[0].clear()
					for element in rows:
						list[0].insertItem(0, element[0])
				except:
					pass
		
	# 소켓 서버에 메시지를 전달하는 함수
	def SendMessage(self, flag : int, msgEdit : QLineEdit, nickname : str, r : int, g : int, b : int):
		try:
			# 메시지를 패킹 후 서버에 전송한다
			data = struct.pack("I32s512sIII", flag, nickname.encode(), msgEdit[0].text().strip().encode(), r, g, b)
			msgEdit[0].clear()
			msgEdit[0].setFocus()
			self.__socket.send(data)
		
		# 타입 오류가 발생한 경우(180430)플래그 전달 시
		except TypeError as e:
			if flag == 180430:
				data = struct.pack("I32s512sIII", flag, nickname.encode(), "Update List".encode(), r, g, b)
				self.__socket.send(data)
			else:
				print(e)
		except struct.error as er:
			print(er)
