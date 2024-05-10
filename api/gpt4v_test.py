import base64
import requests

# OpenAI API Key
api_key = process.env.OPENAI_KEY

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
def main_gpt(image):
    # Path to your image
    image_path = image

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": "describe the person's emotion without 'neautral' in the image in one word."#describe the person's vibe in the image in one word
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": f"data:image/jpeg;base64,{base64_image}"
                }
              }
            ]
          }
        ],
        "max_tokens": 65
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_json = response.json()
    atmo = response_json["choices"][0]["message"]["content"]
    #print(atmo)
    ##jtalk(response_json["choices"][0]["message"]["content"])
    return atmo
    #speech3.say_datetime(atmo)

