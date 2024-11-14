# 라즈베리파이 물류로봇 프로젝트  

# 환경설정 
1. 가상환경 설정 
```bash
python3 -m venv venv 
```
2. 가상환경 활성화 
```bash
source ./venv/bin/activate
```
3. pip로 필요한 라이브러리 설치
```bash
pip install -r requirements.txt
```

4. python3-rpi.gpio 설치
```bash
sudo apt-get install python3-rpi.gpio
```

# 하드웨어 연결 

## 모터 핀 정보
![Motor](/img/lineconnection.png)
## 회로도 
![schematic](/img/schematic_v1.png)

## 신호 연결
|모터|모터 드라이버|
|------|---|
|모터전원M+(좌)|MLA|
|모터전원M-(좌)|MLB|
|모터전원M+(우)|MRA|
|모터전원M-(우)|MRB|
|베터리 + |B+|
|베터리 - |B-|

|라즈베리파이 GPIO|모터드라이버|설명|
|------|---|--|
|12|AIN2|오른쪽 모터를위한  PWM 신호 입력|  
|13|AIN1|왼쪽 모터를 위한 PWM 신호 입력|
|19|DIG2|오른쪽 모터의 방향 신호 입력|
|16|DIG1|왼쪽 모터의 방향 신호 입력|


### 전원 연결
|전원|연결1|연결2|
|------|---|--|
|12V |베터리 +| 모터 드라이버 IN+|
|5V |라즈베리파이 5V IN | 모터 드라이버 OUT+|
|GND |라즈베리파이 GND | 모터 드라이버 OUT-|
|GND |베터리 - | 모터 드라이버 IN-|


## 라즈베리파이 4 
- OS버전: 64bit bookworm


## 모터드라이버 
- [MDDS10](https://robu.in/wp-content/uploads/2015/08/MDDS10-Users-Manual.pdf) 




