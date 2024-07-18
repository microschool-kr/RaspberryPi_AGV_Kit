from ultralytics import YOLO
import matplotlib.pyplot as plt

model = YOLO('yolov8n.pt')
# results = model(source='bus.jpeg', conf=0.4, show=True, save=True)
results = model(source=0, conf=0.4, show=True)
