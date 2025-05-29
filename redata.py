from modules.get_index_list import fetch_data
from modules.get_download_url import download
import json

# 获取主数据（例如 offset=0）
main_data = fetch_data(offset=13990)
print(f"主数据条目数: {len(main_data)}")
def get_all_download_info(main_data):
    """
    根据 main_data 中的 soft_id 获取所有下载信息
    """
    sids = [item["s"] for item in main_data if "s" in item]
    download_results = []

    for sid in sids:
        print("开始下载软件 ID:", sid)
        result = download(sid)
        if "error" in result:
            print(f"下载失败: {result['error']}")
        else:
            download_results.append(result)  # 收集所有下载结果

    return download_results

def merge_and_save(fetch_data, download_results, output_file="data/all.json"):
    """
    将 fetch_data 和 download_results 合并，按 soft_id 匹配，输出到 all.json
    """
    # 构建 download_map: soft_id -> download info
    download_map = {}
    for res in download_results:
        if res and "resp" in res and "soft_list" in res["resp"]:
            for soft_info in res["resp"]["soft_list"]:
                soft_id = soft_info["soft_id"]
                download_map[soft_id] = soft_info

    # 合并主数据与下载信息
    merged_list = []
    for item in fetch_data:
        if "s" not in item:
            continue  # 跳过没有 soft_id 的条目
        soft_id = item["s"]
        dl_info = download_map.get(soft_id, None)

        merged_item = {
            **item,
            "download_info": dl_info
        }

        merged_list.append(merged_item)

    # 写入 JSON 文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_list, f, ensure_ascii=False, indent=2)

    print(f"✅ 数据已写入 {output_file}")

# 执行下载并合并
download_results = get_all_download_info(main_data)
merge_and_save(main_data, download_results)