import time
import requests
from PIL import Image
from io import BytesIO

class NVT:

    path_snapshot = 'webcapture.jpg'
    cmd_snapshot = 'snap'

    def __init__(self, url, username = None, password = None) -> None:
        self.url = url
        self.username = username
        self.password = password

    def get_snapshot(self, channel) -> Image:
        url = self.url+'/'+self.path_snapshot+'?command='+self.cmd_snapshot+'&channel='+str(channel)

        if(self.username != None and self.password != None):
            url += '&user='+self.username+'&pass='+self.password

        resp = requests.get(url)

        if(resp.status_code == 200):
            image = Image.open(BytesIO(resp.content))
            return image
        else:
           raise Exception