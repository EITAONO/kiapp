import cv2
from deepface import DeepFace
import speech3
import gpt4v_test
from flask import Flask, render_template, request, redirect, url_for
import os
import numpy as np

app = Flask(__name__)

# アップロードされたファイルを保存するディレクトリ
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# アップロードされたファイルの拡張子の制限
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    #return render_template('index.html')
    return render_template('index new.html')

@app.route("/upload", methods=["POST"])
def upload_image():
    img = cv2.imdecode(np.fromstring(request.files["image"].read(), np.uint8), cv2.IMREAD_UNCHANGED)
    cv2.imwrite("image.png", img)
    #cv2.imshow("image", img)
    #cv2.waitKey(0)
    
    result = DeepFace.analyze(img_path = "image.png", actions = ['emotion'])

# 結果の最初の要素（ここでは顔データ）を取得
    first_result = result[0]

# 感情の値を取得
    dominant_emotion = first_result['dominant_emotion']
    dominant_emotion_value = first_result["emotion"][dominant_emotion]

    print("Dominant emotion: ",dominant_emotion, "\nEmotion score: ", dominant_emotion_value)

    emotion = dominant_emotion
    emotion_value = dominant_emotion_value
    
    atmo = gpt4v_test.main_gpt("image.png")
    print(atmo)
    return speech3.say_datetime(emotion, emotion_value, atmo)
    #return [dominant_emotion]
    #return "dww" # emotion, emotion_value

#app.run(host="0.0.0.0", debug=False)
