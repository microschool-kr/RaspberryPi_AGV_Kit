import os
import ydlidar
import time

if __name__ == "__main__":
    # LiDAR 초기화
    ydlidar.os_init()

    # 사용 가능한 포트 확인
    ports = ydlidar.lidarPortList()
    port = "/dev/ttyUSB0"
    for key, value in ports.items():
        port = value
        print("사용 가능한 포트:", port)

    # LiDAR 객체 생성
    laser = ydlidar.CYdLidar()
    laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
    laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 128000)
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
    laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
    laser.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0)
    laser.setlidaropt(ydlidar.LidarPropSampleRate, 3)
    laser.setlidaropt(ydlidar.LidarPropSingleChannel, True)
    laser.setlidaropt(ydlidar.LidarPropMaxAngle, 360.0)
    laser.setlidaropt(ydlidar.LidarPropMinAngle, 1.0)  # 각도를 1도에서 359도까지
    laser.setlidaropt(ydlidar.LidarPropMaxRange, 16.0)
    laser.setlidaropt(ydlidar.LidarPropMinRange, 0.08)
    laser.setlidaropt(ydlidar.LidarPropIntenstiy, False)

    # LiDAR 연결 및 초기화
    ret = laser.initialize()
    if ret:
        # LiDAR가 성공적으로 연결되었으면
        print("LiDAR 연결 성공!")

        # 스캔 모드 시작
        ret = laser.turnOn()
        if ret:
            # LiDAR 스캔 시작
            print("LiDAR 스캔 시작...")
            scan = ydlidar.LaserScan()
            first_scan = True
            angle_increment = (359.0) / 359  # 각도 간격 (최대 359 포인트 기준으로 359도)

            # 스캔 데이터 수집 루프
            while ret and ydlidar.os_isOk():
                r = laser.doProcessSimple(scan)
                
                # 첫 번째 스캔에서는 scan_time이 0일 수 있으므로 무시하고 처리
                if scan.config.scan_time != 0 or first_scan:
                    first_scan = False
                    print("Scan received[", scan.stamp, "]:", len(scan.points), "ranges is [", 1.0 / scan.config.scan_time if scan.config.scan_time != 0 else 0, "]")
                    if r:
                        # 스캔 데이터에서 각 포인트의 거리와 각도를 10의 배수인 각도만 출력
                        for i, point in enumerate(scan.points):
                            angle = (i * angle_increment) % 360  # 각도를 정확하게 계산하고 360도로 제한
                            if angle % 10 == 0:  # 각도가 10의 배수일 때만 출력
                                distance = round(point.range * 100, 2)  # cm 단위로 변환하고 소수점 2자리로 출력
                                print(f"Distance: {distance} cm, Angle: {round(angle)}°")
                else:
                    print("Error: scan_time is zero! Waiting for the first scan...")
                
                # 잠시 대기 후 다시 시도
                time.sleep(0.1)
        else:
            print("LiDAR 스캔 시작 실패")
        
        # 스캔 종료 및 LiDAR 연결 해제
        laser.turnOff()
        laser.disconnecting()
    else:
        print("LiDAR 연결 실패")
