import cv2
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64

app = Flask(__name__)
socketio = SocketIO(app)
cap = cv2.VideoCapture(0)  # Change the camera index if needed

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = base64.b64encode(buffer.tobytes()).decode('utf-8')
            socketio.emit('video_frame', {'frame': frame}, namespace='/video_stream')
            socketio.sleep(0.01)

@socketio.on('connect', namespace='/video_stream')
def connect():
    print('Client connected')
    socketio.start_background_task(target=generate_frames)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)