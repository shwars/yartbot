from telegram import TelegramBot
import json

welcome_msg = """
Привет! Я чат-бот, рисующий букеты цветов с помощью YandexGPT и YandexART! Пошлите мне краткое опиcание того, какой букет вам нужен.
"""

prompt_gpt = "Твоя задача - придумать промпт для генеративной модели YandexART, чтобы нарисовать букет цветов. Используй только цветы, которые чаще всего есть в цветочных магазинах: Роза, Роза кустовая, Роза пионовидная, Альстромерия, Гипсофила, Диантус, Хризантема, Пион, Тюльпан, Эустома, Гиацинт, Ромашка, Гербера, Ирис, Хризантема, Листья эвкалипта. Для упаковки используй крафтовую бумагу. Обязательно подумай, какие их этих цветов и в каком количестве подходят для описанного случая, и какие цветы будут гармонировать между собой. Опиши подробно промпт для рисования букета. В ответ выдай только промпт, не используй форматирование и дополнительную разметку."

class FlowerBot(TelegramBot):

    def __init__(self, token, red, art, gpt):
        super(FlowerBot,self).__init__(token)
        self.art = art
        self.gpt = gpt
        self.red = red
        self.qname = 'flower-queue'

    def check(self):
        while True:
            x = self.red.rpop(self.qname)
            if x is None:
                break
            x = json.loads(x)
            if x['type'] == "gpt": # wainting for GPT result
                res = self.gpt.checkAsyncResult(x['id'])
                if res:
                    self.tg_send(x['chat_id'],f"Полученный от YandexGPT промпт: {res}")
                    x['full_prompt'] = res
                    id = self.art.submit(res)
                    if id:
                        x['id'] = id
                        x['type'] = 'art'
                        self.red.lpush(self.qname,json.dumps(x))
                    else:
                        self.tg_send(x['chat_id'],'Я не могу такое нарисовать.')
                else:
                    self.red.lpush(self.qname,json.dumps(x))
            else: # waiting for ART result
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
            self.gpt.instruction_text = prompt_gpt
            id = self.gpt.invokeAsync(text)
            if id:
                self.red.lpush(self.qname, json.dumps({ "type" : "gpt", "id" : id, "chat_id" : chat_id, "prompt" : text }))
                self.tg_send(chat_id,"Побежал рисовать...")
            else:
                self.tg_send(chat_id,"Я не могу такое нарисовать.")