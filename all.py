import json
from core.crawler import run_crawler

# 执行爬虫获取数据
s = run_crawler(mode=2, num=15882, workers=9999)
main_data = s['main_data']
download_results = s['download_data']

def merge_data(main_data, download_results):
    # 构建 soft_id -> download_info 的映射
    download_map = {}
    for item in download_results:
        if item.get("resp", {}).get("retCode") == 0:
            soft_list = item["resp"].get("soft_list", [])
            for soft in soft_list:
                soft_id = soft["soft_id"]
                download_map[soft_id] = soft

    merged = []
    for data in main_data:
        soft_id = data["s"]
        if soft_id in download_map:
            dl_info = download_map[soft_id]
            # 把 download_info 的字段合并到主数据中
            data.update({
                "soft_id": dl_info.get("soft_id"),
                "os_type": dl_info.get("os_type"),
                "os_bit": dl_info.get("os_bit"),
                "display_name": dl_info.get("display_name"),
                "nick_ver": dl_info.get("nick_ver"),
                "ver_name": dl_info.get("ver_name"),
                "file_size": dl_info.get("file_size"),
                "file_name": dl_info.get("file_name"),
                "publish_date": dl_info.get("publish_date"),
                "download_url": dl_info.get("download_url"),
                "download_https_url": dl_info.get("download_https_url"),
                "Logo48File": dl_info.get("Logo48File")
            })
        merged.append(data)

    return merged


# 合并数据
merged_data = merge_data(main_data, download_results)

# 写入 JSON 文件
with open("data/all.json", "w", encoding="utf-8") as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=4)

print(f"✅ 数据已合并并保存至 data/all.json，共 {len(merged_data)} 条记录。")