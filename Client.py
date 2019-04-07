import socket	# 소켓 모듈 임포트
import threading	# 스레드 모듈 임포트
import struct # 구조체 모듈 임포트

class ClientSocket:
	__host = str	# 호스트를 저장할 변수(URL or IP)
	__port = int	# 포트를 저장할 변수
	__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# 클라이언트 소켓
	__running = False	# 클라이언트 실행 여부를 저장하는 변수
	__nickname = str	# 클라이언트의 닉네임을 저장하는 변수
	
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
	def ProcessMessage(self):
		while self.__running:	# 실행상태라면 계속 반복한다
			# 소켓에서 정보를 읽어온다
			#try:
			data = self.__socket.recv(1024)	# 사이즈만큼의 데이터를 받아온 뒤 data 변수에 전달
			message = struct.unpack("I32s512s", data)	# 데이터를 언 패킹한다
			
			# 메시지 수신 플래그를 전달 받은 경우 메시지를 출력한다
			if message[0] == 5002:
				print("[", message[1].decode().replace("\x00", ""),  "] ", message[2].decode().replace("\x00", ""))
				
			#except:
			#	pass
	
	# 클라이언트의 닉네임을 받는 함수
	def SetNickname(self):
		self.__nickname = input("닉네임을 입력해주세요 ")
	
	# 클라이언트를 실행하는 함수
	def Start(self):
		if self.Connect():
			self.SetNickname()
			
			self.__running = True
			procThread = threading.Thread(target=self.ProcessMessage, args=())
			procThread.daemon = True
			procThread.start()
			
			# 초기 실행 시 접속 플래그를 담은 Hello 메시지를 전송한다
			data = struct.pack("I32s512s", 1996, self.__nickname.encode(), "Hello".encode())
			self.__socket.send(data)
			
			# 메시지를 입력 받는 루프
			while self.__running:
				try:
					command = input()
				except:
					break
				
				# quit 을 입력시 클라이언트를 종료한다
				if command == "/quit":
					break
				# 별도의 명령어가 아닌 경우 일반 메시지를 전송하는 플래그를 포함해 전송한다
				else:
					data = struct.pack("I32s512s", 5002, self.__nickname.encode(), command.encode())
					self.__socket.send(data)