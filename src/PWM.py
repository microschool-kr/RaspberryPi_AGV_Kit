from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep
import signal 
import sys 

# 모터 드라이버 핀 설정
AIN2 = PWMOutputDevice(12)  # 왼쪽 모터 PWM 제어: GPIO12 (PWM0)
AIN1 = PWMOutputDevice(13)  # 오른쪽 모터 PWM 제어: GPIO13 (PWM1)
DIG2 = DigitalOutputDevice(23)  # 왼쪽 모터 신호 방향: GPIO23
DIG1 = DigitalOutputDevice(24)  # 오른쪽 모터 신호 방향: GPIO24

def motor_forward(speed):
    """ 모터를 앞으로 회전시키는 함수 """
    AIN1.value = speed  # PWM0으로 속도 설정
    AIN2.value = 0      # PWM1은 0으로 설정
    DIG1.on()           # 방향 설정
    DIG2.off()

def motor_backward(speed):
    """ 모터를 뒤로 회전시키는 함수 """
    AIN1.value = 0      # PWM0은 0으로 설정
    AIN2.value = speed  # PWM1으로 속도 설정
    DIG1.off()          # 방향 설정
    DIG2.on()

def motor_stop():
    """ 모터를 정지시키는 함수 """
    AIN1.value = 0
    AIN2.value = 0
    DIG1.off()
    DIG2.off()

def signal_handler(sig, frame):
    print("Program terminated")
    motor_stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    while True:
        #print("Motor forward at full speed")
        #motor_forward(1.0)  # 모터를 최대 속도로 앞으로 회전
        #sleep(2)  # 2초간 회전

        #print("Motor stop")
        #motor_stop()  # 모터 정지
        #sleep(2)  # 2초간 정지

        #print("Motor backward at half speed")
        #motor_backward(0.5)  # 모터를 절반 속도로 뒤로 회전
        #sleep(2)  # 2초간 회전

        print("Motor stop")
        motor_stop()  # 모터 정지
        sleep(2)  # 2초간 정지

except KeyboardInterrupt:
    print("Program terminated")
    #motor_stop()  # 프로그램 종료 시 모터 정지
    signal_handler(None, None)

