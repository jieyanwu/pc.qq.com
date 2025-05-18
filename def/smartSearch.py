# import requests
# import json

# def smartSearch(keyword):
#     ua = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
#         'cookie': 'pgv_pvid=3316847162; pgv_info=ssid=s7288826772'
#     }
#     BASE_url = "https://luban.m.qq.com/api/public/software-manager/searchcgi?"
#     sd = f"?type=smart&callback=_cb&keyword={keyword}"
#     url = BASE_url + sd
#     res = requests.get(url=url,headers=ua).text
#     print(url)
#     return res
# print(smartSearch("wo"))

import requests
import re
import json

def smartSearch(keyword):
    ua = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
        'cookie': 'pgv_pvid=3316847162; pgv_info=ssid=s7288826772'
    }
    BASE_url = "https://luban.m.qq.com/api/public/software-manager/searchcgi?"
    sd = f"type=smart&callback=_cb&keyword={keyword}"
    url = BASE_url + sd
    res = requests.get(url=url, headers=ua).text
    # print(res)
    # 尝试提取 JSON 数据
    match = re.match(r'^_cb(.*)', res)
    # if not match:
    #     raise ValueError("无法匹配 _cb(...) 格式，响应格式异常")

    # json_str = match.group(1)

    # try:
    #     data = json.loads(json_str)
    # except json.JSONDecodeError as e:
    #     print("JSON 解析失败，错误详情：", e)
    #     print("出错的 JSON 字符串（前200字）：\n", json_str[:200])
    #     raise

    return res

# 调用函数并打印结果
result = smartSearch("wo")
print(result)
# print(json.dumps(result, indent=2, ensure_ascii=False))