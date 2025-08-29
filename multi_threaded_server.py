# multi_threaded_server.py
import socket
import threading

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"[{addr}] {data.decode()}")
            client_socket.sendall(data) # 받은 데이터를 그대로 돌려줌 (Echo)
    except ConnectionResetError:
        print(f"[{addr}] Connection lost.")
    finally:
        print(f"[DISCONNECTED] {addr} disconnected.")
        client_socket.close()

# --- 메인 서버 로직 ---
PORT = 55555
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# [오류 해결 1] 서버가 비정상 종료되어도 주소를 재사용할 수 있도록 설정
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', PORT))
server_socket.listen()
print(f"[LISTENING] 서버가 {PORT} 포트에서 리스닝 중...")

while True:
    # 클라이언트 연결을 수락하고
    client_socket, addr = server_socket.accept()
    # 새로운 스레드를 생성하여 클라이언트를 담당하게 함
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")