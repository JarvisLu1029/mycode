from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction
import configparser
import random
import yahoo_comment as mvcm
import re
import openai
import googletrans

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

openai.api_key = config.get('openai', "openai_api_key")
model_engine = "gpt-3.5-turbo" # ChatGPT的模型引擎


@app.route('/')
def index(): 
    return "<p>Hello World!</p>"

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    message_text = event.message.text

    if message_text == '@今天吃什麼':
        food_list = ['麥當勞', '薯條', '炸雞', '小籠包', '早午餐', '壽司', '火鍋', '披薩', '炒飯', '肉圓',\
        '烤雞', '水餃', '鍋貼', '滷味', '串燒', '牛排', '泰式', '魯肉飯', '越南麵包', '甜不辣', '義大利麵',\
        '鹽水雞', '鹹酥雞', '夜市', '拉麵', '鐵板燒', ]
        food = random.choice(food_list)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text= food)
            )

    elif '@影評' in message_text:
        try:
            mvcm.movie_name = re.search(r'(.+)(?=@影評)|(?<=@影評)(.+)', message_text).group(0)
            comment_link = mvcm.get_comment_link()
            movie_comment = mvcm.get_comments(comment_link)

            buttons_template_message = TemplateSendMessage(
                alt_text='Buttons Template',
                template=ButtonsTemplate(
                    thumbnail_image_url = f"{movie_comment['pic']}",
                    title=f"{movie_comment['search_result']}",
                    text='請選擇下列其中一個選項',
                    actions=[
                        URIAction(
                            label='立即訂票',
                            uri='https://www.ezding.com.tw/'
                        ),
                        MessageAction(
                            label='看多一點影評',
                            text= '待設定'
                        ),
                        URIAction(
                            label='影評網址',
                            uri=f'{comment_link}'
                        )
                    ]
                )
            )
            del movie_comment['search_result']
            del movie_comment['pic']
            text_message = TextSendMessage(text= "\n".join([f"{key} {value}" for key, value in movie_comment.items()]))
            line_bot_api.reply_message(
                event.reply_token, 
                [text_message, buttons_template_message]
                )
            
        except TypeError :
            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage(text='搜尋不到該電影影評')
                )

    elif '@t' or '@T' in message_text:
        try:
            translator = googletrans.Translator()
            split = message_text.split()
            text = message_text[3:]
            if text == '?':
                trans = str(googletrans.LANGCODES)[1:-1].replace(', ', '\n')
            elif split[1] in googletrans.LANGCODES.values() and len(split) != 2:
                text = message_text[6:]
                trans = translator.translate(text, dest=split[1]).text
            else:
                trans = translator.translate(text, dest='zh-tw').text
            reply = TextSendMessage(text=trans)
            line_bot_api.reply_message(event.reply_token, reply)
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='使用格式: @t <語言> <要翻譯的文字>')
            )
    # elif message_text == '@location':
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text='This is keyword for @location!')
    #     )
#     else:
#         response_text = generate_response(message_text) # 使用ChatGPT生成回覆消息
        
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text=response_text)
#         )

# def generate_response(prompt):
#     # 使用OpenAI的API生成回覆消息
#     response = openai.ChatCompletion.create(
#         engine=model_engine,
#         prompt=prompt,
#         max_tokens=50,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )
#     message_text = response.choices[0].text.strip()
#     return message_text


if __name__ == '__main__': 
    app.run(debug=True, port=5000, host="0.0.0.0")
