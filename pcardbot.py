from telegram import TelegramBot

welcome_msg = """
Привет! Я чат-бот, рисующий открытки с помощью Yandex ART! Пошлите мне краткое опиcание того, что вы хотите нарисовать, например "семейка котиков".
"""

prompt = "Открытка в акварельном стиле, мило, акварель, формы из размытых ярких пятен краски, новогодняя тематика, акварель, белый фон, обрамление картинки елочными ветками, в центре "

class PCardBot(TelegramBot):

    def __init__(self, token, art, gpt):
        super(PCardBot,self).__init__(token)
        self.queue = {}
        self.art = art
        self.gpt = gpt

    def check(self):
        nqueue = {}
        for id,x in self.queue.items():
            res = self.art.check(id,return_img=False)
            if res:
                self.tg_send_photo(x['chat_id'],f"Вот ваша открытка на тему: {x['prompt']}",res)
            else:
                nqueue[id] = x
        self.queue = nqueue

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
                self.queue[id] = { "chat_id" : chat_id, "prompt" : text }
                self.tg_send(chat_id,"Побежал рисовать...")
            else:
                self.tg_send(chat_id,"Я не могу такое нарисовать.")