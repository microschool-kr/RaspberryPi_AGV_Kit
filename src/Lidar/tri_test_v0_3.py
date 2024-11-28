import os
import ydlidar
import time

MIN_SCAN_TIME = 0.001 #최소 스캔 시간 설정 

if __name__ == "__main__":
    ydlidar.os_init();
    ports = ydlidar.lidarPortList();
    port = "/dev/ydlidar";
    for key, value in ports.items():
        port = value;
        print(port);
    laser = ydlidar.CYdLidar();
    laser.setlidaropt(ydlidar.LidarPropSerialPort, port);
    laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 128000);
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE);
    laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL);
    laser.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0);
    laser.setlidaropt(ydlidar.LidarPropSampleRate, 3);
    laser.setlidaropt(ydlidar.LidarPropSingleChannel, True);
    laser.setlidaropt(ydlidar.LidarPropMaxAngle, 180.0);
    laser.setlidaropt(ydlidar.LidarPropMinAngle, -180.0);
    laser.setlidaropt(ydlidar.LidarPropMaxRange, 16.0);
    laser.setlidaropt(ydlidar.LidarPropMinRange, 0.08);
    laser.setlidaropt(ydlidar.LidarPropIntenstiy, False);

    ret = laser.initialize();
    if ret:
        ret = laser.turnOn();
        scan = ydlidar.LaserScan();
        while ret and ydlidar.os_isOk() :
            r = laser.doProcessSimple(scan);
            if r:
                if scan.config.scan_time < MIN_SCAN_TIME:
                    hz = 0
                else:
                    hz = 1.0/scan.config.scan_time
                # scan.stamp : 측정 시간
                # scan.point.size(): 측정된 포인트 개수 
                # 1.0/scan.config.scan_time: 실제 스캔 주파수 
                #print("Scan received[",scan.stamp,"]:",scan.points.size(),"ranges is [",1.0/scan.config.scan_time,"]Hz");
                print("Scan received[",scan.stamp,"]:",scan.points.size(),"ranges is [",hz,"]Hz");
                # 더 많은 포인트와 전체 각도 범위를 보기위해 수정 
                for i, point in enumerate(scan.points):
                    #if i < 5: #처음 5개의 포인트만 출력(전체를 출력하면 너무 많음)
                    if i % (scan.points.size() // 8) == 0:
                        angle = point.angle # 각도 (라디안)
                        distance = point.range # 거리 (미터)
                        print(f"Point {i}: 각도 = {angle * 180 / 3.14159:.2f}도, 거리 = {distance:.3f}m")
                distances = [point.range for point in scan.points]
                print(f"Min distance: {min(distances):.3f}m")
                print(f"Max distance: {max(distances):.3f}m")
            else :
                print("Failed to get Lidar Data")
            time.sleep(0.05);
        laser.turnOff();
    laser.disconnecting();
