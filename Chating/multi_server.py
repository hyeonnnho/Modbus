# --- 멀티 클라이언트 채팅 서버 (TCP/IP, 멀티스레딩 활용) ---
import socket
import threading

# 서버 설정
HOST = '127.0.0.1'  # 로컬호스트 IP
PORT = 9999

# 연결된 클라이언트들을 {소켓: 닉네임} 형태로 관리
clients = {}
clients_lock = threading.Lock() # 여러 스레드가 clients 딕셔너리에 동시 접근하는 것을 방지

# 모든 클라이언트에게 메시지를 브로드캐스트하는 함수
def broadcast(message, sender_socket=None):
    with clients_lock:
        # items()로 반복 중 딕셔너리가 변경되어도 오류가 나지 않도록 리스트로 복사
        for client_socket, nickname in list(clients.items()):
            # 메시지를 보낸 클라이언트를 제외하고 모두에게 전송
            if client_socket != sender_socket:
                try:
                    client_socket.send(message)
                except:
                    # 오류 발생 시 해당 클라이언트 제거
                    remove_client(client_socket)

# 개별 클라이언트와의 통신을 담당하는 함수 (스레드에서 실행됨)
def handle_client(client_socket):
    nickname = clients[client_socket]
    while True:
        try:
            # 클라이언트로부터 메시지 수신 (연결이 끊기면 빈 데이터 수신)
            message = client_socket.recv(1024)
            if not message:
                break # 루프를 빠져나가 finally 블록에서 클라이언트 제거
            
            # 받은 메시지를 다른 모든 클라이언트에게 전송
            broadcast(message, client_socket)
        except:
            break # 오류 발생 시 루프 종료
    
    # while 루프가 끝나면 클라이언트 연결 종료 처리
    remove_client(client_socket)

# 클라이언트 연결을 제거하는 함수
def remove_client(client_socket):
    with clients_lock:
        if client_socket in clients:
            nickname = clients[client_socket]
            del clients[client_socket]
            print(f"'{nickname}' 님이 퇴장했습니다. (현재 접속자: {len(clients)}명)")
            broadcast(f"'{nickname}' 님이 퇴장하셨습니다.".encode('utf-8'))
            client_socket.close()

# 서버 시작 함수
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    
    print(f"채팅 서버가 시작되었습니다. ({HOST}:{PORT})")

    try:
        while True:
            # 클라이언트의 연결을 수락
            client_socket, address = server_socket.accept()
            
            try:
                # 클라이언트에게 닉네임 요청
                client_socket.send('NICK'.encode('utf-8'))
                nickname = client_socket.recv(1024).decode('utf-8')
                
                with clients_lock:
                    # 클라이언트 정보 저장
                    clients[client_socket] = nickname
                
                print(f"'{nickname}' 님이 입장했습니다. ({address}) (현재 접속자: {len(clients)}명)")
                broadcast(f"'{nickname}' 님이 입장하셨습니다.".encode('utf-8'), client_socket)
                client_socket.send('서버에 연결되었습니다! (종료하려면 /quit 입력)'.encode('utf-8'))
                
                # 각 클라이언트를 위한 스레드 생성 및 시작
                thread = threading.Thread(target=handle_client, args=(client_socket,))
                thread.start()
            except:
                print(f"{address} 연결 처리 중 오류 발생")
                client_socket.close()

    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()

