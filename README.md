
---

## 一、软件管家数据抓取

### 功能说明

- 批量抓取腾讯软件管家开放API的主列表数据
- 获取并调用接口获取每个软件的详细信息
- 结果分别保存为 `data/data.json` 和 `data/exedata.json`

### 主要脚本

- [`main.py`](main.py)
    - 并发抓取主列表（`getSoftList`接口）
    - 并发POST下载接口（`softwareProxy`接口）
    - 结果写入本地JSON文件

- [`godonload.py`](godonload.py)
    - 单个软件POST接口测试

- [`def/smartSearch.py`](def/smartSearch.py)
    - 智能搜索接口测试

- [`x.txt`](x.txt)
    - 接口返回结构样例与参数说明

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

- 腾讯软件管家API接口分析
- pygame官方文档

---

如有问题欢迎提交Issue或联系作者。