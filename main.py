from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

from zhdate import ZhDate

today = datetime.now()
# start_date = os.environ['START_DATE']
city = os.environ['CITY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp'])


def get_count(start_date):
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


# def get_birthday():
#     next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
#     if next < datetime.now():
#         next = next.replace(year=next.year + 1)
#     return (next - today).days

# 传入农历生日
def get_birthday(month, day):
    # 获取当前年份加一
    year = datetime.today().year
    # 计算两个日期相差的天数
    oneDay = ZhDate(year, month, day);
    # 将当前农历生日日期转公历计算
    birthday = oneDay.to_datetime();
    today = datetime.now()
    difference = birthday.toordinal() - today.toordinal()
    if difference < 0:
        year = year + 1
        day = ZhDate(year, month, day);
        birthday = day.to_datetime();
        print(birthday)
        difference = birthday.toordinal() - today.toordinal()
    print(difference)
    return difference


# 获取当前农历日期
def get_zhDate():
    date = datetime.now()
    zhdate = ZhDate.from_datetime(date)
    return zhdate


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
wea, temperature = get_weather()
# data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"one":{"value":one},"words":{"value":get_words(), "color":get_random_color()}}

json = [{"user_id": "o1nwI6OYWRZcKKG-Cdt3iS6n2HkE", "type": 1, "birthday_left": {"month": 7, "day": 24},
         "birthday_right": {"month": 1, "day": 1}},
        ]

for x in json:
    print(x)
    user_id = x.get("user_id")
    type = x.get("type")
    # 你的生日
    month = x.get("birthday_left").get("month")
    day = x.get("birthday_left").get("day")
    birthday_left = get_birthday(month, day)
    # 我的生日
    month = x.get("birthday_right").get("month")
    day = x.get("birthday_right").get("day")
    birthday_right = get_birthday(month, day)
    # 农历-今天
    today = get_zhDate();
    data = None
    love = None
    if type == 1:
        # 特殊版
        love = "这是我追你的第 " + get_count("2022-08-16") + " 天 "
        # love = "我们已经相恋 " + get_count("2022-08-16") + " 天啦 "
        data = {"today": {"value": today}, "weather": {"value": wea}, "temperature": {"value": temperature},
                "love_days": {"value": love},
                "birthday_left": {"value": birthday_left}, "birthday_right": {"value": birthday_right},
                "words": {"value": get_words(), "color": get_random_color()}}
        print("1111111111")
    else:
        # 普通版
        one = "备用备用"
        data = {"today": {"value": today}, "weather": {"value": wea}, "temperature": {"value": temperature},
                "birthday_left": {"value": get_birthday()}, "birthday_right": {"value": birthday_right},
                "words": {"value": get_words(), "color": get_random_color()}}
        print("222222")
    res = wm.send_template(user_id, template_id, data)
