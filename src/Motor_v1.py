from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep

# 모터드라이버 핀 설정
AIN2 = PWMOutputDevice(12)
AIN1 = PWMOutputDevice(13)
DIG2 = DigitalOutputDevice(19)
DIG1 = DigitalOutputDevice(16)

# 모터 초기화 함수
def initialize_motors():
    AIN1.value = 0
    AIN2.value = 0
    DIG1.off()
    DIG2.off()

# 전진 함수
def move_forward(speed=1.0):
    AIN1.value = speed
    AIN2.value = speed
    DIG1.on()
    DIG2.on()

# 후진 함수
def move_backward(speed=1.0):
    AIN1.value = speed
    AIN2.value = speed
    DIG1.off()
    DIG2.off()

# 시계방향 회전 함수
def rotate_clockwise(speed=1.0):
    AIN1.value = speed
    AIN2.value = 0
    DIG1.on()
    DIG2.off()

# 반시계방향 회전 함수
def rotate_counterclockwise(speed=1.0):
    AIN1.value = 0
    AIN2.value = speed
    DIG1.off()
    DIG2.on()

# 정지 함수
def stop():
    AIN1.value = 0
    AIN2.value = 0
    DIG1.off()
    DIG2.off()

# 메인 루프
if __name__ == '__main__':
    try:
        initialize_motors()
        
        while True:
            # 전진
            print("Moving forward")
            move_forward()
            sleep(2)
            stop()
            sleep(1)

 #           # 후진
 #           print("Moving backward")
 #           move_backward()
 #           sleep(2)
 #           stop()
 #           sleep(1)

 #           # 시계방향 회전
 #           print("Rotating clockwise")
 #           rotate_clockwise()
 #           sleep(2)
 #           stop()
 #           sleep(1)

 #           # 반시계방향 회전
 #           print("Rotating counterclockwise")
 #           rotate_counterclockwise()
 #           sleep(2)
 #           stop()
 #           sleep(1)
    
    except KeyboardInterrupt:
        stop()
        print("Program stopped")

