import json
import requests
import os
import io
from PIL import Image
import base64

class YandexArt:
    def __init__(self,config):
        self.folder_id = config['folder_id']
        self.api_key = config['api_key']

    def call_api(self, url, data):
        headers = { "Authorization" : f"Api-Key {self.api_key}" }
        return requests.post(url, json=data, headers=headers).json()

    def call_api_get(self, url, data):
        headers = { "Authorization" : f"Api-Key {self.api_key}" }
        return requests.get(url, headers=headers).json()

    def submit(self,prompt):
        res = self.call_api("https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync",
        {
            "modelUri": f"art://{self.folder_id}/yandex-art/latest",
            "messages": [
            {
                "weight": 1,
                "text": prompt
            }
            ]
        })
        if 'error' in res:
            print(res)
            return None
        return res['id']
    
    def decode_image(self,base64_str, return_img=True):
        file = io.BytesIO(base64.decodebytes(bytes(base64_str, "utf-8")))
        return Image.open(file) if return_img else file

    def check(self,id, return_img = True):
        res = self.call_api_get(f"https://llm.api.cloud.yandex.net:443/operations/{id}",{})
        if 'done' in res and res['done']:
            return self.decode_image(res['response']['image'],return_img)
        else:
            return None
