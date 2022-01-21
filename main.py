from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import monitoring_ui as mainui
import get_serial_port
import time
import datetime
import serial
import sys
import random

station = 'dump'        # thread <-> GUI 공유 전역 변수, Station 선택 값을 가짐


class SerialThread(QThread):
    """
    Station <-> GUI 시리얼 통신 스레드
    """
    data = pyqtSignal(dict)
    def __init__(self, ser, parent=None):
        super().__init__()
        self.ser = ser          # GUI, ser 정보 인자로 받음
        self.datadict = {}      # Thread > GUI 로 데이터 넘겨줄 dict

    def run(self):
        global station      # thread <-> GUI 공유 전역 변수, Station 선택 값을 가짐
        while True:
            if station == 'dump':
                # station 선택 전 & station Stop 선택 & 요청에 응답이 없을 경우
                pass
            elif station == 'close':
                # Port 닫을 시 생성 스레드 종료
                break
            else:
                # station 선택 후 값을 가질 경우
                self.ser.reset_input_buffer()
                try:
                    self.ser.write(('!' + station + 'REQ').encode())
                except Exception as e:
                    pass
                try:

                    for i in range(12):
                        dict_channel_name = 'ch' + str(i).zfill(2)
                        recv_data = self.ser.readline()
                        if recv_data == b'':
                            # 요청에 응답이 없을 시 빈 dict 출력
                            self.data.emit({})
                        recv_str = recv_data.decode()
                        channel_name, channel_volt, state, checksum = recv_str.split(',')

                        temp_sum = 0
                        for c in recv_data[:-4]:
                            temp_sum += c
                        temp_sum &= 0xFF
                        if temp_sum != int(checksum, 16):
                            # CheckSum 오류 시 ERROR 값 GUI 출력
                            channel_volt, state = 'ERROR', 'ERROR'

                        color = self.state_color(state)
                        self.datadict[dict_channel_name] = [channel_volt, state, color]

                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.datadict["time"] = now
                    self.datadict["station"] = station
                    # datadict = {'ch1': 값 ~ 'ch11': 값, 'time': 수신 시간, 'station': 현재 Station정보}
                    self.data.emit(self.datadict)

                except Exception as e:
                    pass
                time.sleep(1)

    def state_color(self, state):
        if state == 'idle':
            # 상태 idle 일 경우 000000 = 검정
            color = '#000000'
        elif state == 'char':
            # 상태 char 일 경우 ff0000 = 빨강
            color = '#ff0000'
        elif state == 'full':
            # 상태 full 일 경우 00ff00 = 초록
            color = '#00ff00'
        else:
            # 그외 상태 오류 값 수신 시 ffffff = 흰색
            color = '#ffffff'

        return color



class MainDialog(QMainWindow, mainui.Ui_MainWindow):
    def __init__(self):
        QDialog.__init__(self, None)
        self.setupUi(self)
        self.combobox_list()
        self.refresh.clicked.connect(self.combobox_list)
        self.portbtn.clicked.connect(self.combobox_port_open)
        self.connectbtn.clicked.connect(self.station_connect)
        self.Stopbtn.clicked.connect(self.station_stop)
        self.portclosebtn.clicked.connect(self.port_close)
        self.thread_cnt = 0
        self.ser = None

    def combobox_list(self):
        # GUI 시작 및 새로고침 버튼 클릭 시 포트 리스트 불러오기
        self.COMBox.clear()
        port_list = get_serial_port.serial_ports()
        for item in port_list:
            self.COMBox.addItem(item)

    def combobox_port_open(self):
        # Port 열기 상호작용
        global station
        select_port = self.COMBox.currentText()     # 포트 콤보박스 선택 텍스트 불러옴
        station = 'dump'        # global station 값 초기화
        try:
            self.ser = serial.serial_for_url(select_port, baudrate=115200, timeout=1)
            self.serial_thread = SerialThread(self.ser)     # 포트 Open > 쓰레드 시작( 시리얼 정보 스레드에 전송 )
            self.serial_thread.start()
            self.serial_thread.data.connect(self.thread_event)
            # 버튼 Enable 제어
            self.connectbtn.setEnabled(True)
            self.portclosebtn.setEnabled(True)
            self.portbtn.setEnabled(False)
            self.COMBox.setEnabled(False)
            # 상태 램프 변경
            self.port_alarm.setStyleSheet("background-color: #00ff00")

        except Exception as e:
            # Port Open Failed > 경고 창 출력
            self.port_alarm.setStyleSheet("background-color: #ff0000")
            QMessageBox.warning(self, "오류", "포트 열기 실패")

    def port_close(self):
        # Port 닫기 상호작용
        global station
        station = 'close'       # global station > close > Thread 종료
        self.ser.close()
        self.serial_thread.ser.close()      # Thread > ser 종료
        # 버튼 Enable 제어
        self.portbtn.setEnabled(True)
        self.portclosebtn.setEnabled(False)
        self.COMBox.setEnabled(True)
        self.Stopbtn.setEnabled(False)
        # 상태 램프 변경
        self.port_alarm.setStyleSheet("background-color: #ff0000")
        self.station_alarm.setStyleSheet("background-color: #ff0000")

    def station_connect(self):
        # Station Connect 상호작용
        global station
        station = self.StationBox.currentText()     # global station = Station Box 값 가져옴
        # 버튼 Enable 제어
        self.Stopbtn.setEnabled(True)
        self.connectbtn.setEnabled(False)

    def station_stop(self):
        global station
        station = 'dump'        # global station = dump 로 초기화 하여 스레드 pass 상태로 전환
        # 버튼 Enable 제어
        self.Stopbtn.setEnabled(False)
        self.connectbtn.setEnabled(True)
        # 상태 램프 변경
        self.station_alarm.setStyleSheet("background-color: #ff0000")

    def write_value(self, serial_data):
        # 스레드 > GUI 데이터 정상 수신 시 정보 입력
        # 수신 시간 정보 입력
        self.timelabel.setText(serial_data['time'])
        # 전압 정보 입력
        self.voltage_1.setText(serial_data['ch01'][0])
        self.voltage_2.setText(serial_data['ch02'][0])
        self.voltage_3.setText(serial_data['ch03'][0])
        self.voltage_4.setText(serial_data['ch04'][0])
        self.voltage_5.setText(serial_data['ch05'][0])
        self.voltage_6.setText(serial_data['ch06'][0])
        self.voltage_7.setText(serial_data['ch07'][0])
        self.voltage_8.setText(serial_data['ch08'][0])
        self.voltage_9.setText(serial_data['ch09'][0])
        self.voltage_10.setText(serial_data['ch10'][0])
        self.voltage_11.setText(serial_data['ch11'][0])
        # 상태 정보 입력
        self.status_1.setText(serial_data['ch01'][1])
        self.status_2.setText(serial_data['ch02'][1])
        self.status_3.setText(serial_data['ch03'][1])
        self.status_4.setText(serial_data['ch04'][1])
        self.status_5.setText(serial_data['ch05'][1])
        self.status_6.setText(serial_data['ch06'][1])
        self.status_7.setText(serial_data['ch07'][1])
        self.status_8.setText(serial_data['ch08'][1])
        self.status_9.setText(serial_data['ch09'][1])
        self.status_10.setText(serial_data['ch10'][1])
        self.status_11.setText(serial_data['ch11'][1])
        # 상태 램프 변경
        self.light_1.setStyleSheet("background-color: {color}".format(color=serial_data['ch01'][2]))
        self.light_2.setStyleSheet("background-color: {color}".format(color=serial_data['ch02'][2]))
        self.light_3.setStyleSheet("background-color: {color}".format(color=serial_data['ch03'][2]))
        self.light_4.setStyleSheet("background-color: {color}".format(color=serial_data['ch04'][2]))
        self.light_5.setStyleSheet("background-color: {color}".format(color=serial_data['ch05'][2]))
        self.light_6.setStyleSheet("background-color: {color}".format(color=serial_data['ch06'][2]))
        self.light_7.setStyleSheet("background-color: {color}".format(color=serial_data['ch07'][2]))
        self.light_8.setStyleSheet("background-color: {color}".format(color=serial_data['ch08'][2]))
        self.light_9.setStyleSheet("background-color: {color}".format(color=serial_data['ch09'][2]))
        self.light_10.setStyleSheet("background-color: {color}".format(color=serial_data['ch10'][2]))
        self.light_11.setStyleSheet("background-color: {color}".format(color=serial_data['ch11'][2]))
        # Station 램프 변경
        self.station_alarm.setStyleSheet("background-color: #00ff00")
        # 수신 Station 정보 입력
        self.stationname.setText("Station " + serial_data['station'])

    def wrong_value(self):
        # Thread > GUI 수신 dict 가 비어 있을 경우(요청에 응답이 없었을 경우)
        global station
        station = 'dump'        # global station > dump ( 스레드 pass 상태 전환 )
        # 경고 창 팝업
        QMessageBox.warning(self, "오류", "수신 데이터 없음!\nStation 주소를 확인해 주세요")
        # 버튼 Enable 제어
        self.connectbtn.setEnabled(True)
        self.Stopbtn.setEnabled(False)
        # 상태 램프 변경
        self.station_alarm.setStyleSheet("background-color: #ff0000")


    @pyqtSlot(dict)
    def thread_event(self, data):
        """
        Thread 데이터 전달(emit) 시 GUI에서 실행되는 함수
        :param data: Thread 에서 전달된 dict 형식 데이터
        :return: -
        """
        serial_data = data
        if serial_data == {}:
            # 빈 데이터 받았을 경우(응답이 없을 경우)
            self.wrong_value()
        else:
            # 데이터가 있을 경우
            self.write_value(serial_data)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MainDialog()
    dialog.show()
    app.exec_()


