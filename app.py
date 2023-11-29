import cv2
import asyncio
import websockets
import base64

# 웹 소켓 서버 설정
async def server(websocket, path):
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 이미지 좌우 반전
        frame = cv2.flip(frame, 1)

        # 이미지를 base64로 인코딩
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_base64 = base64.b64encode(img_encoded.tobytes()).decode('utf-8')

        # 웹 소켓으로 이미지 전송
        await websocket.send(img_base64)

    cap.release()

start_server = websockets.serve(server, "localhost", 8765)

# 비동기 이벤트 루프 시작
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
