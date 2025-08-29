# --- 채팅 클라이언트 (TCP/IP, 멀티스레딩 활용) ---
import socket
import threading
import sys

# 서버 설정
HOST = '127.0.0.1'
PORT = 9999

# 서버로부터 메시지를 수신하는 함수 (수신용 스레드에서 실행됨)
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                # 서버가 연결을 닫았을 때
                print("서버와의 연결이 끊겼습니다.")
                break
            
            # 서버가 보낸 닉네임 요청인지 확인
            if message == 'NICK':
                client_socket.send(nickname.encode('utf-8'))
            else:
                # 일반 메시지 출력
                print(message)
        except:
            # 오류 발생 시
            print("오류가 발생하여 연결을 종료합니다.")
            break
    client_socket.close()

# --- 메인 프로그램 로직 ---
try:
    nickname = input("사용할 닉네임을 입력하세요: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
except ConnectionRefusedError:
    print("서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
    sys.exit()

# 메시지 수신을 위한 스레드 시작
# daemon 스레드로 설정하여 메인 프로그램 종료 시 함께 종료되도록 함
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.daemon = True
receive_thread.start()

# 사용자 입력을 받아 서버로 메시지를 보내는 로직 (메인 스레드에서 실행)
print("채팅을 시작합니다. 메시지를 입력하세요.")
try:
    while True:
        message = input()
        if message == '/quit':
            break
        
        # 메시지를 "닉네임: 메시지" 형식으로 만들어 서버에 전송
        full_message = f'{nickname}: {message}'
        client_socket.send(full_message.encode('utf-8'))
except KeyboardInterrupt:
    print("\n채팅을 종료합니다.")
except:
    print("메시지 전송 중 오류가 발생했습니다.")
finally:
    client_socket.close()

