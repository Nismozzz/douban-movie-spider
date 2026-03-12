# 豆瓣热门电影爬虫

一个简单的Python爬虫项目，用于爬取豆瓣正在热映的电影信息。

## 功能特点

- 爬取豆瓣正在热映的电影列表
- 获取电影的基本信息（标题、评分、导演、演员、海报等）
- 将数据保存为JSON格式
- 添加请求延迟，避免对服务器造成压力

## 环境要求

- Python 3.7+
- requests
- beautifulsoup4
- lxml

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

运行爬虫脚本：

```bash
python douban_spider.py
```

爬取完成后，数据将保存在 `douban_movies.json` 文件中。

## 数据格式

```json
[
  {
    "title": "电影标题",
    "rating": "评分",
    "director": "导演",
    "actors": "主演",
    "poster": "海报链接",
    "detail_url": "详情页链接",
    "crawl_time": "爬取时间"
  }
]
```

## 注意事项

- 请遵守豆瓣的robots.txt协议
- 不要频繁请求，避免给服务器造成压力
- 仅供学习交流使用，请勿用于商业用途

## 许可证

MIT License
