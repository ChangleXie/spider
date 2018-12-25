# -*- coding: utf-8 -*-
from threading import Thread, Lock, Timer
from time import time, sleep, strftime, localtime
from requests import Session, Request
from bs4 import BeautifulSoup
from tkinter import Tk, Label, Button, Text, END, RAISED, NW, Toplevel, Frame, TclError, messagebox
from re import compile, findall
from os import mkdir
from os.path import exists
from xlsxwriter import Workbook
from random import random
from sys import version_info
from hashlib import sha1, sha256
from hmac import new
from urllib import parse, request
from json import loads
from binascii import b2a_base64
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import warnings
import logging
from PIL import Image, ImageTk
from io import BytesIO

warnings.filterwarnings("ignore")

secretId = "AKIDU3VmspxKo6FF8qwvaaTBhcs44sK06iME"
secretKey = "udDdrMmAa2a8hIm9JH3cKya3ZzMi8Vhl"


def initlogging(logfilename):
    logging.basicConfig(
                    level=logging.DEBUG,
                    format='%(asctime)s-%(levelname)s-%(message)s',
                    datefmt='%y-%m-%d %H:%M',
                    filename=logfilename,
                    filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


initlogging('logging.log')


def sign(secretkey, signstr, signmethod):
    if version_info[0] > 2:
        signstr = signstr.encode("utf-8")
        secretkey = secretkey.encode("utf-8")
    if signmethod == 'HmacSHA256':
        digestmod = sha256
    elif signmethod == 'HmacSHA1':
        digestmod = sha1
    hashed = new(secretkey, signstr, digestmod)
    base64 = b2a_base64(hashed.digest())[:-1]
    if version_info[0] > 2:
        base64 = base64.decode()
    return base64


def dict_to_str(dictdata):
    temp_list = []
    for evekey, evevalue in dictdata.items():
        temp_list.append(str(evekey) + "=" + str(evevalue))
    return "&".join(temp_list)


def translate(secretid, secretkey, source_text):
    timedata = str(int(time()))
    noncedata = int(random() * 10000)
    actiondata = "TextTranslate"
    uridata = "tmt.tencentcloudapi.com"
    signmethod= "HmacSHA256"
    request_method = "GET"
    region_data = "ap-hongkong"
    version_data = '2018-03-21'
    sign_dict_data = {
        'Action': actiondata,
        'Nonce': noncedata,
        'ProjectId': 0,
        'Region': region_data,
        'SecretId': secretid,
        'SignatureMethod': signmethod,
        'Source': "en",
        'SourceText': source_text,
        'Target': "zh",
        'Timestamp': int(timedata),
        'Version': version_data,
    }

    request_str = "%s%s%s%s%s" % (request_method, uridata, "/", "?", dict_to_str(sign_dict_data))
    sign_data = parse.quote(sign(secretkey, request_str, signmethod))
    action_args = sign_dict_data
    action_args["Signature"] = sign_data
    request_url = "https://%s/?" % uridata
    request_url_with_args = request_url + dict_to_str(action_args)
    response_data = request.urlopen(request_url_with_args).read().decode("utf-8")
    return loads(response_data)['Response']['TargetText']


def urlread(url):

    s = Session()
    # url = 'http://' + url[8:]
    # proxy = {'http': 'http://222.76.204.110:808'}
    request = Request('GET', url, headers=headers, cookies=cookie)
    prepared_request = s.prepare_request(request)
    settings = s.merge_environment_settings(prepared_request.url, None, None, None, None)
    response = s.send(prepared_request, **settings).text
    soup = BeautifulSoup(response, 'lxml')
    # logging.info(soup)
    return soup


def get_reviews(link, arr=[]):
    rev_soup = urlread(link)
    page = rev_soup.find_all(class_='page-button')
    if not page:
        return get_last_reviews(link, [])
    last_page = rev_soup.find(class_='a-selected page-button')
    reviewers_info = rev_soup.find_all(class_='a-section celwidget')
    next_page = rev_soup.find('li', class_='a-last')

    if isinstance(next_page.a, type(None)):
        return get_last_reviews(ama_url + last_page.a['href'], arr)
    logging.info('Page %s\'s review(s)' % last_page.get_text())
    for reviewer in reviewers_info:
        rev_id = reviewer.find(class_='a-profile-name').get_text()
        rev_time = reviewer.find(class_='a-size-base a-color-secondary review-date').get_text()
        style = reviewer.find(class_='a-size-mini a-link-normal a-color-secondary')
        if style is not None:
            rev_style = reviewer.find(class_='a-size-mini a-link-normal a-color-secondary').get_text() or 'None'
        else:
            rev_style = 'None'
        rev_content = reviewer.find(class_='a-size-base review-text').get_text()
        rev_rate = reviewer.find(class_='a-icon-alt').get_text()
        rev_title = reviewer.find(class_='a-size-base a-link-normal review-title a-color-base a-text-bold').get_text()

        reviewer_info = {'id': rev_id,
                         'time': rev_time,
                         'style': rev_style,
                         'content': rev_content,
                         'rate': rev_rate,
                         'title': rev_title}
        if reviewer_info not in arr:
            arr.append(reviewer_info)

    return get_reviews(ama_url + next_page.a['href'], arr)


def get_last_reviews(link, arr):
    rev_soup = urlread(link)
    reviewers_info = rev_soup.find_all(class_='a-section celwidget')
    logging.info('Last page\'s review(s)')
    for reviewer in reviewers_info:
        rev_id = reviewer.find(class_='a-profile-name').get_text()
        rev_time = reviewer.find(class_='a-size-base a-color-secondary review-date').get_text()
        style = reviewer.find(class_='a-size-mini a-link-normal a-color-secondary')
        if style is not None:
            rev_style = reviewer.find(class_='a-size-mini a-link-normal a-color-secondary').get_text() or 'None'
        else:
            rev_style = 'None'
        rev_content = reviewer.find(class_='a-size-base review-text').get_text()
        rev_rate = reviewer.find(class_='a-icon-alt').get_text()
        rev_title = reviewer.find(class_='a-size-base a-link-normal review-title a-color-base a-text-bold').get_text()
        reviewer_info = {'id': rev_id,
                         'time': rev_time,
                         'style': rev_style,
                         'content': rev_content,
                         'rate': rev_rate,
                         'title': rev_title}
        if reviewer_info not in arr:
            arr.append(reviewer_info)

    return arr


def ship_weight(dic, sw):
    reg = r'([\d\.]+ )(pounds|ounces)'
    pattern = compile(reg)
    res2 = findall(pattern, sw)
    weight = ''
    if res2:
        for k in res2[0]:
            weight += k
    if weight:
        dic['Shipping Weight'] = weight
    else:
        dic['Shipping Weight'] = 'Not Found'


def get_saler(dic, soup):
    saler = soup.find('a', id='bylineInfo').get_text()
    # logging.info(saler)
    dic['Saler'] = saler


def get_price(dic, soup):
    price = soup.find(id='priceblock_ourprice')
    if price:
        dic['Price'] = price.get_text()
    else:
        dic['Price'] = '$0'


def init_cencor_word():
    if not exists('cencor words.txt'):
        with open('cencor words.txt', 'w') as file:
            file.write('''and,to,the,for,of,is,your,&,are,x,on,or,that,in,\
from,you,any,a,no,which,it,when,can,-,with,i,ii,iii,vi,needs,\
us,.,we,–,not,this,will,be,all,so,also,up,our,them,have,an,--,\
by,they,wa,but,my,if,had,was,one,would,just,very,it’s,some,since\
,many,wasnt,were,at,other,out,into,do,like,has,after''')


def freq_word(arr):
    res = ''
    for i in [shit for shit in arr]:
        for j in i:
            res += str(j)
    puncs = [',', ':', '★', '(', ')', '/', '@', '=', ]
    for punc in puncs:
        res = res.replace(punc, ' ')
    freq = {}
    for word in res.lower().split():
        if word not in freq:
            freq[word] = 1
        else:
            freq[word] += 1
    with open('cencor words.txt', 'r') as f:
        words = f.read().split(',')

    for word in freq.keys():
        if word[-1] == 's':
            if word[:-1] in freq.keys():
                freq[word[:-1]] += freq[word]
                words.append(word)

        if word[-3:] == 'ies':
            if word[:-3]+'y' in freq.keys():
                freq[word[:-3]+'y'] += freq[word]
                words.append(word)

        if len(word) == 1:
            words.append(words)

    for word in words:
        if str(word) in freq:
            freq.pop(word)

    res = sorted(freq.items(), key=lambda item: item[1], reverse=True)
    res_dic = {key: value for (key, value) in res}

    return res_dic


def format_words(book, ws, i, j, sequences, fw):

    def ainb(a, b):
        tails = [')', '(', ',', '\'', '"', '.', '!', '?']
        for i in tails:
            a = a.replace(i, '')
        if a.lower() == b or a.lower() == b+'s' or a[:-3].lower()+'y' == b:
            return True
        else:
            return False

    red = book.add_format({'color': 'red',
                           'bold': 1,
                           'font_name': 'Times New Roman'
                           })
    green = book.add_format({'color': 'green',
                             'bold': 1,
                             'font_name': 'Times New Roman'
                             })
    blue = book.add_format({'color': 'blue',
                            'bold': 1,
                            'font_name': 'Times New Roman'
                            })
    orange = book.add_format({'color': 'orange',
                              'bold': 1,
                              'font_name': 'Times New Roman'
                              })
    normal = book.add_format({'font_name': 'Times New Roman'})
    wraps = book.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'font_name': 'Times New Roman'
    })
    wraps.set_text_wrap()
    format_pairs = []
    count = 0
    for word in sequences.split():
        if ainb(word, fw[0][0]):
            format_pairs.extend((red, str(word+' ')))
            count += 1
        elif ainb(word, fw[1][0]):
            format_pairs.extend((green, str(word+' ')))
            count += 1
        elif ainb(word, fw[2][0]):
            format_pairs.extend((orange, str(word+' ')))
            count += 1
        elif ainb(word, fw[3][0]):
            format_pairs.extend((blue, str(word+' ')))
            count += 1
        else:
            format_pairs.extend((normal, str(word+' ')))
    if count >= 1:
        ws.write_rich_string(i, j, *format_pairs, wraps)
    else:
        ws.write(i, j, sequences, wraps)


# 运输方式
def merchant_info(dic, soup):
    deliver_way = soup.find(id='merchant-info')
    if deliver_way:
        ship_way = deliver_way.get_text().strip()
        if ship_way == '':
            fb_what = 'Unknown (All Sold Out)'
        else:
            reg = r'from and sold by (.*)'
            pattern = compile(reg)
            res = findall(pattern, ship_way[:-1])
            if not res:
                fb_what = 'FBA'
            elif 'Amazon' in res[0]:
                fb_what = 'AMZ'
            else:
                fb_what = 'FBM'
    dic['Delivery Way'] = fb_what


# 评论数和评分
def get_review_qty(dic):
    cr_name = 'Customer Reviews' if 'Customer Reviews' in dic else 'Average Customer Review'
    cr = dic[cr_name]
    reg = r'([,\d]+ customer reviews?)'
    res = findall(reg, cr)
    reg2 = r'([\.\d]+ out of 5 stars)'
    res2 = findall(reg2, cr)
    if res:
        dic['Customer Reviews'] = res[0]
        dic['Review Rate'] = res2[0]
    else:
        dic['Customer Reviews'] = '0 customer reviews'
        dic['Review Rate'] = '0.0 out of 5 stars'
    if 'Average Customer Review' in dic:
        dic.pop('Average Customer Review')


def get_pic(dic, soup):
    pic = soup.find('div', id='imgTagWrapperId').img['data-a-dynamic-image']
    pic = loads(pic)
    dic['Picture'] = sorted(pic.items(), key=lambda d: d[1]).pop()[0]


def get_all_stars(soup):
    one_star_link = soup.find('a', class_='a-size-base a-link-normal 1star')
    two_star_link = soup.find('a', class_='a-size-base a-link-normal 2star')
    three_star_link = soup.find('a', class_='a-size-base a-link-normal 3star')
    four_star_link = soup.find('a', class_='a-size-base a-link-normal 4star')
    five_star_link = soup.find('a', class_='a-size-base a-link-normal 5star')
    a = [one_star_link, two_star_link, three_star_link, four_star_link, five_star_link]
    return a


def star_percent(a):
    rate_dic = {}
    for i in range(5):
        if a[i]:
            rate = a[i]['aria-label'][:6]
            percentage = a[i]['aria-label'][6:].replace('(', '').replace(')', '')
        else:
            rate = '%s star' % str(i+1)
            percentage = '0%'
        rate_dic[rate] = percentage
    #logging.info(rate_dic)
    return rate_dic


def get_rev(dic, soup):
    totle_reviews_info = []
    arr = []
    see_all_reviews = soup.find(class_='a-link-emphasis a-text-bold')
    if see_all_reviews:
        soup2 = urlread(ama_url+see_all_reviews['href'])
        all_cratical_reviews = soup2.find('a', {'data-reftag': 'cm_cr_arp_d_viewpnt_rgt'})

        if all_cratical_reviews:
            dic['Reviews_url'] = ama_url + all_cratical_reviews['href']
        else:
            dic['Reviews_url'] = ama_url+see_all_reviews['href']
        if 'Reviews_url' in dic:
            sort_reviews_info = []
            reviews_info = get_reviews(dic['Reviews_url'], arr=[])
            for item in reviews_info:
                if float(item['rate'][:-15]) <= 3.0:
                    sort_reviews_info.append(item)
            totle_reviews_info.append(sort_reviews_info)

    r = 0
    if totle_reviews_info:
        for item in totle_reviews_info:
            for peace in item:
                peace['row_num'] = r
                r += 1
                arr.append(peace)
        dic['Reviews info'] = arr
    else:
        dic['Reviews info'] = totle_reviews_info


def inch_to_cm(size):
    x, y, z = '0', '0', '0'
    if size != '':
        if 'inches' in size:
            reg = r'([\d\.]+) x ([\d\.]+) x ([\d\.]+)'
            pattern = compile(reg)
            x, y, z = findall(pattern, size)[0]
            x, y, z = sorted([float(x)*2.54, float(y)*2.54, float(z)*2.54], reverse=True)

        elif 'cm' in size:
            return size
    res = '%.2f x %.2f x %.2f cm' % (float(x), float(y), float(z))
    return res


def pound_to_kg(weight):
    if weight:
        reg = r'([\d\.]+)'
        pattern = compile(reg)
        if 'pounds' in weight:
            return '%.2f kg' % (float(findall(pattern, weight)[0]) * 0.45359237)
        elif 'ounces' in weight:
            return '%.2f kg' % (float(findall(pattern, weight)[0]) * 0.0283495231)
        elif 'Kg' or 'g' in weight:
            return weight
        else:
            return 'Something Wrong'


def translate_format(lst):
    res = translate(secretId, secretKey, lst.lower().encode('ascii', 'ignore'))
    rep_list = ['B', '‘', '“', '”', '’', 'b']
    for rep in rep_list:
        res = res.replace(rep, '')
    return res


def excel_writer(arr):
    book_name = 'Products Survey%s.xlsx' % strftime('%Y%m%d%H%m%S', localtime())
    sheet_name = 'Product Information'
    review_detail_name = 'Review Detail'
    wb = Workbook(book_name, options={'strings_to_urls': 0})
    ws = wb.add_worksheet(sheet_name)
    ws2 = wb.add_worksheet(review_detail_name)
    ncol = len(pro_infos)
    style = wb.add_format({'font_name': 'Times New Roman',
                           'align': 'center',
                           'valign': 'vcenter',
                           'border': 1,
                           })
    red = wb.add_format({'color': 'red',
                         'bold': 1,
                         'align': 'center',
                         'valign': 'vcenter',
                         'border': 1,
                         'font_name': 'Times New Roman'
                         })
    green = wb.add_format({'color': 'green',
                           'bold': 1,
                           'align': 'center',
                           'valign': 'vcenter',
                           'border': 1,
                           'font_name': 'Times New Roman'
                           })
    blue = wb.add_format({'color': 'blue',
                          'bold': 1,
                          'align': 'center',
                          'valign': 'vcenter',
                          'border': 1,
                          'font_name': 'Times New Roman'
                          })
    orange = wb.add_format({'color': 'orange',
                            'bold': 1,
                            'align': 'center',
                            'valign': 'vcenter',
                            'border': 1,
                            'font_name': 'Times New Roman'
                            })
    style_arr = [red, green, orange, blue]
    style_arr.extend([style_arr] * 16)

    style.set_text_wrap()

    ws.set_column(1, 21, 20)
    ws.set_column(0, 0, 10)
    row_high = [(0, 20), (1, 120), (2, 50), (3, 20), (4, 20),
                (5, 20), (6, 20), (7, 20), (8, 20), (9, 20),
                (10, 120), (11, 20), (12, 20), (13, 20), (14, 120)]
    for item in row_high:
        ws.set_row(item[0], item[1])

    first_col = ['产品信息', '产品图片', '类目', '尺寸', '尺寸（cm）',
                 '重量', '重量（kg）', '卖家', '发货方式', '评论数',
                 '评分', '售价', '上架日期', '销量', '销量趋势']
    for j in range(len(first_col)):
        ws.write(j, 0, first_col[j], style)

    for j in range(20):
        ws.write(0, j + 1, j + 1, style)

    for j in range(1, 602):
        ws2.set_row(j + 1, 23)

    ws2.merge_range(1, 0, 6, 0, '产品图片', style)
    nn = 7
    for j in range(102):
        ws2.merge_range(5 * j + nn, 0, 5 * j + nn+1, 0, '标题', style)
        ws2.write(5 * j + nn+2, 0, '评分', style)
        ws2.write(5 * j + nn+3, 0, '款式', style)
        ws2.write(5 * j + nn+4, 0, '评论时间', style)

    ws2.set_column(1, 3*ncol, 20)
    ws2.set_column(0, 0, 10)

    for j in range(ncol):
        ws2.merge_range(0, 3 * j + 1, 0, 3 * j + 3, j + 1, style)
        ws2.merge_range(1, 3 * j + 1, 6, 3 * j + 3, '', style)

    for I in range(ncol):
        try:
            url = pro_infos[I][1]['Url']
            col_num = 1
            asin = pro_infos[I][1]['ASIN']
            pic_link = pro_infos[I][1]['Picture']
            get_img(pic_link, asin)
            rank = pro_infos[I][1]['Best Sellers Rank']
            size = pro_infos[I][1]['Package Dimensions']
            weight = pro_infos[I][1]['Shipping Weight']
            cm_size = pro_infos[I][1]['Package Dimensions(cm)']
            kg_weight = pro_infos[I][1]['Shipping Weight(kg)']
            price = pro_infos[I][1]['Price']
            review_num = pro_infos[I][1]['Customer Reviews']
            saler = pro_infos[I][1]['Saler']

            delivery = pro_infos[I][1]['Delivery Way']
            first_date = pro_infos[I][1]['Date First Available']
            review_rate = pro_infos[I][1]['Review Rate']
            one_star = pro_infos[I][1]['Review Details']['1 star']
            two_star = pro_infos[I][1]['Review Details']['2 star']
            three_star = pro_infos[I][1]['Review Details']['3 star']
            four_star = pro_infos[I][1]['Review Details']['4 star']
            five_star = pro_infos[I][1]['Review Details']['5 star']
            stars = [one_star, two_star, three_star, four_star, five_star]

            ws.insert_image(col_num, I + 1, 'images/%s.jpg' % asin, {'x_scale': 0.2,
                                                                     'y_scale': 0.2,
                                                                     'x_offset': 10,
                                                                     'y_offset': 10,
                                                                     'url': url})
            ws.write(col_num, I+1, '', style)
            col_num += 1

            name_list = ['1 star', '2 star', '3 star', '4 star', '5 star']
            num_list = [int(stars[j].strip().strip('%')) for j in range(5)]
            grey_list = [100 - j for j in num_list]
            rects = plt.barh(range(5), num_list, tick_label=name_list, color='orange')
            plt.barh(range(5), grey_list, color='grey', left=[rect.get_width() for rect in rects])
            k = 0
            for rect in rects:
                plt.text(102, rect.get_y() + rect.get_height() / 2, str(num_list[k]) + '%', ha='left', va='center',
                         fontdict={'fontsize': 'xx-large'})
                plt.text(0, rect.get_y() + rect.get_height() / 2, name_list[k], ha='right', va='center',
                         fontdict={'color': 'blue',
                                   'fontsize': 'xx-large'})
                k += 1
            plt.text(10, -1, str(review_rate), fontdict={'fontsize': 30})
            plt.axis('off')
            if not exists('reviews_shot'):
                mkdir('reviews_shot')
            plt.savefig('reviews_shot/%s.jpg' % asin)
            plt.close()


            row_value = [str(rank), str(size), str(cm_size), str(weight), str(kg_weight), str(saler), str(delivery), int(review_num[:-16].replace(',', ''))]
            for j in range(len(row_value)):
                ws.write(j + col_num, I + 1, row_value[j], style)
            col_num += len(row_value)

            ws.insert_image(col_num, I + 1, 'reviews_shot/%s.jpg' % asin, {'x_scale': 0.2325, 'y_scale': 0.3,
                                                                           'x_offset': 3, 'y_offset': 13})
            ws.write(col_num, I + 1, '', style)
            col_num += 1

            row_value2 = [float(price[1:]), str(first_date)]
            for j in range(len(row_value2)):
                ws.write(j + col_num, I + 1, row_value2[j], style)
            col_num += len(row_value2)

            # 销量， 销量趋势
            for j in range(2):
                ws.write(j + col_num, I + 1, '', style)
            col_num += 2

            ws.write(100, I+1, str(url))

            ws2.insert_image(1, 3*I+1, 'images/%s.jpg' % asin, {'x_scale': 0.2,
                                                                'y_scale': 0.2,
                                                                'x_offset': 180,
                                                                'y_offset': 10,
                                                                'url': url})

            logging.info('准备翻译评论--ASIN: %s  ......\n' % asin)

            threads = [TranslaterThread(wb, ws2, pro_infos[I][1]['Reviews info'], style, arr) for j in range(10)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        except KeyError as e:
            logging.info(e, url)


    for I in range(len(arr[:20])):
        ws2.write(0, 3 * ncol + 1, 'Words', style)
        ws2.write(0, 3 * ncol + 2, 'Translation', style)
        ws2.write(0, 3 * ncol + 3, 'Frequency', style)
        ws2.write(I + 1, 3 * ncol + 1, str(arr[I][0]), style)
        try:
            ws2.write(I + 1, 3 * ncol + 2, translate_format(arr[I][0]), style)
        except KeyError:
            logging.info(arr[I][0])
        ws2.write(I + 1, 3 * ncol + 3, int(arr[I][1]), style)


    # 插入词频饼状图
    chart = wb.add_chart({'type': 'pie'})
    chart.add_series({
        'name': 'Word Frequency Data',
        'categories': ['%s' % review_detail_name, 1, 3*ncol + 1, 11, 3*ncol + 1],
        'values': ['%s' % review_detail_name, 1, 3*ncol + 3, 11, 3*ncol + 3],
        'data_labels': {'value': 1,
                        'category': 1}
    })
    chart.set_title({'name': 'Word Frequency Top 10'})
    chart.set_style(10)
    ws2.insert_chart(4, 3 * ncol + 4, chart, {'x_offset': 25, 'y_offset': 20})
    logging.info('\nExcel写入完成......')
    wb.close()


def product_info(tuple_link):
    global ama_url
    url = tuple_link[1]
    soup = urlread(url)

    reg = r'https://www\.amazon\.(.*?)/'
    ama_url = 'https://www.amazon.' + findall(reg, url)[0] + '/'
    pro_info = {}
    pro_info['Num'] = tuple_link[0]
    try:
        try:
            logging.info('way 1')
            information = soup.find(id='prodDetails').find_all('tr')
            if information:
                for item in information:
                    if ama_url == 'https://www.amazon.com/':
                        tip = item.th.get_text().strip()
                        try:
                            if tip == 'Best Sellers Rank':
                                ranks = item.td.span.find_all('span')
                                if len(ranks) > 1:
                                    pro_info['Best Sellers Rank'] = ranks[1].get_text()
                                else:
                                    pro_info['Best Sellers Rank'] = ranks[0].get_text()
                            else:
                                pro_info[tip] = item.td.get_text().strip()
                                if tip == 'Shipping Weight':
                                    ship_weight(pro_info, pro_info['Shipping Weight'])

                        except AttributeError as e:
                            logging.info('Error 1:' + e)
                            pass

                    elif ama_url == 'https://www.amazon.co.uk/':
                        uk_info = item.find_all('td')
                        uk_title = uk_info[0]
                        uk_text = uk_info[1]
                        if uk_title.get_text() == 'Best Sellers Rank':
                            ranks = uk_text.find_all('span')
                            pro_info['Best Sellers Rank'] = ranks[0].get_text() + ' ' + ranks[1].get_text()
                        else:
                            pro_info[uk_title.get_text()] = uk_text.get_text()
            else:
                logging.info('Could not find id="prodDetails",' + url)
        except:
            logging.info('way 2')
            information = soup.find(id='detail-bullets').find(class_='content').find_all('li')
            pro_info['Shipping Weight'] = ' '
            if information:
                for item in information:

                    try:
                        title, content = item.get_text().split(':', 1)
                        pro_info[title.strip()] = content.strip()

                    except:
                        pass
                ship_weight(pro_info, pro_info['Shipping Weight'])
                if 'Product Dimensions' not in pro_info:
                    pro_info['Product Dimensions'] = '0 x 0 x 0 inch'
                elif ';' in pro_info['Product Dimensions']:
                    pro_info['Product Dimensions'], pro_info['Item Weight'] = pro_info['Product Dimensions'].split(';')

                bsr = soup.find(id='detail-bullets').find(class_='content').find('li', id='SalesRank')

                ranks = bsr.find('li')
                rank_str = ''
                if ranks is not None:
                    rank = ranks.find_all('span')
                    for j in rank:
                        rank_str += ' ' + j.get_text()
                else:
                    reg = '(#.*?)\(See Top 100 '
                    pattern = compile(reg)
                    res = findall(pattern, bsr.get_text())
                    logging.info(res)
                    rank_str += res[0]
                pro_info['Best Sellers Rank'] = rank_str.replace('\xa0', ' ').strip()
            else:
                logging.info('Could not find id="detail-bullets",' + url)
    except AttributeError as e:
        logging.info(e)
        logging.info('Error 2:' + url)

    # 评论数
    get_review_qty(pro_info)
    # 卖家
    get_saler(pro_info, soup)
    # 价格
    get_price(pro_info, soup)
    # 链接
    pro_info['Url'] = url
    # 图片
    get_pic(pro_info, soup)
    # 评论
    get_rev(pro_info, soup)
    # 发货方式
    merchant_info(pro_info, soup)
    # 评论细节
    a = get_all_stars(soup)
    review_details = star_percent(a)
    pro_info['Review Details'] = review_details
    if 'Package Dimensions' not in pro_info:
        if 'Product Dimensions' in pro_info:
            pro_info['Package Dimensions'] = pro_info['Product Dimensions']
        else:
            pro_info['Package Dimensions'] = ''
    pro_info['Package Dimensions(cm)'] = inch_to_cm(pro_info['Package Dimensions'])
    try:
        pro_info['Shipping Weight(kg)'] = pound_to_kg(pro_info['Shipping Weight'])
    except KeyError:
        pro_info['Shipping Weight'] = 'Not Found'
        pro_info['Shipping Weight(kg)'] = 'Not Found'
        logging.info(url)

    if 'Date First Available' not in pro_info:
        pro_info['Date First Available'] = ''

    return tuple_link[0], pro_info


def get_img(url, asin):
    # logging.info(url)
    s = Session()
    req = Request('GET', url, headers=headers, cookies=cookie)
    prepared_request = s.prepare_request(req)
    settings = s.merge_environment_settings(prepared_request.url, None, None, None, None)
    response = s.send(prepared_request, **settings)
    if not exists('images'):
        mkdir('images')
    open(r'images/%s.jpg' % asin, 'wb').write(response.content)


def save_links(link_box):
    file = open('amazon links.txt', 'w')
    for BOX in link_box:
        link = BOX.get('1.0', END)
        if link.strip() != '':
            file.write(link.strip())
            file.write('\n')


def clear_links():
    for b in boxes:
        b.delete('1.0', END)


def resize(w, h, w_box, h_box, pil_image):
    f1 = w_box / w
    f2 = h_box / h
    factor = min([f1, f2])

    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)


class Tkshoot(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title('亚马逊产品调查表')
        self.geometry('1100x600+200+100')
        # self.wm_attributes('-topmost', 1)
        self.protocol('WM_DELETE_WINDOW', self.del_pic)

    def remove(self, arr):
        progress = Option(arr)
        self.wait_window(progress)
        return progress.arr

    def del_pic(self):
        if messagebox.askyesno('想好了嘛?', '真的要退出嘛?'):
            self.destroy()


class Option(Toplevel):

    def __init__(self, arr):
        Toplevel.__init__(self)
        self.title('屏蔽关键词')
        self.arr = arr
        self.copy_arr = list(self.arr.items())
        self.geometry('200x450+500+200')
        self.show_options()
        self.wm_attributes('-topmost', 1)

    def show_options(self):
        row = Frame(self)
        row.pack(fill="x")
        label = Label(row, text='点击下列需要屏蔽的关键词', width=40)
        label.pack()
        for i in range(10):
            key, value = self.copy_arr.pop(0)
            btn = Button(row, text=key+': '+str(value), width=20)
            btn['command'] = lambda row=row, binst=btn: self.func(row, binst)
            btn.pack()
        self.finbtn = Button(row, text='完成', width=8, command=self.quit_window)
        self.finbtn.pack()

    def func(self, row, btn):
        print(btn['text'])
        self.arr.pop(btn['text'].split(':')[0])
        print(self.arr)
        self.finbtn.destroy()
        btn.destroy()
        if self.copy_arr:
            key, value = self.copy_arr.pop(0)
            btn1 = Button(row, text=key+': '+str(value), width=20)
            btn1['command'] = lambda binst=btn1: self.func(row, binst)
            btn1.pack()
            self.finbtn = Button(row, text='完成', width=8, command=self.quit_window)
            self.finbtn.pack()

    def quit_window(self):
        self.destroy()


class Control:

    def __init__(self, master, boxes, func):
        self.parent = master
        self.boxes = boxes
        self.label = []
        self.func = func
        self.x = 50
        self.y = 50
        self.btns = []
        self.label2 = Label(self.parent)
        if exists('Snoopy.ico'):
            self.parent.iconbitmap('Snoopy.ico')
        with open('amazon links.txt', 'r') as file:
            a = file.read()
            self.num = round(len(a.split('\n')) / 2)
        if self.num <=7:
            self.init_box()
        else:
            self.init_box(self.num)
        if exists('amazon links.txt'):
            f = open('amazon links.txt')
            for box in self.boxes:
                box.insert(END, f.readline())
        self.init_btn()

    def init_box(self, num=7):
        for num in range(num):
            x = self.x
            y = self.y + 60 * num
            lable1 = Label(self.parent, text='网址%s:' % str(2*num+1),
                  )
            lable1.place(x=x+30, y=y, anchor=NW)
            box1 = Text(self.parent,
                        width=50,
                        height=2,
                        bd=2.1)
            box1.place(x=x+100, y=y, anchor=NW)
            lable2 = Label(self.parent, text='网址%s:' % str(2*num+2),
                  )
            lable2.place(x=11*x+30, y=y, anchor=NW)
            box2 = Text(self.parent,
                        width=50,
                        height=2,
                        bd=2.1)

            box2.place(x=11*x+100, y=y, anchor=NW)
            self.boxes.extend([box1, box2])
            self.label.extend([lable1, lable2])

    def add_box(self):
        self.num += 1
        lable1 = Label(self.parent, text='网址%s:' % str(2 * (self.num-1) + 1))
        lable1.place(x=self.x + 30, y=self.y+60*(self.num-1), anchor=NW)
        box1 = Text(self.parent,
                    width=50,
                    height=2,
                    bd=2.1)
        box1.place(x=self.x + 100, y=self.y+60*(self.num-1), anchor=NW)
        timer = Timer(0.5, self.show_pic, (box1, 20, 50 + 60 * (self.num-1)))
        timer.daemon = True
        timer.start()
        label2 = Label(self.parent, text='网址%s:' % str(2 * (self.num-1) + 2))
        label2.place(x=11 * self.x + 30, y=self.y+60*(self.num-1), anchor=NW)
        box2 = Text(self.parent,
                    width=50,
                    height=2,
                    bd=2.1)
        box2.place(x=11 * self.x + 100, y=self.y+60*(self.num-1), anchor=NW)
        timer2 = Timer(0.5, self.show_pic, (box2, 520, 50 + 60 * (self.num-1)))
        timer2.daemon = True
        timer2.start()
        self.label.extend([lable1, label2])
        self.boxes.extend([box1, box2])
        self.parent.geometry('1100x%s' % str(180+60*(self.num-1)))

    def del_box(self):
        self.num -= 1
        for lable in self.label[-2:]:
            lable.destroy()
            self.label.pop()
        for box in self.boxes[-2:]:
            box.delete('1.0', END)
            box.destroy()
            self.boxes.pop()
        self.parent.geometry('1100x%s' % str(180 + 60 * (self.num - 1)))

    def init_btn(self):
        btn = Button(self.parent, text="下载Excel", relief=RAISED, command=self.func)
        btn2 = Button(self.parent, text="清空链接", relief=RAISED, command=clear_links)
        btn3 = Button(self.parent, text="增加链接", relief=RAISED, command=self.add_box)
        btn4 = Button(self.parent, text="删除链接", relief=RAISED, command=self.del_box)
        btn.place(x=340, y=10, anchor=NW)
        btn2.place(x=440, y=10, anchor=NW)
        btn3.place(x=540, y=10, anchor=NW)
        btn4.place(x=640, y=10, anchor=NW)
        self.btns.extend([btn, btn2, btn3, btn4])

    def show_pic(self, box, x_p, y_p):
        try:
            link = box.get('1.0', END).strip()
            if link:
                soup = urlread(link)
                pic = soup.find('div', id='imgTagWrapperId').img['data-a-dynamic-image']
                pic = loads(pic)
                pic_link = sorted(pic.items(), key=lambda d: d[1]).pop()[0]
                s = Session()
                req = Request('GET', pic_link, headers=headers, cookies=cookie)
                prepared_request = s.prepare_request(req)
                settings = s.merge_environment_settings(prepared_request.url, None, None, None, None)
                response = s.send(prepared_request, **settings)
                img = Image.open(BytesIO(response.content))
                w_box, h_box = 50, 50
                w, h = img.size
                pil_img_resize = resize(w, h, w_box, h_box, img)
                w_re, h_re = pil_img_resize.size
                tk_image = ImageTk.PhotoImage(pil_img_resize)
                label = Label(self.parent, image=tk_image, width=w_re, height=h_re)
                label.image = tk_image
                label.place(x=x_p, y=y_p, anchor=NW)
                label.bind("<Enter>", self.handlerAdaptor(self.view_large, pic=img, x_p=x_p, y_p=y_p))
                label.bind("<Leave>", self.handlerAdaptor(self.hide_view))
                timer = Timer(0.5, self.judge_change, (label, box, link, x_p, y_p))
                timer.daemon = True
                timer.start()
            else:
                timer = Timer(1, self.show_pic, (box, x_p, y_p))
                timer.daemon = True
                timer.start()
        except (RuntimeError, AttributeError, TclError):
            pass

    def handlerAdaptor(self, fun, **kwds):
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

    def view_large(self, event, pic, x_p, y_p):
        w_box, h_box = 400, 400
        w, h = pic.size
        pil_img_resized = resize(w, h, w_box, h_box, pic)
        tk_image = ImageTk.PhotoImage(pil_img_resized)
        w_re, h_re = pil_img_resized.size
        try:
            self.label2.configure(image=tk_image, width=w_re, height=h_re)
            self.label2.image = tk_image
            if y_p + h_re >= 580:
                self.label2.place(x=x_p + 100, y=580 - h_re)
            else:
                self.label2.place(x=x_p + 100, y=y_p + 50)
        except TclError:
            pass

    def hide_view(self, event):
        self.label2.destroy()
        self.label2 = Label(self.parent)

    def judge_change(self, label, box, link, x_p, y_p):
        try:
            if box:
                link2 = box.get('1.0', END).strip()
                if link != link2:
                    label.destroy()
                    timer = Timer(0.5, self.show_pic, (box, x_p, y_p))
                    timer.daemon = True
                    timer.start()
                else:
                    timer = Timer(0.5, self.judge_change, (label, box, link, x_p, y_p))
                    timer.daemon = True
                    timer.start()
            else:
                label.destroy()
        except:
            label.destroy()


class TreadMain:
    def __init__(self, boxes, master):
        self.master = master
        self.boxes = boxes
        self.gui = Control(master, self.boxes, self.starting)

        for i, box in enumerate(self.boxes):
            if i / 2 == i // 2:
                timer = Timer(1, self.gui.show_pic, (box, 20,  50 + 60 * i/2))
                timer.daemon = True
                timer.start()
            else:
                timer = Timer(1, self.gui.show_pic, (box, 520, 50 + 60 * (i-1)/2))
                timer.daemon = True
                timer.start()

    def start_running(self):
        global pro_infos, ama_url
        init_cencor_word()
        pro_infos = []
        save_links(self.gui.boxes)
        links = []
        for i, BOX in enumerate(self.gui.boxes):
            link = BOX.get('1.0', END)
            if link.strip() != '':
                links.append((i, link.strip()))
        threads = [Producer(links) for i in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        pro_infos = sorted(pro_infos, key=lambda x: x[0])
        for col_nums, item in enumerate(pro_infos):
            for peace in item[1]['Reviews info']:
                peace['col_num'] = col_nums
        frequency = []
        for PRO_INFO in pro_infos:
            for review in PRO_INFO[1]['Reviews info']:
                frequency.append(review['content'])
        arr = freq_word(frequency)
        if arr:
            arr = self.master.remove(arr)
        arr = list(arr.items())
        logging.info('数据写入Excel......')
        excel_writer(arr)

    def starting(self):
        self.thread = Thread(target=self.start_running)
        self.thread.start()


class Producer(Thread):

    global pro_info

    def __init__(self, links):
        Thread.__init__(self)
        self.pages = links

    def run(self):
        global count
        while self.pages:
            product = self.pages.pop(0)
            try:
                res = product_info(product)
                my_lock.acquire()
                pro_infos.append(res)
                my_lock.release()
            except AttributeError as e:
                logging.info('\n<Error>Thread Error')
                logging.info(e)


class TranslaterThread(Thread):

    def __init__(self, workbook, worksheet, review_info, style, arr):
        Thread.__init__(self)
        self.worksheet = worksheet
        self.review_info = review_info
        self.style = style
        self.workbook = workbook
        self.arr = arr

    def run(self):
        global count
        while self.review_info:
            en_review = self.review_info.pop(0)
            purchase_time = en_review['time']
            style = en_review['style']
            rate = en_review['rate']
            title = en_review['title']
            en_content = en_review['content']
            en_old_content = en_content
            row = en_review['row_num']
            col = en_review['col_num']
            rr = 7
            try:
                urlstr = [('+', 'plus'), ('%', 'percent'), ('&', 'and'), ('#', 'no.'),
                          ('?', ''), ('/', ' or '), ('\n', ''), ('=', 'equal'), ('!', ' '),
                          ('$', 'dollar of '), ('-', ' ')]
                for item in urlstr:
                    en_content = en_content.replace(item[0], item[1])
                cn_review = translate(secretId, secretKey, en_content.lower().encode('ascii', 'ignore'))
                rep_list = ['B', '‘', '“', '”', '’', 'b']
                for rep in rep_list:
                    cn_review = cn_review.replace(rep, '')
                my_lock.acquire()
                # logging.info('%s: %s' % (en_content, cn_review))
                self.worksheet.merge_range(5 * row + rr, 3 * col + 1, 5 * row + rr + 1, 3 * col + 1, title, self.style)
                self.worksheet.write(5 * row + rr + 2, 3 * col + 1, rate, self.style)
                self.worksheet.write(5 * row + rr + 3, 3 * col + 1, style, self.style)
                self.worksheet.write(5 * row + rr + 4, 3 * col + 1, purchase_time, self.style)
                self.worksheet.merge_range(5 * row + rr, 3 * col + 2, 5 * row + rr + 4, 3 * col + 2, '', self.style)
                format_words(self.workbook, self.worksheet, 5 * row + rr, 3*col+2, en_old_content, self.arr)
                self.worksheet.merge_range(5 * row + rr, 3 * col + 3, 5 * row + rr + 4,
                                           3 * col + 3, cn_review, self.style)
                my_lock.release()
                sleep(0.5)
            except KeyError:

                self.worksheet.merge_range(5 * row + rr, 3 * col + 1, 5 * row + rr + 1, 3 * col + 1, title, self.style)
                self.worksheet.write(5 * row + rr + 2, 3 * col + 1, rate, self.style)
                self.worksheet.write(5 * row + rr + 3, 3 * col + 1, style, self.style)
                self.worksheet.write(5 * row + rr + 4, 3 * col + 1, purchase_time, self.style)
                self.worksheet.merge_range(5 * row + rr, 3 * col + 2, 5 * row + rr + 4, 3 * col + 2, '', self.style)
                format_words(self.workbook, self.worksheet, 5 * row + rr, 3 * col + 2, en_old_content, self.arr)

                logging.info('\n%s: 翻译失败\n' % en_content)


if __name__ == '__main__':
    cookie = {'session-id': '134-3856831-6537631',
              'session-id-time': '2082787201l',
              'ubid-main': '130-1157931-8753215',
              's_fid': '4FD2C3C011299EE8-021F9EAFC572E127',
              's_dslv_s': 'First%20Visit',
              's_vn': '1572424924025%26vn%3D1',
              's_invisit': 'true',
              'regStatus': 'pre-register',
              's_cc': 'true',
              'aws-priv': 'eyJ2IjoxLCJzdCI6MX0=',
              's_depth': '3',
              's_dslv': '1540889004876',
              's_nr': '1540889004877-New',
              'a-ogbcbff': '1',
              'session-token': "XT04m2XC5juHX3i+mD5nd1zVynI8BBpKDb2uPsWRE+8UDWUdUiXr/nsQ83416x9vEKAM8kFqdSfI+adjwQOEzJVxi7PqYJza50ac90mWk9PioGVgm9cBUYyw/nHpQq6RR4N7EnJzAJyJVPrVB2vMiQ8ky8qZG2xTzHMU1qMbjNXWylJseSVFIthckiR9U2iABztN1qw5EQtAhm7R8HpEyrRYq0l7sa1HYSM9sq3yOeo=",
              'x-main': "PoWZ3rCn6D9ji?xtgsYr8uztxg9JB6dks4iF3zSRFJjawUDjZR7eFCVj6MP0@m9q",
              'at-main': 'Atza|IwEBII5BxWpps3ravM52GNR7oLZ6VewyY4hxMykt_m94zkGp_6Wf-XPVd1DOX0ioAMGyBqPncEceKRc_9kzSZ1vdDQc5cX2juiW4rUWKnRO-U1COjGl3iqIR8Yf1JLZwnYLgjkX--FOUDEeZXtTbyHvsmNsLS0Lc8BboA7Tp8AFRVZTvgWm2EB186NJKm8wJXNgsOuj94NkFp9UbuBPlY7cfaH6iQg8W1yfjp4XTB8p_SYE1yXDr_bFbEUorcEMRgoGHz2KeBr1LIKyEEyXYgaROUBbpiAywijGPo1WA6j1S-3JAwN6oOqE96ag1dxLhqwRyaqOijDZoGJxWL6gV3bLrqCMcGHWgofOKFynd6kyfFlBIIMFDi3KROqq1y9SgnR1wbg_em19l8_DRHzXGHKccaIIk',
              'sess-at-main': '"YSLtfGHW3yvMfEy/nQpu9Edyj4aXcjDnbjsfl2TT5xA="',
              'sst-main': 'Sst1|PQFT0zg0UbdXrmR0ohnZgoejC-Dpn37khTJS4YoeexmrA6z1zkSSwaXBmgtWznvt8YdqG4wjh6z-zXF8r3hO6HABT6YB6W2ELV-OppbqrW1abrJNneG38MS-1G1gKvkmT-VA4e_Lx5aHxQiWkMu5WatDLZVWUhUBCcaHvHeMT8j_LddjHXZskmN9gDamMMCA9WvOJbQMl4dTZlqdRXOGNUypEiziOfSlRLe8Ojn2H9LCqNLektine0nLTIbaPJcNCHq1IEo2cc3Sx4vYLvfUnPTPij6Itghi7DxnHhDUEY9G8oPto0tKTHOQJpbXhHfihCpHc1_7KIev1Dce5MdtmREZJQ',
              'lc-main': 'en_US',
              'x-wl-uid': '1gcAWcUxqoUoSCND3zabY7xQtrE1c8wWhsrfn8NwTyvWPgpjEnWfI/VBLzn0pwcamFEXs9CmGDUywbOllXHI6Aav2VQB1lVCorL+J6q0zW8vv6yhnP5wfoaQhhca7pZQTsFnftvRfpEw='}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
    my_lock = Lock()
    boxes = []
    root = Tkshoot()
    tool = TreadMain(boxes, root)
    root.mainloop()
