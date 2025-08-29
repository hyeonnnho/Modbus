# --- SCADA (Modbus Master) 프로그램 (pymodbus v2.5.3 호환) ---
# 이 프로그램은 가상 계전기(Slave)에 접속하여 데이터를 읽어오는 클라이언트입니다.

# 1. 필요한 라이브러리 가져오기 (v2.5.3 버전에서는 .sync 경로를 사용합니다)
from pymodbus.client.sync import ModbusTcpClient

# 접속할 계전기(Slave)의 IP와 포트
SLAVE_IP = '127.0.0.1'
SLAVE_PORT = 502
SLAVE_ID = 0x01 # 1번 장비

# 2. Modbus 클라이언트 생성
client = ModbusTcpClient(SLAVE_IP, port=SLAVE_PORT)

try:
    # 3. 계전기에 연결
    client.connect()
    print("가상 계전기에 성공적으로 연결되었습니다.")

    # 4. 데이터 읽기 요청
    # 4-1. 전원 상태(Coil) 읽기: "1번 장비의 1번 주소(address=0) Coil 데이터를 1개 읽어줘"
    # Modbus 주소는 0부터 시작하므로, 1번 주소는 address=0 입니다.
    power_status_response = client.read_coils(address=0, count=1, unit=SLAVE_ID)

    if not power_status_response.isError():
        # .bits[0]으로 첫 번째 Coil 값에 접근
        is_power_on = power_status_response.bits[0]
        power_state_str = "ON" if is_power_on else "OFF"
        print(f"  - 현재 전원 상태: {power_state_str}")
    else:
        print("  - 전원 상태 읽기 실패")

    # 4-2. 전류량(Holding Register) 읽기: "1번 장비의 5번 주소(address=4) Register 데이터를 1개 읽어줘"
    current_value_response = client.read_holding_registers(address=4, count=1, unit=SLAVE_ID)
    
    if not current_value_response.isError():
        # .registers[0]으로 첫 번째 Register 값에 접근
        current_value = current_value_response.registers[0]
        print(f"  - 현재 전류량: {current_value} A")
    else:
        print("  - 전류량 읽기 실패")

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    # 5. 연결 종료
    client.close()
    print("가상 계전기와의 연결을 종료합니다.")
