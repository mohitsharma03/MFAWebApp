from flask import Flask, render_template,  request, Response, redirect
import cv2
import face_recognition
from pipeline import Pipeline 
#import dlib

app = Flask(__name__)
pipeLine = Pipeline()


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/video_feed', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    # Replace the following code with your authentication logic
    if username == 'admin' and password == 'password':
        #return render_template('face.html')
        return Response(pipeLine.runPipeline(), mimetype='multipart/x-mixed-replace; boundary=frame')

    else:
        #return redirect('/error', code=302)
        return redirect('/error')

@app.route('/error')
def errorPg():
   return 'Incorrect username or pass'

def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            face_locations = face_recognition.face_locations(frame)
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#@app.route('/video_feed')
#def video_feed():
#   return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
