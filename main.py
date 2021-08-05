import os
import time
from decouple import config
from PIL import Image
from PIL import ImageDraw
from nvt import NVT
from objectDetector import ObjectDetector

FILE_PATH = os.path.split(os.path.realpath(__file__))[0]
SNAPSHOT_FOLDER = os.path.join(FILE_PATH,'tmp')

NVT_URL = config('NVT_URL')
NVT_USER = config('NVT_USER')
NVT_PASS = config('NVT_PASS')
NVT_CHANNELS = config('NVT_CHANNELS')
MODEL = config('MODEL')
LABELS = config('LABELS')

def print_banner():
    print(" _____                    _____                     \n/  __ \                  /  ___|                    \n| /  \/  __ _  _ __ ___  \ `--.   ___   __ _  _ __  \n| |     / _` || '_ ` _ \  `--. \ / __| / _` || '_ \ \n| \__/\| (_| || | | | | |/\__/ /| (__ | (_| || | | |\n \____/ \__,_||_| |_| |_|\____/  \___| \__,_||_| |_|\n- (c)2021 RobinMglsk ------\n\n")

def draw_objects(image, objs):
  """Draws the bounding box and label for each object."""
  draw = ImageDraw.Draw(image)
  print(objs)
  for obj in objs:
    print(obj)
    bbox = obj.get('bbox')
    draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)], outline='red')
    draw.text((bbox.xmin + 10, bbox.ymin + 10), '%s\n%.2f' % (obj.get('label'), obj.get('score')), fill='red')

def main():
    print_banner()
    detector = ObjectDetector(MODEL, LABELS)
    detector.threshold = 0.6
    nvt = NVT(NVT_URL, NVT_USER, NVT_PASS)
    nvt.snapshotFolder = SNAPSHOT_FOLDER

    while(1):
        for channel in NVT_CHANNELS.split(','):
            image = nvt.get_snapshot(channel)
            objects, inference_time = detector.detect(image)
            
            print(f'{len(objects)} objects detected in {int(inference_time*1000)}ms')

            if len(objects) > 0:
                draw_objects(image, objects)
                image.save(os.path.join(SNAPSHOT_FOLDER, f'C{channel}_{time.time()}.jpg'))



if __name__ == '__main__':
  main()