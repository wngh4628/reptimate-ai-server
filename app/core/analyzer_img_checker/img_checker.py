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
        # 가장 높은 신뢰도를 갖는 인덱스를 찾기
        confidences = resultData[0].boxes.conf
        max_conf_index = confidences.argmax()

        # 해당 인덱스에 대응하는 클래스 가져오기
        class_index = int(resultData[0].boxes.cls[max_conf_index])
        class_name = self.yolo_model.names[class_index]
        if 'gecko' in class_name:
            found_gecko = True

        if not found_gecko:
            raise ex.NotGeckoImg()
