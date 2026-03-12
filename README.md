# 豆瓣热门电影爬虫

一个简单的Python爬虫项目，用于爬取豆瓣正在热映的电影信息。

## 功能特点

- 爬取豆瓣正在热映的电影列表
- 获取电影的基本信息（标题、评分、导演、演员、海报等）
- 将数据保存为JSON格式
- 自动发送JSON文件到指定邮箱
- 添加请求延迟，避免对服务器造成压力

## 环境要求

- Python 3.7+
- requests
- beautifulsoup4
- lxml
- python-dotenv

## 安装依赖

```bash
pip install -r requirements.txt
```

## 邮箱配置

如果需要使用邮件发送功能，请按以下步骤配置：

1. 复制 `.env.example` 文件并重命名为 `.env`
2. 编辑 `.env` 文件，填写你的邮箱信息：

```
SENDER_EMAIL=your_qq_email@qq.com
EMAIL_PASSWORD=your_authorization_code
RECEIVER_EMAIL=receiver@example.com
```

**重要提示：**
- `EMAIL_PASSWORD` QQ邮箱的授权码
- `.env` 文件已添加到 `.gitignore`，不会被提交到Git仓库

如果不配置邮箱，爬虫仍会正常运行，只是不会发送邮件。

## 使用方法

运行爬虫脚本即可

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

## 许可证

MIT License
