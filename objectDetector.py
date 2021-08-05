import time
import os

from PIL import Image

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
MODEL_DIR = 'models'

class ObjectDetector:

    threshold = 0.4

    __interpreter = None
    __model = None;

    def __init__(self, model, labels) -> None:
        if self.__checkIfModelFileExists(model):
            self.__model = model
        else:
            raise Exception('Model not found')

        if self.__checkIfLabelsFileExists(labels):
            self.__labels = read_label_file(os.path.join(MODEL_DIR, labels))
        else:
            raise Exception('Model not found')

        self.__interpreter = make_interpreter(os.path.join(MODEL_DIR, self.__model))
        self.__interpreter.allocate_tensors()
        return

    def getModel(self):
        return self.__model

    def detect(self, image):
        _, scale = common.set_resized_input(self.__interpreter, image.size, lambda size: image.resize(size, Image.ANTIALIAS))
        start = time.perf_counter()
        self.__interpreter.invoke()
        inference_time = time.perf_counter() - start
        objects = detect.get_objects(self.__interpreter, self.threshold, scale)
        return self.__addLabelsToObjects(objects), inference_time


    def __checkIfLabelsFileExists(self, labels) -> bool:
        return self.__checkIfModelFileExists(labels)

    def __checkIfModelFileExists(self, model) -> bool:
        return os.path.exists(os.path.join(MODEL_DIR, model))

    def __addLabelsToObjects(self, objects):
        newObjects = [];
        for object in objects:
            newObject = {
                'id': object.id,
                'label': self.__labels.get(object.id, 'Undefined'),
                'score': object.score,
                'bbox': object.bbox,
            }
            newObjects.append(newObject)
        return newObjects