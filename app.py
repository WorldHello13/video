import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)
cap = cv2.VideoCapture(0)  # 0은 기본 카메라를 나타냅니다.

def generate_frames():
    while True:
        success, frame = cap.read()  # 비디오 프레임 읽기
        if not success:
            break
        else:
            # 좌우 반전
            frame = cv2.flip(frame, 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 프레임 전송

@app.route('/')
def index():
    return render_template('templates/index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
