from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import time
import pytz
from zhdate import ZhDate

# today = datetime.now()
# start_date = os.environ['START_DATE']
# city = "湘潭"

app_id = "wx7bb34aa80052a474"
app_secret = "dccd85b03daa8e45c72a5c92ad6e92dc"


# user_id = os.environ["USER_ID"]
# template_id = os.environ["TEMPLATE_ID"]

# 获取东八区时间
def nowDay():
    # 当前服务器时间
    aa = datetime.now()
    print('当前服务器时间===：%s' % (aa))
    # 北京时间
    utc = pytz.utc
    beijing = pytz.timezone("Asia/Shanghai")
    # 时间戳
    loc_timestamp = time.time()
    # 转utc时间 datetime.datetime 类型
    utc_date = datetime.utcfromtimestamp(loc_timestamp)
    # 转utc当地 标识的时间
    utc_loc_time = utc.localize(utc_date)
    fmt = '%Y-%m-%d %H:%M:%S'
    # 转北京时间
    beijing_time = utc_loc_time.astimezone(beijing)
    # utc 时间
    utc_time = beijing_time
    # cst时间
    cst_time = beijing_time.strftime(fmt)
    # 转datetime时间
    today = datetime.strptime(cst_time, "%Y-%m-%d %H:%M:%S")

    print('现在时间===：%s' % (today))
    return today


def get_weather(city):
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp'])


def get_count(start_date):
    today = nowDay()
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


# def get_birthday():
#     next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
#     if next < datetime.now():
#         next = next.replace(year=next.year + 1)
#     return (next - today).days

# 传入农历生日
def get_birthday(month, day):
    today = nowDay()
    # 获取当前年份加一
    year = datetime.today().year
    # 计算两个日期相差的天数
    oneDay = ZhDate(year, month, day);
    # 将当前农历生日日期转公历计算
    birthday = oneDay.to_datetime();
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
    today = nowDay()
    zhdate = ZhDate.from_datetime(today)
    return zhdate


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


# data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"one":{"value":one},"words":{"value":get_words(), "color":get_random_color()}}

json = [
    # 凌琪
    {"user_id": "o1nwI6OYWRZcKKG-Cdt3iS6n2HkE", "type": 1, "birthday_left": {"month": 7, "day": 24},
     "birthday_right": {"month": 1, "day": 7}, "template_id": "zykjLd1EuijeZtiFOhjGf8zxvMvE22PBRgPZPUwqloI",
     "know": "2022-08-16", "city": "长沙"},
    # 包贝
    {"user_id": "o1nwI6MTh3AlPIEQWNItZyV8BG6M", "type": 1, "birthday_left": {"month": 1, "day": 7},
     "birthday_right": {"month": 7, "day": 24}, "template_id": "zykjLd1EuijeZtiFOhjGf8zxvMvE22PBRgPZPUwqloI",
     "know": "2022-08-16", "city": "岳阳"}
]

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
# 沙雕文案
words = get_words()

for x in json:
    city = x.get("city")
    wea, temperature = get_weather(city)

    user_id = x.get("user_id")
    type = x.get("type")
    # 你的生日  东八区早上六点推送，实际是前一天的晚上日期，所以要加一天
    month = x.get("birthday_left").get("month")
    day = x.get("birthday_left").get("day")
    birthday_left = get_birthday(month, day)
    # 我的生日
    month = x.get("birthday_right").get("month")
    day = x.get("birthday_right").get("day")
    birthday_right = get_birthday(month, day)
    # 农历-今天
    zhToday = get_zhDate();
    today2 = ('今天是：%s' % (zhToday))
    print(today2)
    # 模板id
    template_id = x.get("template_id")
    # 相识日期 // 相恋日期
    know = x.get("know")
    love_day = get_count(know)
    
    data = None
    love = None
    if type == 1:
        love = "喜欢你喜欢你喜欢你 " + str(love_day) + " 天 "

    data = {"today": {"value": today2}, "city": {"value": city}, "weather": {"value": wea},
            "temperature": {"value": temperature}, "love_days": {"value": love},
            "birthday_left": {"value": birthday_left}, "birthday_right": {"value": birthday_right},
            "words": {"value": words, "color": get_random_color()}}
    print("1111111111")
    res = wm.send_template(user_id, template_id, data)
