from fastapi import FastAPI, WebSocket, Response, status
from PIL import Image

import uvicorn
import io

app = FastAPI()

PASSWORD = ''
LAST_FRAME = None

W_H = (256, 144)

@app.get('/')
async def index():
    return 'hi'

@app.get('/frame')
async def frame(res: Response):
    global LAST_FRAME

    if not LAST_FRAME:
        res.status_code = status.HTTP_404_NOT_FOUND
        return 'NO FRAME RN'
    
    return LAST_FRAME
    


# c = 0
@app.websocket('/stream')
async def stream(ws: WebSocket, auth: str):
    global c, LAST_FRAME
    print('hi')
    print(auth)
    if auth != PASSWORD:
        return await ws.close(reason='Wrong Password')
    await ws.accept()
    while True:
        
        data = await ws.receive_bytes()
        #
        # c += 1
        # with open(f'images/{c}.png', 'wb') as f:
        #     f.write(data)

        img = Image.open(io.BytesIO(data)).convert('RGB').resize(W_H, Image.Resampling.LANCZOS)

        w, h = img.size

        pixels = list(img.getdata())
        LAST_FRAME = [
            pixels[i * w:(i + 1) * w] 
            for i in range(h)
        ]
        
        await ws.send_text('OK')

if __name__ == '__main__':
    uvicorn.run('ws:app', port=2000, log_level='debug')
