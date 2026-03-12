#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣热门电影爬虫
爬取豆瓣正在热映的电影信息并保存为JSON格式
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv


class DoubanMovieSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = 'https://movie.douban.com'
        self.movies = []
        self.email_config = self.load_email_config()

    def load_email_config(self):
        """加载邮箱配置"""
        load_dotenv()
        return {
            'sender': os.getenv('SENDER_EMAIL'),
            'password': os.getenv('EMAIL_PASSWORD'),
            'receiver': os.getenv('RECEIVER_EMAIL'),
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.qq.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', 465))
        }

    def get_hot_movies(self):
        """获取正在热映的电影列表"""
        url = f'{self.base_url}/cinema/nowplaying/beijing/'

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')
            movie_list = soup.find('ul', class_='lists')

            if not movie_list:
                print("未找到电影列表")
                return

            movies = movie_list.find_all('li', class_='list-item')
            print(f"找到 {len(movies)} 部热门电影")

            for movie in movies:
                movie_info = self.parse_movie(movie)
                if movie_info:
                    self.movies.append(movie_info)
                    print(f"已爬取: {movie_info['title']}")
                time.sleep(1)  # 添加延迟，避免请求过快

        except requests.RequestException as e:
            print(f"请求失败: {e}")

    def parse_movie(self, movie_element):
        """解析单个电影信息"""
        try:
            # 电影标题
            title = movie_element.get('data-title', '未知')

            # 电影评分
            rating = movie_element.get('data-score', '暂无评分')

            # 电影导演
            director = movie_element.get('data-director', '未知')

            # 电影演员
            actors = movie_element.get('data-actors', '未知')

            # 电影海报
            img_tag = movie_element.find('img')
            poster = img_tag.get('src', '') if img_tag else ''

            # 电影详情链接
            movie_id = movie_element.get('data-subject', '')
            detail_url = f'{self.base_url}/subject/{movie_id}/' if movie_id else ''

            return {
                'title': title,
                'rating': rating,
                'director': director,
                'actors': actors,
                'poster': poster,
                'detail_url': detail_url,
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        except Exception as e:
            print(f"解析电影信息失败: {e}")
            return None

    def save_to_json(self, filename='douban_movies.json'):
        """保存数据到JSON文件"""
        if not self.movies:
            print("没有数据可保存")
            return False

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=2)
            print(f"\n数据已保存到 {filename}")
            print(f"共保存 {len(self.movies)} 部电影信息")
            return True
        except Exception as e:
            print(f"保存文件失败: {e}")
            return False

    def send_email(self, filename='douban_movies.json'):
        """发送邮件附件"""
        if not all(self.email_config.values()):
            print("\n邮箱配置不完整，跳过邮件发送")
            print("请创建.env文件并配置邮箱信息（参考.env.example）")
            return False

        try:
            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender']
            msg['To'] = self.email_config['receiver']
            msg['Subject'] = f"豆瓣热门电影数据 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

            # 邮件正文
            body = f"""
            您好！

            这是豆瓣热门电影爬虫的自动邮件。

            爬取时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            电影数量：{len(self.movies)} 部

            详细数据请查看附件中的JSON文件。

            ---
            此邮件由豆瓣电影爬虫自动发送
            """
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 添加附件
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    attachment = MIMEApplication(f.read(), _subtype='json')
                    attachment.add_header('Content-Disposition', 'attachment',
                                        filename=filename)
                    msg.attach(attachment)

            # 发送邮件
            print("\n正在发送邮件...")
            # 创建SSL上下文，降低安全级别以兼容QQ邮箱
            context = ssl.create_default_context()
            context.set_ciphers('DEFAULT@SECLEVEL=1')

            with smtplib.SMTP_SSL(self.email_config['smtp_server'],
                                 self.email_config['smtp_port'],
                                 context=context) as server:
                server.login(self.email_config['sender'],
                           self.email_config['password'])
                server.send_message(msg)

            print(f"邮件已成功发送到 {self.email_config['receiver']}")
            return True

        except Exception as e:
            print(f"邮件发送失败: {e}")
            return False

    def run(self):
        """运行爬虫"""
        print("=" * 50)
        print("豆瓣热门电影爬虫启动")
        print("=" * 50)

        self.get_hot_movies()

        if self.save_to_json():
            self.send_email()

        print("=" * 50)
        print("爬虫运行完成")
        print("=" * 50)


if __name__ == '__main__':
    spider = DoubanMovieSpider()
    spider.run()
