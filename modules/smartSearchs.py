import requests
import re
import json

def smart_search(keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
        'cookie': 'pgv_pvid=3316847162; pgv_info=ssid=s7288826772'
    }

    base_url = "https://luban.m.qq.com/api/public/software-manager/searchcgi?"
    query_string = f"type=smart&callback=_cb&keyword={keyword}"
    url = base_url + query_string

    response = requests.get(url, headers=headers)
    raw_response = response.text.strip()  # 去除首尾空白字符

    apps_data = []

    # 使用最宽容的正则表达式提取 _cb(...) 中的内容
    match = re.search(r'^_cb$$(.+?)$$', raw_response, re.DOTALL)

    if match:
        json_str = match.group(1)
        try:
            data = json.loads(json_str)
            apps_data = data['data']['pc']['app']
        except json.JSONDecodeError as e:
            print("❌ JSON 解析失败：", e)
    else:
        # 备用方案：直接去掉 _cb( 和 ) 后解析
        if raw_response.startswith('_cb(') and raw_response.endswith(')'):
            json_str = raw_response[4:-1]  # 去掉 _cb( 和结尾 )
            try:
                data = json.loads(json_str)
                apps_data = data['data']['pc']['app']
            except json.JSONDecodeError as e:
                print("❌ 备用解析失败：", e)
        else:
            print("❌ 数据格式异常，无法解析。")

    return apps_data