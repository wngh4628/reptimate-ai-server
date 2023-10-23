from ultralytics import YOLO

model = YOLO('yolov8n-seg.pt')

print(type(model.names), len(model.names))

print(model.names)

model.train(data='/Users/munjunho/Desktop/응용 2단계/YOLOV8/datasets/data.yaml', epochs=5000, patience=500, batch=32, imgsz=416)
