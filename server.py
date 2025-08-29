import socket

# 1. 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2. 주소 할당 (bind)
server_socket.bind(('127.0.0.1', 9999))
# 3. 연결 대기 (listen)
server_socket.listen()

print("서버가 클라이언트의 연결을 기다립니다...")
# 4. 연결 수락 (accept)
client_socket, addr = server_socket.accept()
print(f"{addr} 에서 클라이언트가 접속했습니다.")

# 5. 데이터 수신 (recv) 및 송신 (send)
data = client_socket.recv(1024)
print(f"받은 데이터: {data.decode()}")
client_socket.sendall("메시지를 잘 받았습니다!".encode())

# 6. 소켓 닫기
client_socket.close()
server_socket.close()