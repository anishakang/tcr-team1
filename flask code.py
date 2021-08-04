import json,time
from new import Video
from flask import Flask, render_template, request, jsonify, Response
import requests
import base64,cv2


app=Flask(_name_)
output=[]
@app.route('/')
def home_page():
    return render_template('task.html')


def gen(camera):
    while True:

        frame=camera.detector()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Video()), mimetype='multipart/x-mixed-replace; boundary=frame')


if _name=="main_":
    app.run(debug=True)#,host="192.168.43.161")