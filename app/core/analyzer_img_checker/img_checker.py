from ultralytics import YOLO
from os import path
from core.errors import exceptions as ex
base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

class Img_checker:
    def __init__(self, yolo_model_path):
        self.yolo_model = YOLO(yolo_model_path)

    def img_checking(self, image_path):
        resultData = self.yolo_model.predict(source=image_path, save=False, imgsz=320)
        found_gecko = False
        if len(resultData[0].boxes.cls) == 0:
            raise ex.NotGeckoImg()

        print('class_name =', self.yolo_model.names[int(resultData[0].boxes.cls)])
        class_name = self.yolo_model.names[int(resultData[0].boxes.cls)]
        if 'gecko' in class_name:
            found_gecko = True

        if not found_gecko:
            raise ex.NotGeckoImg()
