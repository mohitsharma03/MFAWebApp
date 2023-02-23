from flask import Flask, render_template,  request, Response, redirect
from flask_cors import CORS
import cv2
import numpy as np
import base64

from pipeline import Pipeline 

app = Flask(__name__)
CORS(app)
pipeLine = Pipeline()



@app.route('/')
def login():
    return render_template('login.html')

@app.route('/test')
def test_cam():
    return render_template('webcam.html')
    
@app.route('/sendImages', methods=['POST'])
def image_process():
    prev = data_uri_to_cv2_img(request.form["prev"])
    curr = data_uri_to_cv2_img(request.form["curr"])
    ret = pipeLine.pipeline2(prev,curr)
    ret = base64.b64encode(ret)
    return Response(ret)

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

#@app.route('/video_feed')
#def video_feed():
#   return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img
if __name__ == '__main__':
    app.run(debug=True)
