import json
import concurrent.futures
from modules.get_download_url import download
from modules.get_index_list import fetch_data


def run_crawler(mode, num, workers):
    try:
        # 全局数据容器
        dic = []

        print("请选择抓取模式：")
        print("1. 按循环次数（每组30个）")
        print("2. 按总数据量（自动计算循环次数）")
        selected_mode = str(mode)
        if selected_mode not in ["1", "2"]:
            print("❌ 输入无效，请选择 1 或 2。")
            return None

        if selected_mode == "1":
            times = int(num)
            if times < 1:
                print("❌ 循环次数必须大于等于1")
                return None
            offsets = [i * 30 for i in range(times)]
            print(f"✅ 已设置为按【{times}次】抓取，每组30条")
        else:
            total = int(num)
            if total < 1:
                print("❌ 总数据量必须大于等于1")
                return None
            times = (total + 29) // 30  # 向上取整
            offsets = [i * 30 for i in range(times)]
            print(f"✅ 已设置为按【{total}条】抓取，共需请求 {times} 次")

        print(f"偏移量: {offsets}")

        max_workers = int(workers)
        if max_workers < 1:
            print("❌ 线程数不能小于1，使用默认值 5")
            max_workers = 5
        print(f"使用的最大线程数: {max_workers}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
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

        # 返回数据供外部使用
        return {
            "main_data": dic,
            "download_data": download_results
        }

    except KeyboardInterrupt:
        print("\n\n♦️ 用户已中断程序。")
        exit(0)
    except Exception as e:
        print(f"❌ 发生异常：{e}")
        return None