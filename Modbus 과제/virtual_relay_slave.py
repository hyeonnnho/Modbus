# --- 가상 계전기 (Modbus Slave) 프로그램 (최종 해결 버전) ---
#
# [가장 중요] 이 코드를 실행하기 전, 터미널에서 아래 명령어로
#            라이브러리를 지정된 버전(2.5.3)으로 재설치해야 합니다.
#
# pip uninstall pymodbus -y && pip install pymodbus==2.5.3
# ---------------------------------------------------------------------------

# 1. 필요한 라이브러리 가져오기 (pymodbus v2.5.3 기준)
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import logging

# 로깅 설정 (서버 동작을 확인하기 위함)
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


# 2. Modbus 데이터 저장 공간(Data Store) 설정
# 가상 계전기의 초기 상태를 여기서 직접 설정합니다.
# - Coil 주소 1번: 전원 상태 (초기값: False -> OFF)
# - Holding Register 주소 5번: 현재 전류량 (초기값: 0 A)
store = ModbusSlaveContext(
    co=ModbusSequentialDataBlock(1, [False] * 100),  # Coil 주소 1번부터 100개
    hr=ModbusSequentialDataBlock(5, [0] * 100)       # Holding Register 주소 5번부터 100개
)
context = ModbusServerContext(slaves=store, single=True)


# 3. Modbus TCP 서버 실행 (v2.5.3 동기 방식)
log.info("가상 계전기(Modbus Slave)를 시작합니다.")
log.info("SCADA(Master)의 접속을 '127.0.0.1' IP와 '502' 포트에서 기다립니다.")
log.info("서버를 종료하려면 Ctrl+C 를 누르세요.")

# 서버를 시작하고 계속 실행 상태를 유지합니다.
StartTcpServer(context, address=("127.0.0.1", 502))

