import time
import math
import subprocess
import pandas as pd
import random

"""def stt(audio_file):
    st = time.time()
    headers = {
        'accept': 'application/json',
        'x-gladia-key': '9399f5c0-98fa-468e-ac22-eee3f452d1b5',
    }

    files = {
        'audio': (audio_file, open(audio_file, 'rb'), 'audio/mpeg'),
        #'audio_url': (None, 'http://files.gladia.io/example/audio-transcription/split_infinity.wav'),
        #'language': (None, 'japanese'),
        'language_behaviour': (None, 'automatic single language'),
    }

    response = requests.post(
        'https://api.gladia.io/audio/text/audio-transcription/',
        headers=headers,
        files=files)

    et = time.time()
    elapsed_time = et - st

    # Save the response to a file
    with open('response.json', 'w') as f:
        f.write(response.text)

    return response, elapsed_time"""
# ファイルからiとjの値を読み込む関数
def load_values(filename):
    try:
        with open(filename, 'r') as file:
            #e_hap,v_hap,e_sad,v_sad,e_ang,v_ang,e_fea,v_fea,e_dis,v_dis,e_sur,v_sur,e_neu,v_neu = map(float, file.readline().split())
            e_hap,v_hap,e_sad,v_sad,e_ang,v_ang,e_fea,v_fea,e_dis,v_dis,e_sur,v_sur,e_neu,v_neu = map(float, file.readline().split(','))
            return e_hap,v_hap,e_sad,v_sad,e_ang,v_ang,e_fea,v_fea,e_dis,v_dis,e_sur,v_sur,e_neu,v_neu
    except FileNotFoundError:
        return None, None

# ファイルにiとjの値を保存する関数
def save_values(filename, e_hap,v_hap,e_sad,v_sad,e_ang,v_ang,e_fea,v_fea,e_dis,v_dis,e_sur,v_sur,e_neu,v_neu):
    with open(filename, 'w') as file:
        file.write(f"{e_hap},{v_hap},{e_sad},{v_sad},{e_ang},{v_ang},{e_fea},{v_fea},{e_dis},{v_dis},{e_sur},{v_sur},{e_neu},{v_neu}")




# 初回実行時、もしくはファイルが存在しない場合
"""if e_hap is None or v_hap is None or e_sad is None or v_sad is None or e_ang is None or v_ang is None or e_fea is None or v_fea is None or e_dis is None or v_dis is None or e_sur is None or v_sur is None or e_neu is None or v_neu is None:
    e_hap = 0.5
    v_hap = 0.5
    e_sad = 0.2
    v_sad = 0.2
    e_ang = 0.5
    v_ang = 0.2
    e_fea = 0.5
    v_fea = 0.2
    e_dis = 0.5
    v_dis = 0.2
    e_sur = 0.5
    v_sur = 0.5
    e_neu = 0.3
    v_neu = 0.4"""

lower_limit = 0
upper_limit = 0.7


RECORD = """
const sleep = time => new Promise(resolve => setTimeout(resolve, time))
const b2text = blob => new Promise(resolve => {
  const reader = new FileReader()
  reader.onloadend = e => resolve(e.srcElement.result)
  reader.readAsDataURL(blob)
})
var record = time => new Promise(async resolve => {
  stream = await navigator.mediaDevices.getUserMedia({ audio: true })
  recorder = new MediaRecorder(stream)
  chunks = []
  recorder.ondataavailable = e => chunks.push(e.data)
  recorder.start()
  await sleep(time)
  recorder.onstop = async ()=>{
    blob = new Blob(chunks)
    text = await b2text(blob)
    resolve(text)
  }
  recorder.stop()
})
"""

"""def record(sec, filename='audio.wav'):
  display(Javascript(RECORD))
  s = output.eval_js('record(%d)' % (sec * 1000))
  b = b64decode(s.split(',')[1])
  with open(filename, 'wb+') as f:
    f.write(b)"""

df = pd.read_csv('output4.csv')

    
def say_datetime(emotion,emotion_value,atmo):
        filename = "values.txt"
        e_hap,v_hap,e_sad,v_sad,e_ang,v_ang,e_fea,v_fea,e_dis,v_dis,e_sur,v_sur,e_neu,v_neu = load_values(filename)
        filtered_results = []
        if emotion == "happy":
                filtered_results = df[
                (df['energy'] >= e_hap) & (df['energy'] <= e_hap + 0.4) &
                (df['valence'] >= v_hap) & (df['valence'] <= v_hap + 0.4)
		]
        elif emotion == "sad":
                filtered_results = df[
                (df['energy'] >= e_sad) & (df['energy'] <= e_sad + 0.4) &
                (df['valence'] >= v_sad) & (df['valence'] <= v_sad + 0.4)
                ]
        elif emotion == "angry":
                filtered_results = df[
                (df['energy'] >= e_ang) & (df['energy'] <= e_ang + 0.4) &
                (df['valence'] >= v_ang) & (df['valence'] <= v_ang + 0.4)
                ]
        elif emotion == "fear":
                filtered_results = df[
                (df['energy'] >= e_fea) & (df['energy'] <= e_fea + 0.4) &
                (df['valence'] >= v_fea) & (df['valence'] <= v_fea + 0.4)
                ]
        elif emotion == "disgust":
                filtered_results = df[
                (df['energy'] >= e_dis) & (df['energy'] <= e_dis + 0.4) &
                (df['valence'] >= v_dis) & (df['valence'] <= v_dis + 0.4)
                ]
        elif emotion == "surprise":
                filtered_results = df[
                (df['energy'] >= e_sur) & (df['energy'] <= e_sur + 0.4) &
                (df['valence'] >= v_sur) & (df['valence'] <= v_sur + 0.4)
                ]
        elif emotion == "neutral":
                filtered_results = df[
                (df['energy'] >= e_neu) & (df['energy'] <= e_neu + 0.4) &
                (df['valence'] >= v_neu) & (df['valence'] <= v_neu + 0.4)
                ]

        if len(filtered_results) > 0:
            random_result = filtered_results.sample(n=1).iloc[0]
            url = random_result['URL']
            energy = random_result['energy']
            valence = random_result['valence']
            print(url)
            return url
        else:
            print("can't find data")
            return text
