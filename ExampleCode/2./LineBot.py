import Settings
import ChatGPT

import Settings
import openai
from spacy.lang.en import English
from spacy.lang.zh import Chinese
import langid
import json

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# sudo FLASK_APP=LineBot.py flask run --host=0.0.0.0 --port=80
# 請替換成您的Channel Access Token和Channel Secret
line_bot_api = LineBotApi(Settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Settings.LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route("/health", methods=['GET'])
def health():
    return 'OK', 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    anser = ChatGPT.prompt_with_gpt(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=anser)
    )

if __name__ == "__main__":
    app.run()
