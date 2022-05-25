from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
)
from control import get_news,stop_work,stock,Movie
import random


app = Flask(__name__)

line_bot_api = LineBotApi('9iVoAzuZpYoRnQydwM1/wbEbxSB0lqpt1sV75ZwybJvDRC1KKzxtZQ+O1pcUesYuQ84bRy6hv28Gd5j3los88SAlS/rqJSBuuuxy7cjnA0pr1j+RNqI5VzlMNwhpgp6NSZwtggZIBpfPbijIRsdTeAdB04t89/1O/w1cDnyilFU=/j9up3hlCY5qUagxQEe1VbyQ6i9hcrChj/kYKHGxNNA9V9J1j3gBfq4aJoSvKg2MAwQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f668e830ccbea1aa15188f129ab8f948')
def Control_stock(message):
    message=message.split('\n')
    if len(message)==2:
        day=message[1]
    else:
        day=None
    text=[]
    try:
        url,data=stock(message[0],day)
        text.append(ImageSendMessage(original_content_url=url, preview_image_url=url))
        text.append(TextSendMessage(text=f'{message[0]}走勢圖'))
        text.append(TextSendMessage(text=data))
    except:
        text.append(TextSendMessage(text='輸入錯誤或功能維護中'))
    
    respond = text     
    return respond
    


def Control(message):
    text=[]
    if message == '#使用說明':
        text.append(TextSendMessage(text='輸入想要尋找的股票代號(例如:2330.tw)'))
        text.append(TextSendMessage(text='換行後可選擇加起始日期或使用預設(例如:2021-01-01)'))
        text.append(TextSendMessage(text='指令格式 #(指令文字)'))
        respond = text
    elif message =='#Hello':
        texts=['Hello','你好','Hi 很高興見到你','歡迎使用','如果有機會我會...啊!!!原來你在 Hello 剛剛我沒說什麼']
        text.append(TextSendMessage(text=texts[random.randrange(5)]))
        respond =text
    elif message == '#有趣的圖':
        cv=random.randrange(2)
        image_text=['不可以色色','圖勒?']
        image_link=['https://i.imgur.com/IFMFsr4.png','https://imgur.com/J77AOY1.png']
        text.append(TextSendMessage(text=image_text[cv]))
        text.append(ImageSendMessage(original_content_url=image_link[cv], preview_image_url=image_link[cv]) )
        respond = text
    elif message == '#最新停班停課消息':
        text.append(TextSendMessage(text=stop_work()))
        respond = text
    elif message == '#最新Yahoo新聞':
        text.append(TextSendMessage(text=get_news()))
        respond = text 
    elif message == '#目前熱門電影':
        text.append(TextSendMessage(text=Movie()))
        respond = text    
    else:
        respond =TextSendMessage(text='無相關指令!')
    return respond


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    #print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    
    message = event.message.text
    if '#' in message[0]:
        line_bot_api.reply_message(event.reply_token,Control(message))
    else:
        line_bot_api.reply_message(event.reply_token,Control_stock(message))
    
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ.get('PORT', 5000))
