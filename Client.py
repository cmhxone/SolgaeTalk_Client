import socket	# 소켓 모듈 임포트
import threading	# 스레드 모듈 임포트

class ClientSocket:
	__host = str	# 호스트를 저장할 변수(URL or IP)
	__port = int	# 포트를 저장할 변수
	__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# 클라이언트 소켓
	__running = False	# 클라이언트 실행 여부를 저장하는 변수
	
	# 클래스 생성자
	def __init__(self, host, port):
		self.__host = host
		self.__port = port
		
	# 소켓 서버에 접속을 시도하는 함수
	def Connect(self):
		# 소켓을 생성한다
		try:
			__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print("소켓 생성 완료")
		except socket.error as er:
			print("소켓 생성 실패 : ", er)
			exit(-1)
			
		# 소켓에 접속한다
		try:
			self.__socket.connect((self.__host, self.__port))
			print("서버 접속 성공")
			return True
		except socket.error as er:
			print("서버 접속 실패 : ", er)
			exit(-1)
	
	# 소켓 서버에서 정보를 받아오는 함수
	def Recv(self):
		while self.__running:	# 실행상태라면 계속 반복한다
			# 소켓에서 정보를 읽어온다
			try:
				data = self.__socket.recv(1024)	# 사이즈만큼의 데이터를 받아온 뒤 data 변수에 전달
			except:
				pass
		
	
	# 클라이언트를 실행하는 함수
	def Start(self):
		if self.Connect():
			self.__running = True
			recvThread = threading.Thread(target=self.Recv, args=())
			recvThread.daemon = True
			recvThread.start()
			
			while self.__running:
				command = input()
				if command == "/quit":
					break