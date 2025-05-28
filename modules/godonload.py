import requests
ua = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'
}
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
    
    

download(sid=36464)