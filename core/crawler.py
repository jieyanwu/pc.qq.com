import json
import concurrent.futures
from modules.get_download_url import download
from modules.get_index_list import fetch_data

def run_crawler():
    try:
        # 全局数据容器
        dic = []
        # 设置偏移量（测试范围缩小为 30~120）
        ranges = input("输入范围，尽量为30倍数：(默认120)") or  "120"
        if not ranges.isdigit() or int(ranges) < 31:
            print("输入无效，请输入一个大于30的数字。")
            return
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
    except KeyboardInterrupt:
        print("\n\n♦️ 用户已中断程序。")
        exit(0)