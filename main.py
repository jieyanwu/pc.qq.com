# import requests
# import time
# import json
# BASE_url = 'https://luban.m.qq.com/api/public/softReportApi/getSoftList'

# data = {
#     "c":0,
#     "sort":0,
#     "offset":30,
#     "limit":30,
# }
# dic = []
# END_num = 0
# while(END_num<=900):
#     END_num += 30
#     url = BASE_url+"?"+f"c=0&sort=0&offset={END_num}&limit=30"
#     print(END_num)
#     res = requests.get(url).json()
#     # print(res["list"])
#     for i in res["list"]:
#         dic.append(i)
#     # dic.append(res["list"])
#     # time.sleep(0.2)
# print(dic)
# with open("data.json","w",encoding="utf-8") as f:
#     json.dump(dic,f,ensure_ascii=False)
# # res = requests.get()

import requests
import json
import concurrent.futures


ua = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'
}
BASE_URL = 'https://luban.m.qq.com/api/public/softReportApi/getSoftList'
dic = []

def fetch_data(offset):
    url = f"{BASE_URL}?c=0&sort=0&offset={offset}&limit=30"
    print(f"当前获取尾: {offset}")
    response = requests.get(url,headers=ua)
    if response.status_code == 200:
        return response.json().get("list", [])
    else:
        print(f"获取失败 {offset}")
        return []

def download(sid):
    url = "https://luban.m.qq.com/api/public/software-manager/softwareProxy"
    data = {
        "cmdid":3318,
        "jprxReq[req][soft_id_list][]":sid
    }
    res = requests.post(url,headers=ua,data=data)
    print(res.status_code)
    if res.status_code == 200:
        print(res.json())
    else:
        return res.json()
    
    


def main():
    offsets = [i for i in range(30, 31931, 30)]  # Generate offsets from 30 to 900 in steps of 30

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(fetch_data, offsets)

    for result in results:
        dic.extend(result)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(dic, f, ensure_ascii=False)

if __name__ == "__main__":
    main()