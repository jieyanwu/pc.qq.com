import requests
import json
import concurrent.futures

# 请求头
ua = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'
}

# API 地址
BASE_URL = 'https://luban.m.qq.com/api/public/softReportApi/getSoftList'
PROXY_URL = 'https://luban.m.qq.com/api/public/software-manager/softwareProxy'

# 全局数据容器
dic = []

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

def main():
    # 设置偏移量（测试范围缩小为 30~120）
    ranges = input("输入范围，尽量为30倍数：")
    offsets = [i for i in range(30, int(ranges), 30)]
    print(f"偏移量: {offsets}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # 并发抓取主列表数据
        results = executor.map(fetch_data, offsets)

        # 合并所有结果到全局变量 dic
        for result in results:
            dic.extend(result)

        # 提取 soft_id，并确保字段存在
        sids = [item["s"] for item in dic if "s" in item]

        # 并发下载每个软件信息
        download_results = list(executor.map(download, sids)) 

    # 保存主数据到 data.json
    with open("data/data.json", "w", encoding="utf-8") as f:
        json.dump(dic, f, ensure_ascii=False, indent=2)

    # 保存下载结果到 exedata.json
    with open("data/exedata.json", "w", encoding="utf-8") as f:
        json.dump(download_results, f, ensure_ascii=False, indent=2)

    print("✅ 所有任务完成，结果已写入 data/data.json 和 data/exedata.json")

if __name__ == "__main__":
    main()