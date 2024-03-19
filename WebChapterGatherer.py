import requests
from bs4 import BeautifulSoup
import time
import json

# 定义爬取的链接
url_root = 'https://m.lwxiaoshuo.org'   # 以此网站为例
url_book = '/shu/12345'
index_num = 15

# 定义保存进度的文件
progress_file = 'progress.json'
# 定义保存结果的文件
output_file = 'chapters_content.txt'

# 尝试加载上次的进度
try:
    with open(progress_file, 'r', encoding='utf-8') as f:
        progress = json.load(f)
    starting_url_index = progress['last_url_index']
    starting_chapter_index = progress['last_chapter_index']
    print(f"继续上次进度：URL索引 {starting_url_index}，章节索引 {starting_chapter_index}")
except FileNotFoundError:
    # 如果没有找到进度文件，从头开始
    starting_url_index = 0
    starting_chapter_index = 0
    print("从头开始")

# 定义爬取的链接列表
# urls = [f'https://m.lwxiaoshuo.org/shu/12345_{i}/' for i in range(1, 15)] 以此网站为例
urls = [url_root + url_book +'_{i}/' for i in range(1, index_num)]
total_urls = len(urls)
total_chapters = 0  # 将在每个URL处理后更新

# 使用with语句确保文件正确关闭
with open(output_file, 'a', encoding='utf-8') as file:
    # 遍历所有链接，从保存的进度开始
    for url_index, url in enumerate(urls[starting_url_index:], start=starting_url_index):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        chapter_links = soup.find_all('li')
        if url_index == starting_url_index:  # 如果是从中间开始，调整总章节数
            total_chapters = len(chapter_links) - starting_chapter_index
        else:
            total_chapters = len(chapter_links)

        print(f"正在处理链接 {url_index+1}/{total_urls}，包含章节数：{total_chapters}")

        for chapter_index, chapter in enumerate(chapter_links, start=0):
            if chapter_index < starting_chapter_index and url_index == starting_url_index:
                continue  # 跳过已完成的章节
            a_tag = chapter.find('a')
            if a_tag and 'href' in a_tag.attrs:
                chapter_url = url_root + a_tag['href']
                print(f"正在爬取章节 {chapter_index+1}/{total_chapters}...")
                chapter_response = requests.get(chapter_url)
                chapter_soup = BeautifulSoup(chapter_response.content, 'html.parser')
                content_div = chapter_soup.find('div', class_='content')
                if content_div:
                    file.write(content_div.text.strip())
                    file.write('\n\n')  # 章节之间添加空行

                # 保存进度
                with open(progress_file, 'w', encoding='utf-8') as f:
                    json.dump({'last_url_index': url_index, 'last_chapter_index': chapter_index + 1}, f)
                
                # 避免请求过于频繁
                time.sleep(0.5)
        
        starting_chapter_index = 0  # 重置章节索引，为处理下一个URL做准备
