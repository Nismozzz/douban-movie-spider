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
from datetime import datetime


class DoubanMovieSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = 'https://movie.douban.com'
        self.movies = []

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
            return

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=2)
            print(f"\n数据已保存到 {filename}")
            print(f"共保存 {len(self.movies)} 部电影信息")
        except Exception as e:
            print(f"保存文件失败: {e}")

    def run(self):
        """运行爬虫"""
        print("=" * 50)
        print("豆瓣热门电影爬虫启动")
        print("=" * 50)

        self.get_hot_movies()
        self.save_to_json()

        print("=" * 50)
        print("爬虫运行完成")
        print("=" * 50)


if __name__ == '__main__':
    spider = DoubanMovieSpider()
    spider.run()
