
---

## 一、软件管家数据抓取🎉🎉🎉🎉

### 功能说明

- 批量抓取腾讯软件管家API的主列表数据
- 获取并调用接口获取每个软件的详细信息
- 结果分别保存为 `data/data.json` 和 `data/exedata.json`

### 主要脚本🚀
- [`core`](core/)✅
    - [`main.py`](main.py)
        1. 并发抓取主列表（`getSoftList`接口）
        2. 并发POST下载接口（`softwareProxy`接口）
        3. 结果写入本地JSON文件
- [`modules`](modules/)✅
    - [`modules/smartSearch.py`](modules/smartSearch.py)
        1. 内容网页端搜索框，提示词，官方接口
        2. [提示词接口预览]
        `https://luban.m.qq.com/api/public/software-manager/searchcgi?type=smart&callback=_cb&keyword=wei`
    - [`modules/get_index_list.py`](modules/get_index_list.py)✅
        1. 获取pc.qq.com主页list内容函数

    - [`modules/get_download_url.py`](modules/get_download_url.py)✅
        1. 根据sid获取下载直连
        2. [直连接口预览]
        `https://luban.m.qq.com/api/public/software-manager/softwareProxy`
    - [`x.txt`](x.txt)
        1. 接口返回结构样例与参数说明

### 快速开始

1. 安装依赖
    ```sh
    pip install requests -r requirements.txt
    ```

2. 运行主脚本
    ```sh
    python main.py
    ```

3. 结果文件保存到data目录下
    - `data.json`：主列表数据
    - `exedata.json`：每个软件详细信息

---

## 参考

- edge F12

---

如有问题欢迎提交Issue或联系作者。🚀🚀🚀🚀🚀🚀