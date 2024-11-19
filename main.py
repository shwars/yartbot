from flask import Flask, jsonify, make_response, abort, request, send_file
import json
import requests
from PIL import Image
import io,os
from flask_cors import CORS, cross_origin
from flask_apscheduler import APScheduler
from pcardbot import PCardBot
from yandex_art import YandexArt

with open('config.json') as f:
    config = json.load(f)

app = Flask(__name__)
CORS(app)

scheduler = APScheduler()
scheduler.init_app(app)

@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'status': 'error', 'reason' : str(error) }), 500)

yart = YandexArt(config)
pcardbot = PCardBot(config['pcard_bot'],yart,None)

@app.route('/pcardhook',methods=['GET','POST'])
def pcard_hook():
    if request.method=='POST':
        post = request.json
        pcardbot.process_post(post)
    return { "ok" : True }

@scheduler.task('interval', id='check_all', seconds=5)
def check_all():
    pcardbot.check()

scheduler.start()

cert = "/home/vmuser/WORK/certs/fullchain.pem"
cert_key = "/home/vmuser/WORK/certs/privkey.pem"

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8443,ssl_context=(cert,cert_key))
