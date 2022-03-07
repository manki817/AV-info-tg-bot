# -*- coding:utf-8 -*-

import requests, telegram, schedule, time, json
from bs4 import BeautifulSoup

bot = telegram.Bot(token='1223891253:AAHA6ykedHiscyN_M_k20O1QGaAIBDyEM80')


def playno1(former_info):
    url_forbid = 'http://stno1.playno1.com/forbid.htm'
    url = 'http://www.playno1.com/portal.php?mod=list&catid=78'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'stno1.playno1.com',
        'Referer': 'http://stno1.playno1.com/forbid.htm'
    }

    try:
        s = requests.Session()
        s.get(url_forbid)
        # s.get(url)
        requests.cookies.RequestsCookieJar()
        cookie_dict = s.cookies.get_dict()
        cookie_dict.update({'playno1': 'playno1Cookie'})
        r = requests.get(url, headers=headers, cookies=cookie_dict)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        html = r.text

        soup = BeautifulSoup(html, 'html.parser')

        titles = soup.select('h3 a')
        title_text = titles[0].get('title')
        hrefs = soup.select('h3 a')
        title_href = 'http://www.playno1.com/' + hrefs[0].get('href')
        imgs = soup.select('.fire_imgbox img')
        img_url = imgs[0].get('src')
        summarys = soup.select('.fire_p')
        summary_text = summarys[0].get_text()

        playno1_info = {'title': title_text, 'href': title_href, 'img': img_url, 'summary': summary_text}

        if not (former_info == title_href):
            message_text = '<b>PlayNo1</b>\n' + '<a href="' + playno1_info['href'] + '">' + playno1_info[
                'title'] + '</a>' + playno1_info['summary'] + '\n' + playno1_info['img']
            bot.send_message(chat_id='@av_info',
                             text=message_text,
                             parse_mode=telegram.ParseMode.HTML)
        else:
            print('PlayNo1没有新的文章')
        return title_href
    except Exception as e:
        # print('错误类型是',e.__class__.__name__)
        # print('错误明细是',e)
        bot.send_message(chat_id='@av_info_info', text='playno1 error, return former info')
        return former_info


def a383(former_info):
    url = 'https://www.a383.com/api/NewsList?page=1'
    try:
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        html = r.text

        dict_data = json.loads(html)
        # print(dict_data['data'][0])
        title_text = dict_data['data'][0]['title']
        title_href = 'https://www.a383.com/NewsDetail.asp?id=' + str(dict_data['data'][0]['id'])
        title_href_m = 'https://m.a383.com/#/articlecontent?Id=' + str(dict_data['data'][0]['id'])
        img_url = dict_data['data'][0]['frontCover']
        summary_text = dict_data['data'][0]['desc']
        a383_info = {'title': title_text, 'href': title_href, 'img': img_url, 'summary': summary_text,
                     'href_m': title_href_m}

        if not (former_info == title_href):
            message_text = '<b>A383</b>\n' + '<a href="' + a383_info['href'] + '">' + a383_info['title'] + '</a>-PC端\n' \
                           + '<a href="' + a383_info['href_m'] + '">' + a383_info['title'] + '</a>-移动端\n' + a383_info[
                               'summary'] + '\n' + a383_info['img']
            bot.send_message(chat_id='@av_info',
                             text=message_text,
                             parse_mode=telegram.ParseMode.HTML)
        else:
            print('a383没有新的文章')
        return title_href # a383_info
    except:
        bot.send_message(chat_id='@av_info_info', text='a383 error, return former info')
        return former_info



def jkf(former_info):
    url = 'https://www.jkforum.net/forum.php?mod=forumdisplay&fid=535'
    try:
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        html = r.text

        soup = BeautifulSoup(html, 'html.parser')

        titles = soup.select('.xw0 a:nth-child(1)')
        title_text = titles[0].get_text()
        title_href = 'https://www.jkforum.net/' + titles[0].get('href')
        # imgs = soup.select('.z img')
        # img_url = imgs[0].get('src')
        # summarys = soup.select('.block_msg a')
        # summary_text = summarys[0].get_text()

        jkf_info = {'title': title_text, 'href': title_href}

        if not (former_info == title_href):
            # message_text = '<b>JKF捷克論壇</b>\n'+'<a href="'+jkf_info['href']+'">'+jkf_info['title']+'</a>\n'+jkf_info['summary']+'\n'+jkf_info['img']
            message_text = '<b>JKF捷克論壇</b>\n' + '<a href="' + jkf_info['href'] + '">' + jkf_info['title'] + '</a>'
            bot.send_message(chat_id='@av_info',
                             text=message_text,
                             parse_mode=telegram.ParseMode.HTML)
        else:
            print('JKF捷克論壇没有新的文章')
        return title_href # jkf_info
    except:
        bot.send_message(chat_id='@av_info_info', text='jkf error, return former info')
        return former_info


def click_me(former_info):
    url = 'https://api.clickme.net/article/list?key=clickme'
    data = {
        'articleType': 'r18',
        'subtype': 'category',
        'subtypeSlug': 'av',
        'device': '',
        'limit': 1,
        'page': 1
    }
    try:
        r = requests.post(url, data=data)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        html = r.text

        dict_data = json.loads(html)
        title_text = dict_data['data']['items'][0]['title']
        title_href = dict_data['data']['items'][0]['url']
        # img_url = dict_data['data']['items'][0]['thumbnail']
        click_me_info = {'title': title_text, 'href': title_href}

        if not (former_info == title_href):
            message_text = '<b>ClickMe</b>\n' + '<a href="' + click_me_info['href'] + '">' + click_me_info[
                'title'] + '</a>'
            bot.send_message(chat_id='@av_info',
                             text=message_text,
                             parse_mode=telegram.ParseMode.HTML)
        else:
            print('Click Me 没有新的文章')
        return title_href # click_me_info
    except:
        bot.send_message(chat_id='@av_info_info', text='click_me error, return former info')
        return former_info


def jnm(former_info):
    url = 'https://japan-night-concierge.com/category/av/'
    try:
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        html = r.text

        soup = BeautifulSoup(html, 'html.parser')

        titles = soup.select('.heading-secondary a')
        title_text = titles[0].get_text()
        title_href = titles[0].get('href')

        jnm_info = {'title': title_text, 'href': title_href}

        if not (former_info == title_href):
            # message_text = '<b>JNM</b>\n'+'<a href="'+jnm_info['href']+'">'+jnm_info['title']+'</a>\n'+jnm_info['summary']+'\n'+jnm_info['img']
            message_text = '<b>JNM</b>\n' + '<a href="' + jnm_info['href'] + '">' + jnm_info['title'] + '</a>'
            bot.send_message(chat_id='@av_info',
                             text=message_text,
                             parse_mode=telegram.ParseMode.HTML)
        else:
            print('JNM没有新的文章')
        return title_href # jnm_info
    except:
        bot.send_message(chat_id='@av_info_info', text='jnm error, return former info')
        return former_info


def hi_live(former_info):
    # url = 'https://www.hilive.tv/news/list/p1'
    url = 'https://www.hilive.tv/Adultonly/Entry?u=https%253a%252f%252fwww.hilive.tv%252fnews%252flist%252fp1'
    try:
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        html = r.text

        soup = BeautifulSoup(html, 'html.parser')

        titles = soup.select('h3 a')
        title_text = titles[0].get_text()
        title_href = 'https://www.hilive.tv' + titles[0].get('href')

        hi_live_info = {'title': title_text, 'href': title_href}

        if not (former_info == title_href):
            message_text = '<b>HiLive</b>\n' + '<a href="' + hi_live_info['href'] + '">' + hi_live_info[
                'title'] + '</a>'
            bot.send_message(chat_id='@av_info',
                             text=message_text,
                             parse_mode=telegram.ParseMode.HTML)
        else:
            print('HiLive没有新的文章')
        return title_href # hi_live_info
    except:
        bot.send_message(chat_id='@av_info_info', text='hi_live error, return former info')
        return former_info


file = open('temp.txt', 'r')
js = file.read()
dic = json.loads(js)
file.close()
former_info_playno1 = dic['playno1']
# print(former_info_playno1)
former_info_a383 = dic['a383']
former_info_jkf = dic['jkf']
former_info_click_me = dic['click_me']
former_info_jnm = dic['jnm']
former_info_hi_live = dic['hi_live']


def check_and_send():
    global former_info_playno1
    former_info_playno1 = playno1(former_info_playno1)

    global former_info_a383
    former_info_a383 = a383(former_info_a383)

    global former_info_jkf
    former_info_jkf = jkf(former_info_jkf)

    global former_info_click_me
    former_info_click_me = click_me(former_info_click_me)

    global former_info_jnm
    former_info_jnm = jnm(former_info_jnm)

    global former_info_hi_live
    former_info_hi_live = hi_live(former_info_hi_live)
    # print('after:')
    # print(former_info)
    txt = {
        'playno1': former_info_playno1,
        'a383': former_info_a383,
        'jkf': former_info_jkf,
        'click_me': former_info_click_me,
        'jnm': former_info_jnm,
        'hi_live': former_info_hi_live
    }
    str_txt = json.dumps(txt)
    temp_file = open('temp.txt', 'w')
    temp_file.write(str_txt)
    temp_file.close()


schedule.every(10).minutes.do(check_and_send)

while True:
    schedule.run_pending()   # 运行所有可以运行的任务
    time.sleep(1)
