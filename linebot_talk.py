import configparser
import json, random
import requests
import argparse

# LINE 聊天機器人的基本資料
# config = configparser.ConfigParser()
# config.read('config.ini')

# ACCESS_TOKEN = config.get('line-bot', 'channel_access_token')
# user_id = config.get('line-bot', 'channel_user_id')

ACCESS_TOKEN = '86ZekFJ8hKT6IvUA/LgwtpKrz7CRIp3u9y5MsCdsVtB9+erlWTkYOA2VVeuBfuuxpkZnCT06V7pw4Eak4+8kSXpSbYbr9PMviLRnqyoDEnyV6kJmpnhPfNfOIJW6xK1Yo7NQ7Ef671cY9T7mctkwlQdB04t89/1O/w1cDnyilFU='
user_id = 'C9f97562e62b69f34038b62073a9ffd80'

def textLineBot(talk_text):
    API_URL = 'https://api.line.me/v2/bot/message/push'

    message = {
        'type': 'text',
        'text': f'{talk_text}'
    }
    data = {
        'to': user_id,
        'messages': [message]
    }
    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + ACCESS_TOKEN
    }
    response = requests.post(API_URL, data=payload, headers=headers)

def imageLineBot():
    API_URL = 'https://api.line.me/v2/bot/message/push'

    # 讀取檔案
    with open('/home/jarvis/glis/linebot/data.txt', 'r') as f:
        images_data = f.readlines()
        # 移除每一行的換行符
        images_data = [line.strip() for line in images_data]

    imageUrl = random.choice(images_data)

    message = {
        "type": "image",
        "originalContentUrl": imageUrl,
        "previewImageUrl": imageUrl
        }
    data = {
        'to': user_id,
        'messages': [message]
    }
    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + ACCESS_TOKEN
    }
    response = requests.post(API_URL, data=payload, headers=headers)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='自行輸入文字')
    parser.add_argument('-t', help='自行輸入文字')
    parser.add_argument('-i', help='自行輸入文字')
    args = parser.parse_args()

    if args.t:
        talk_text = args.t
        textLineBot(talk_text)
    
    imageLineBot()
        