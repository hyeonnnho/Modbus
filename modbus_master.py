# (실제 장비 없이 개념을 보여주기 위한 코드입니다)
# pip install pymodbus==2.5.3

from pymodbus.client.sync import ModbusTcpClient

# 통신할 장비(슬레이브)의 IP와 포트
SLAVE_IP = '127.0.0.1' 
SLAVE_PORT = 502
SLAVE_ID = 1

# 1. Modbus 클라이언트 생성 및 연결
client = ModbusTcpClient(SLAVE_IP, port=SLAVE_PORT)
client.connect()

print("Modbus 장비에 연결되었습니다.")

try:
    # 2. 데이터 읽기 요청 (마스터 -> 슬레이브)
    # "1번 장비의 100번 주소부터 5개의 데이터를 읽어줘"
    response = client.read_holding_registers(address=100, count=5, unit=SLAVE_ID)

    if not response.isError():
        print(f"읽어온 데이터: {response.registers}")
    else:
        print("데이터 읽기 실패")

    # 3. 데이터 쓰기 요청 (마스터 -> 슬레이브)
    # "1번 장비의 105번 주소에 값 255를 써줘"
    write_response = client.write_register(address=105, value=255, unit=SLAVE_ID)

    if not write_response.isError():
        print("데이터 쓰기 성공")
    else:
        print("데이터 쓰기 실패")

finally:
    # 4. 연결 종료
    client.close()
    print("Modbus 연결이 종료되었습니다.")