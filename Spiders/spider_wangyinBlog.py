#!/usr/bin/env python
# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import os
import urllib
from urllib import parse
from urllib import request

url = 'http://YinWang.org'

def main():
    res = requests.get(url)

    if not res:
        print('Download failed, please check!')
        return

    print('Begin task...')

    soup = BeautifulSoup(res.content, 'lxml')

    li_of_titles = soup.find_all('li', class_='list-group-item title')

    # <li class="list-group-item title">
    # <a href="/blog-cn/2017/08/16/weibo">微博</a>
    # </li>

    blog_list = list()

    for item in li_of_titles:
        a = item.find('a')

        # 获取博文标题
        blog_title = a.get_text()
        # 获取文章链接
        herf = url + a.get('href')

        blog = {'title':blog_title, 'url':herf}
        # print (blog)
        # blog_list.append(blog)
        save_name = blog_title + '.md'

        # 如果之前下载过了，就不再下载
        if not os.path.exists('yinwang/' + save_name):
            download_blog(blog)


def download_blog(blog_info):
    blog_url = blog_info.get('url')
    blog_title = blog_info.get('title')

    if not blog_url:
        print('download《' + blog_title + '》fail!\n')
        print('url is error, please check!\n')
        return


    blog_req = requests.get(blog_url)
    blog_html = BeautifulSoup(blog_req.content, 'lxml')

    # print (blog_html)
    # p_tags = blog_html.find_all('p')
    # print(p_tags)

    try:
        print(".....")
        all_tags = blog_html.find('div',attrs={'style': 'padding: 2% 8% 5% 8%; border: 1px solid LightGrey;'}).descendants
    except AttributeError:
        all_tags = blog_html.find('body').descendants

    # all_tags = main_div.descendants
    # dir_path = 'yinwang/'+blog_title
    dir_path = 'yinwang'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for tag in all_tags:
        text = ''

        if tag.name == 'p':
            text = tag.get_text()

        elif tag.name == 'a':
            # print('a-tag')
            link_title = tag.get_text()
            # print (link_title)
            link_url = tag.get('href')
            # print (link_url)
            text = '[' + link_title + '](' + link_url + ')'

        elif tag.name == 'img':
            img_src = tag.get('src')
            # img_name = parse.urlparse(img_src).path.split('/')[-1];
            # download_img(url=img_src,path='yinwang/'+blog_title+'/'+img_name)
            text = '![image](' + img_src + ')'


        text += '\n'
        # article_path = 'yinwang/'+ blog_title + '/' + blog_title + '.md'
        article_path = 'yinwang/' + blog_title + '.md'
        f = open(article_path, 'a+')

        try:
            f.write(text)
        finally:
            f.close()

    print('dwoload the blog : ' + blog_title)

def download_img(url,path):
    request.urlretrieve(url,path)


if __name__ == '__main__':
    main()
