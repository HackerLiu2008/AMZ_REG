import json
import time
import pymysql
from getinfo_us import data_tool
import re
#
# from selenium import webdriver
#
# driver = webdriver.Chrome()
# #
# cookies = dr.get_cookies()
# with open("cookies.txt", "w") as fp:
#     json.dump(cookies, fp)
# # #
# dr.quit()

#
# def read_cookies():
#     # 设置cookies前必须访问一次百度的页面
#     driver.get("http://www.baidu.com")
#     with open("cookies.txt", "r") as fp:
#         cookies = json.load(fp)
#         for cookie in cookies:
#             # cookie.pop('domain')  # 如果报domain无效的错误
#             driver.add_cookie(cookie)
#
#     driver.get("https://www.amazon.fr/")
#     time.sleep(20)
#     # driver.quit()

# read_cookies()

# 拿到的是cookies被转成字符串
# s = '[{"domain": ".amazon.fr", "expiry": 2082754801.629155, "httpOnly": false, "name": "session-id-time", "path": "/", "secure": false, "value": "2082754801l"}, {"domain": ".amazon.fr", "expiry": 2184229149.022969, "httpOnly": false, "name": "session-token", "path": "/", "secure": false, "value": "\"GBz45sHjfaPQOTJzeyMi4GJy5SGsBU8qdtez7Cwsb1KD2D1cZMIvEhzuTeFp0fUbiQ1yBGSQ57hwvbzqltJdWivApk8Ggcj0b0DOkkMNL2YTBdLPVmR9wk0NgnLuUg5v8vp2mF/dBv66CUwwNibAoVHb5lYKPgYyBqfjdKM1QES78ISMDR6nGN3paP0pEE0Jol8ooVL80YpHq4IYtl71Fam85rtVy18P6NrtrPSbQ90=\""}, {"domain": ".amazon.fr", "expiry": 2184229149.022972, "httpOnly": true, "name": "sess-at-acbfr", "path": "/", "secure": true, "value": "\"2+h1M0VnkZC0mh5ySW9PAKmHcBsgiboC7uEMT1lhzBE=\""}, {"domain": ".amazon.fr", "expiry": 2082754801.629156, "httpOnly": false, "name": "session-id", "path": "/", "secure": false, "value": "261-3444454-5179851"}, {"domain": ".amazon.fr", "expiry": 2184229149.022971, "httpOnly": true, "name": "at-acbfr", "path": "/", "secure": true, "value": "Atza|IwEBIPICGJE47uTkzcWtJiSro994lCKNW2zX8EcVgcoQsP1esy2EAAixVOKyUGee22XEJZCYIAjmMWBL2CIDghIGnbRsHXhCcDpzfvmA3i3MbS0rFpkpblpsGQi4uLjz0p23rkhNYyQRIJxQdfxKyrp-raPftyzLJF_JSh9xrwbyGh4nEtbpAR9C-3vKqCrMLEpNIrE0HySAh5LPo1S8O7clSnXXNjblP0219FLdPQmra7kfGFA-DmfWBEYGfE_Oxi2aRcv1SOq77w4txoAw8roEKgxc7BnDfll_fqs9kvGM-mAjd5975J-ZIRGjwn-H4tSywZdsEoYmEWpj8tAtOG2WRAIvkzNLAbhStXnAgcsx-_fEheVAL-PJYV1Xt9apfoYn0sa-oFCOYHCsthyQ0xbKmRZ_"}, {"domain": ".amazon.fr", "expiry": 2082754801.629154, "httpOnly": false, "name": "ubid-acbfr", "path": "/", "secure": false, "value": "260-4939874-1440307"}, {"domain": ".amazon.fr", "expiry": 2184229149.02297, "httpOnly": false, "name": "x-acbfr", "path": "/", "secure": false, "value": "irKRXPfWa0GygGuS2O1A8Sp7nqHynjHlfET204HBQyXYapCv0rb0s70iZtgltTTL"}, {"domain": ".amazon.fr", "expiry": 1553509989.022967, "httpOnly": false, "name": "a-ogbcbff", "path": "/", "secure": false, "value": "1"}, {"domain": ".amazon.fr", "expiry": 2184229149.022973, "httpOnly": true, "name": "sst-acbfr", "path": "/", "secure": true, "value": "Sst1|PQEkZYWKOSG-nHWvSEOtQJvrC3algG4rg8-69Qi_Gn8p0_TwOMh8zMCVQ5TrZYc09PWzV_DrLy4_abe6jxb1FqbYbm_pEjqf1tIrlECQWEvTkmAWt_A-ZYMS4beJonRuhunM9cVPdrRTkwqcXZ4b9MRKTwfjgX_WjKYXeq-gY14eioc6Td75ojqfzZJtk5qX4WytM0ttr4AKOK6juXSefev9qAFLJSzV8fPqu6GQCC1r1QpKZMorpRHTPR5fAPO-VkHwlCOcWbisIq3dzxzVqLnngtNO2jlIitsyrT0wDHB2fZvfIN9TYHjSHP7ZmelNmAWCW8OPCOKaDBFcMYWukoSG0A"}, {"domain": ".amazon.fr", "expiry": 2082754801.884968, "httpOnly": false, "name": "x-wl-uid", "path": "/", "secure": false, "value": "1Qikhw80XFhm6lejyt9T4zM1+TZUynnIYZTsKHtdm9VIX0O5U9jzm0GqO1nGitc2TX+vZq1SHTTfd/TS86EgnD4sXqhxO2XPQMS43kopnwsQK5VEVSrGyfK/FQHi4eyJuH8Up0oIsU5A="}, {"domain": "www.amazon.fr", "expiry": 1613989162, "httpOnly": false, "name": "csm-hit", "path": "/", "secure": false, "value": "tb:s-N0TECW7Z0VGD6XMK5BTD|1553509162203&t:1553509162339&adb:adblk_no"}]'
#
# # 直接写入数据，s里的‘\’就没有了
# pass
#
# # 只能先存txt，在读取出来，在判断，一个变成两个
# with open("cookies.txt", "w") as fp:
#     json.dump(s, fp)
#
#  f = open('cookies.txt', 'r')
# s = ""
# for i in f.read():
#     if i == "\\":
#         i = "\\\\"
#     s += i
# f.close()
