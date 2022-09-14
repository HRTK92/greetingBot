from datetime import datetime
from pytz import timezone
import json
import os

from jinja2 import Template
import requests
from linebot import LineBotApi
from linebot.models import FlexSendMessage

from dotenv import load_dotenv
load_dotenv()

line_bot_api = LineBotApi(os.getenv('channel_access_token'))

class Greeting:
    def __init__(self):
        self.today = datetime.now(timezone('Asia/Tokyo')).strftime('%m月%d日')
        self.wday = datetime.now(timezone('Asia/Tokyo')).strftime('%a')
        self.message = ''
        self.quotation = ''
        self.weather = ''

    def day(self):
        return self.today

    def setMessage(self, message):
        self.message = message

    def setQuotation(self, text, auther):
        self.quotation = [text, auther]

    def setWeather(self, text):
        self.weather = text

    def flex(self):
        template = Template(
            """
{
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "{{hello_send_message}}",
            "size": "xl",
            "wrap": true
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "今日は"
              },
              {
                "type": "text",
                "size": "xxl",
                "align": "center",
                "text": "{{today_ja}}"
              },
              {
                "type": "text",
                "text": "です。",
                "align": "end"
              }
            ]
          },
          {
            "type": "separator"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "今日の名言",
                "size": "xl"
              },
              {
                "type": "text",
                "wrap": true,
                "text": "{{geted_Quotations[0]}}",
                "style": "italic"
              },
              {
                "type": "text",
                "text": "by {{geted_Quotations[1]}}",
                "size": "xs",
                "align": "end",
                "style": "italic"
              }
            ]
          }
        ]
      }
    },
    {
      "type": "bubble",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "{{geted_weather[\"title\"]}}",
            "size": "lg",
            "wrap": true
          }
        ]
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "contents": [
              {
                "type": "span",
                "text": "天気: {{geted_weather[\"forecasts\"][0][\"telop\"]}}"
              },
              {
                "type": "span",
                "text": "最高気温: {{geted_weather[\"forecasts\"][0][\"temperature\"][\"max\"][\"celsius\"]}}"
              }
            ]
          },
          {
            "type": "text",
            "text": "近日実装予定",
            "wrap": true
          }
        ]
      }
    }
  ]
}
            """
        )
        ren_s = template.render(
            hello_send_message=self.message,
            today_ja=f'{self.today}({self.wday})',
            geted_weather=self.weather,
            geted_Quotations=self.quotation,
        )
        return ren_s

    def debug(self):
        print(self.today)
        print(self.wday)
        print(self.message)
        print(quotation)


greeting = Greeting()

messages = json.load(open('config/greetings.json', 'r'))
try:
    messages[greeting.day()]
    message = messages[greeting.day]
except:
    message = 'おはようございます'
greeting.setMessage(message)

quotation = requests.post(
    "https://meigen.doodlenote.net/api/json.php"
).json()[0]
greeting.setQuotation(quotation['meigen'], quotation['auther'])

greeting.setWeather(requests.get(
    "https://weather.tsukumijima.net/api/forecast/city/110010"
).json()
)

print(greeting.flex())
line_bot_api.push_message(
    os.getenv('groupId'),
    FlexSendMessage(alt_text="おはようございます。",
                    contents=json.loads(greeting.flex())),
)
