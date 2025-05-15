import requests
import time
import json
BASE_url = 'https://luban.m.qq.com/api/public/softReportApi/getSoftList'

data = {
    "c":0,
    "sort":0,
    "offset":30,
    "limit":30,
}
END_num = 0
while(END_num<=30):
    END_num += 30
    url = BASE_url+"?"+f"c=0&sort=0&offset={END_num}&limit=30"
    print(END_num)
    res = requests.get(url).json()
    print(res["list"])
    # time.sleep(0.2)
# print(url)
# res = requests.get()