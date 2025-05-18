import requests
import json

def smartSearch(keyword):
    ua = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'
    }
    BASE_url = "https://luban.m.qq.com/api/public/software-manager/searchcgi?"
    keyword = "腾讯"
    sd = f"?type=smart&callback=_cb&keyword={keyword}"
    url = BASE_url + sd
    res = requests.get(url=url,headers=ua)
    return res