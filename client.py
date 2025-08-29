import socket

# 1. 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2. 서버에 연결 (connect)
client_socket.connect(('127.0.0.1', 9999))

# 3. 데이터 송신 (send)
client_socket.sendall("안녕하세요, 서버!".encode())
# 4. 데이터 수신 (recv)
data = client_socket.recv(1024)
print(f"서버로부터 받은 데이터: {data.decode()}")

# 5. 소켓 닫기
client_socket.close()