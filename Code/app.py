from flask import Flask, render_template,  request, Response, redirect
import cv2
from pipeline import Pipeline 

app = Flask(__name__)
pipeLine = Pipeline()



@app.route('/')
def login():
    return render_template('login.html')

@app.route('/test')
def test_cam():
    return render_template('webcam.html')
    
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

if __name__ == '__main__':
    app.run(debug=True)
