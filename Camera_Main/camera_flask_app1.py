from flask import Flask, render_template, Response, request, redirect
import cv2
import datetime
import time
import os
import numpy as np
import pyrebase
import mediapipe as mp
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler

from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
# from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score  # Accuracy metrics
import pickle
from time import time
from threading import Thread
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


global capture, rec_frame, grey, switch, neg, face, rec, out
capture = 0
grey = 0
neg = 0
face = 0
switch = 1
rec = 0

# make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

# Load pretrained face detection model
net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt',
                               './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

# instatiate flask app
app = Flask(__name__, template_folder='./templates')


camera = cv2.VideoCapture(0)


def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)


def detect_face(frame):
    global net
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    confidence = detections[0, 0, 0, 2]

    if confidence < 0.5:
        return frame

    box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
    (startX, startY, endX, endY) = box.astype("int")
    try:
        frame = frame[startY:endY, startX:endX]
        (h, w) = frame.shape[:2]
        r = 480 / float(h)
        dim = (int(w * r), 480)
        frame = cv2.resize(frame, dim)
    except Exception as e:
        pass
    return frame


def gen_frames():  # generate frame by frame from camera
    global out, capture, rec_frame
    while True:
        success, frame = camera.read()
        if success:
            if(face):
                frame = detect_face(frame)
            if(grey):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if(neg):
                frame = cv2.bitwise_not(frame)
            if(capture):
                capture = 0
                now = datetime.datetime.now()
                p = os.path.sep.join(
                    ['shots', "shot_{}.png".format(str(now).replace(":", ''))])
                cv2.imwrite(p, frame)

            if(rec):
                rec_frame = frame
                frame = cv2.putText(cv2.flip(
                    frame, 1), "Recording...", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)
                frame = cv2.flip(frame, 1)

            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass

        else:
            pass


firebaseConfig = {
    "apiKey": "AIzaSyCDxKa-AEKeqm-nFyFDh3u9j00rS_tNzqE",
    "authDomain": "posture-analytics.firebaseapp.com",
    "projectId": "posture-analytics",
    "storageBucket": "posture-analytics.appspot.com",
    "messagingSenderId": "993803643647",
    "appId": "1:993803643647:web:9c6beaa9367a66f6c83aca",
    "databaseURL": "",
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


@app.route('/', methods=['GET', 'POST'])
def basic():
    unsuccessful = 'Please check your credentials'
    successful = 'Login successful'
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            auth.sign_in_with_email_and_password(email, password)
            return redirect("/index")
        except:
            return render_template('auth.html', us=unsuccessful)

    return render_template('auth.html')


@app.route('/signup', methods=['GET', 'POST'])
def basic2():
    unsuccessful = 'Please check your credentials'
    successful = 'Login successful'
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            auth.create_user_with_email_and_password(email, password)
            return redirect("/")
        except:
            return render_template('signup.html', us=unsuccessful)

    return render_template('signup.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/pose_detect')
def pose():
    # initiate mediapipe
    mp_drawing = mp.solutions.drawing_utils  # mediapipe drawing :D
    mp_pose = mp.solutions.pose  # mediapipe pose class.
    # Setting up the Pose function.
    pose = mp_pose.Pose(static_image_mode=True,
                        min_detection_confidence=0.3, model_complexity=2)

    with open('wakandaRaisingHands_rf.pkl', 'rb') as f:
        model = pickle.load(f)

    input_video_path = 'test.avi'
    cap = cv2.VideoCapture(input_video_path)
# Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                landmarks_row = list(np.array(
                    [[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in landmarks]).flatten())

                # Make Detections
                X = pd.DataFrame([landmarks_row])
                body_language_class = model.predict(X)[0]
                body_language_prob = model.predict_proba(X)[0]
                print(body_language_class, body_language_prob)

                # Get status box
                cv2.rectangle(image, (0, 0), (250, 60), (245, 117, 16), -1)

                # Display Classification
                cv2.putText(image, 'CLASS', (95, 12),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, body_language_class.split(' ')[
                            0], (90, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                # Display Probability
                cv2.putText(image, 'PROB', (15, 12),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)], 2)), (
                    10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            except:
                pass

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(
                                          color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(
                                          color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    # link the button to this route
    # call machine learning process
    # render new html with the results on it


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/requests', methods=['POST', 'GET'])
def tasks():
    global switch, camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture = 1
        elif request.form.get('grey') == 'Grey':
            global grey
            grey = not grey
        elif request.form.get('neg') == 'Negative':
            global neg
            neg = not neg
        elif request.form.get('face') == 'Face Only':
            global face
            face = not face
            if(face):
                time.sleep(4)
        elif request.form.get('stop') == 'Stop/Start':

            if(switch == 1):
                switch = 0
                camera.release()
                cv2.destroyAllWindows()

            else:
                camera = cv2.VideoCapture(0)
                switch = 1
        elif request.form.get('rec') == 'Start/Stop Recording':
            global rec, out
            rec = not rec
            if(rec):
                frame_width = int(camera.get(3))
                frame_height = int(camera.get(4))
                now = datetime.datetime.now()
                fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
                out = cv2.VideoWriter("vid_{}.avi".format(
                    str(now).replace(":", '')), fourcc, 20.0, (frame_width, frame_height))
                # Start new thread for recording the video
                thread = Thread(target=record, args=[out, ])
                thread.start()
            elif(rec == False):
                out.release()
        # elif request.form.get("rec") == "Stop Recording":
        #     return redirect('/pose_detect')
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

camera.release()
cv2.destroyAllWindows()