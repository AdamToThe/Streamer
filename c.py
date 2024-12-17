from websockets.sync.client import connect


import pyautogui
import time
import io

from PIL import Image

ip, password, dem = '', '', (256, 144)

with connect('wss://{0}/stream?auth={1}'.format(ip, password)) as ws:
    while True:
        pb = io.BytesIO()
        ss = pyautogui.screenshot()
        ss.save(pb, format='PNG')
        pb.seek(0)

        img = Image.open(pb).resize(dem, Image.Resampling.LANCZOS)
        b = io.BytesIO()
        img.save(b, format='PNG')

        r = b.getvalue()
        ws.send(r)

        message = ws.recv()
        print(f"Received: {message}")
        
        
