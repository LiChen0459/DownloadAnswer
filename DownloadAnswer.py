import requests
import json
import time
import re
from os import mkdir


def download_img(img_url, file):
    print('Start download: ', img_url)
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"} # 设置http header，视情况加需要的条目，这里的token是用来鉴权的一种方式
    r = requests.get(img_url, headers=header, stream=True)
    if r.status_code == 200:
        open(file, 'wb').write(r.content)
        print(img_url, 'File download Success!!')
    del r


def download_question(url):
    print('开始获取图片地址......\n')
    ha = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 9; zh-CN; Redmi 6 Pro Build/PKQ1.180917.001) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Quark/5.3.8.193 Mobile Safari/537.36'}

    html = requests.get(url, headers=ha)
    html.encoding = 'utf-8'

    urls = []
    process = html.text.replace('\/', '/')
    n = re.findall(r"//*/(.+?).jpg", process)
    for i in range(len(n)):
        azz = n[i]
        urls.append("http://" + azz + '.jpg')
    del html
    del process
    del ha
    del n
    print('共', len(urls), '张图片')
    for i in range(len(urls)):
        print(urls[i])
    print('\n图片地址获取结束')
    name = input('请输入文件夹名称: ')
    mkdir(name)
    print('\n\n开始下载......\n\n')
    for i in range(len(urls)):
        download_img(urls[i], '.\\' + name + '\\' + str(i + 1) + '.jpg')


def go_get(name, others, start = 0):
    global x
    url = 'https://quark.sm.cn/api/rest'
    data = {
        "method": "sc.jiaofu_ziliao",
        "req_app": "true",
        "q": name,
        "start": start,
        "req_period": "k12",
        "_": time.time(),
        "callback": ""
    }
    data = dict(others, **data)
    print(data)
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; U; Android 9; zh-CN; Redmi 6 Pro Build/PKQ1.180917.001) AppleWebKit/537.36 ("
                      "KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Quark/5.3.8.193 Mobile Safari/537.36",
        "accept": "*/*",
        "referer": "https://quark.sm.cn/api/rest?uc_param_str=dsdnutlbgpmiosntnnfrpfbivepcsvpr&method=education.home&q=&entry=camera&uc_biz_str=OPT%3AS_BAR_BG_COLOR%40FFFFFF"
    }
    req = requests.get(url, params=data, headers=headers)

    ret = json.loads(req.text)["data"]["item"]
    print('-' * 90)
    for x in range(len(ret)):
        print('[ %i ] %s' % (x, ret[x]["title"]))
    print('-' * 90)
    print('[ %i ] 下一页   [ %i ] 上一页   当前是第 %i 页' % (x + 1, x + 2, (start / 15) + 1))
    command = input('请做出您的选择 > ')
    if command != '' and command.isdigit():
        if int(command) != (x + 1) and int(command) != (x + 2):
            print(ret[int(command)]['detail_url'])
            download_question(ret[int(command)]['detail_url'])
        else:
            if int(command) == (x + 1):
                go_get(name, others, start + 15)
            else:
                go_get(name, others, start - 15)
    else:
        print('您的输入有误 (: ')
        input()


def get_more():
    url = 'https://quark.sm.cn/api/rest?method=sc.jiaofu_ziliao&req_app=true'
    r = requests.get(url)
    ret = json.loads(r.text)["data"]['filter']
    grade = ret["grade"]["items"]
    subject = ret["subject"]["items"]
    year = ret["year"]["items"]
    semester = ret["semester"]["items"]
    version = ret["version"]["items"]
    # print(grade)
    # print(subject)
    # print(year)
    # print(semester)
    return grade, subject, year, semester, version


if __name__ == '__main__':
    print("---------------------------------------------")
    print("| |     | | /  ___| | | | | | ____| |  \ | | ")
    print("| |     | | | |     | |_| | | |__   |   \| | ")
    print("| |     | | | |     |  _  | |  __|  | |\   | ")
    print("| |___  | | | |___  | | | | | |___  | | \  | ")
    print("|_____| |_| \_____| |_| |_| |_____| |_|  \_| ")
    print("---------------------------------------------")
    print('答案助手 1.0')
    print('Made by LiChen')
    print('Source Code : https://github.com/LiChen0459/DownloadAnswer')
    answer_name = input('您要搜索什么答案: ')
    advanced = {
        "grade": '',
        "subject": '',
        "year": '',
        "semester": '',
        "version": ''
    }
    print()
    if input('是否启用高级搜索 \n[ 1 ] 启用   [ 2 ] 关闭  ') == '1':
        print()
        more_Options = get_more()
        for i in range(len(get_more())):
            for j in range(len(more_Options[i])):
                print('[ %i ] %s' % (j, more_Options[i][j]))
            option = input('请选择 > ')
            print()
            if option != '' and option.isdigit():
                try:
                    advanced[list(advanced.keys())[i]] = more_Options[i][int(option)]
                except Exception:
                    pass

    print(advanced)
    go_get(answer_name, advanced)
    print('感谢使用LiChen开发的网页')