from telegram import TelegramBot
import json

welcome_msg = """
Привет! Я чат-бот, рисующий открытки с помощью YandexART! Пошлите мне краткое опиcание того, что вы хотите нарисовать, например «семейка котиков».
"""

prompt = "Открытка в акварельном стиле, мило, акварель, формы из размытых ярких пятен краски, новогодняя тематика, акварель, белый фон, обрамление картинки елочными ветками, в центре "

class PCardBot(TelegramBot):

    def __init__(self, token, red, art, gpt):
        super(PCardBot,self).__init__(token)
        self.art = art
        self.gpt = gpt
        self.red = red
        self.qname = 'pcard-queue'

    def check(self):
        while True:
            x = self.red.rpop(self.qname)
            if x is None:
                break
            x = json.loads(x)
            res = self.art.check(x['id'],return_img=False)
            if res:
                self.tg_send_photo(x['chat_id'],f"Вот ваша открытка на тему: {x['prompt']}",res)
            else:
                self.red.lpush(self.qname,json.dumps(x))

    def process(self,chat_id,text):
        if text is None or len(text)==0:
            return
        if text=='/start':
            self.tg_send(chat_id,welcome_msg)
        elif text[0] == '/':
            self.tg_send(chat_id,"Я не знаю такую команду :(")
        else:
            id = self.art.submit(prompt + text)
            if id:
                self.red.lpush(self.qname, json.dumps({ "id" : id, "chat_id" : chat_id, "prompt" : text }))
                self.tg_send(chat_id,"Побежал рисовать...")
            else:
                self.tg_send(chat_id,"Я не могу такое нарисовать.")