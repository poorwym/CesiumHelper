# URLcollection 使用方法

URLcollection 是一个从 HTML 文件中提取 URL 链接的工具。它主要用于从保存的 HTML 文件中收集并保存所有 URL 链接。

## 使用步骤

### 1. 准备环境

首先，安装所需依赖：

```bash
pip install -r requirements.txt
```

主要依赖是 `beautifulsoup4` 库，用于 HTML 解析。

### 2. 准备 HTML 文件

将需要提取链接的 HTML 文件放入 `html` 目录中。工具会自动处理该目录下的所有 HTML 文件。目前该目录中已有一个示例文件：`Index - Cesium Documentation.html`。

### 3. 运行提取工具

在 URLcollection 目录中运行 Python 脚本：

```bash
python extract_links.py
```

### 4. 查看结果

脚本执行后会生成 `extracted_links.txt` 文件，其中包含从所有 HTML 文件中提取的链接。每个链接占一行。

## 功能说明

- 脚本会自动检查 `html` 目录是否存在
- 处理该目录下的所有 HTML 文件
- 使用 BeautifulSoup 解析 HTML 并提取所有 `<a>` 标签的 href 属性
- 将所有提取到的链接保存到 `extracted_links.txt` 文件中
- 在处理过程中会输出每个文件提取的链接数量以及总链接数量

这个工具特别适合收集网页中的大量链接，比如 API 文档、参考页面等。从现有的 `extracted_links.txt` 文件来看，已经从 Cesium 文档中提取了大量 API 相关链接。
