#根据sid获取下载直链
import requests
import json
ua = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'
}
PROXY_URL = 'https://luban.m.qq.com/api/public/software-manager/softwareProxy'

def download(sid):
    data = {
        "cmdid": 3318,
        "jprxReq[req][soft_id_list][]": sid
    }
    print(f"下载软件 ID: {sid}")
    try:
        res = requests.post(PROXY_URL, headers=ua, data=data, timeout=10)
        result = res.json()
        print(f"状态码 {res.status_code}: {result}")
        return result
    except Exception as e:
        print(f"下载失败: {e}")
        return {"error": str(e), "sid": sid}