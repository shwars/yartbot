import requests

verbose = True

class TelegramBot:

    def __init__(self,token):
        self.telegram_token = token

    def tg_send(self, chat_id, text):
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        requests.post(url, data=data)

    def tg_get_file(self, file_id):
        url = f"https://api.telegram.org/bot{self.telegram_token}/getFile"
        data = { "file_id": file_id }
        resp = requests.post(url, data=data)
        return resp.json()
    
    def tg_send_photo(self, chat_id, text, file):
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendPhoto"
        data = {"chat_id": chat_id, "caption": text}
        files = { "photo" : file }
        requests.post(url, data=data, files=files)

    def process_post(self,post):
        if verbose:
            print(f" + Incoming post: {post}")
        for m in ['message','edited_message']:
            if m in post.keys():
                break
        chat_id = post[m]['chat']['id']
        text = None
        if 'text' in post[m]:
            text = post[m]['text']
        if 'caption' in post[m]:
            text = post[m]['caption']
        self.process(chat_id, text)

    def process(self,chat_id,text):
        pass