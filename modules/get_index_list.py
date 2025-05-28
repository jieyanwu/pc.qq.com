import requests

# 请求头
ua = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'
}

# API 地址
BASE_URL = 'https://luban.m.qq.com/api/public/softReportApi/getSoftList'

#获取主页data内容
def fetch_data(offset):
    url = f"{BASE_URL}?c=0&sort=0&offset={offset}&limit=30"
    print(f"Fetching offset: {offset}")
    try:
        response = requests.get(url, headers=ua, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("list", [])
        else:
            print(f"请求失败 [{response.status_code}]: {url}")
            return []
    except Exception as e:
        print(f"请求异常: {e}")
        return []
