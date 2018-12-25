import pandas as pd
from requests import Session, Request
import time
from bs4 import BeautifulSoup
import numpy as np
from threading import Thread, Lock, current_thread
from queue import Queue
from intocm import weight, fbafee, cal_size, calcu_profit
import xlsxwriter
import xlrd
import os
import re
import warnings
warnings.filterwarnings("ignore")


def urlread(url):
    cookie = {'s_fid': '4FD2C3C011299EE8-021F9EAFC572E127',
              'regStatus': 'pre-register',
              's_cc': 'true',
              'aws-priv': 'eyJ2IjoxLCJzdCI6MX0=',
              'lc-main': 'en_US',
              's_sq': '%5B%5BB%5D%5D',
              's_ppv': '73',
              's_vnum': '1972898082437%26vn%3D2',
              'appstore-devportal-locale': 'zh_CN',
              'AMCVS_4A8581745834114C0A495E2B%40AdobeOrg': '1',
              '_mkto_trk': 'id:365-EFI-026&token:_mch-amazon.com-1540974668299-31178',
              'AMCV_4A8581745834114C0A495E2B%40AdobeOrg': '-330454231%7CMCIDTS%7C17836%7CMCMID%7'
                                                          'C25155120772369371358210843232415684168%7CMCOPTOUT-1540'
                                                          '981868s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2',
              's_lv': '1540974671016',
              'skin': 'noskin',
              's_vn': '1572424924025%26vn%3D2',
              'c_m': 'undefinedwww.google.comSearch%20Engine',
              's_dslv': '1541406758240',
              's_nr': '1541406758252-Repeat',
              'at-main': 'Atza|IwEBIGDfPjZo5hDFBQpJN9pelu'
                         '1nxcxRxXlFDdkPbZJNaujrAcSHXWRyXnet'
                         'IJD8-Xc0RjufK60VdzWR76e52XZF2l2K5bi'
                         'Z14LZ5x-WR8Z7zW0UIZD9cENkvSe93N-T3jqBI6MLLM_OEzkaBZgvqmFmY'
                         'IqVwE50JFYXAaN1JOy9ZO1E5TA274nFQhPdCgkxeVq-'
                         'v4wuJNK_b0xy4q2LtW3Iz7PnDFLFkl'
                         'clRqUgiTsmHiNe_1REedFH6zQAw5GQ'
                         'CMqMOgqdaKV88ABAZuk_uuGjeZBvK5Qfa3u4s'
                         'r1_acP7m2nPJN9-yocaqVZCZK0L2OjBQDmcMvCilgESIQw0l-EMgsn8FIS'
                         'Toi6RY6q72W6FS60Og3ZG6asvIHsgJYb7vVh7D'
                         'aDUddvXsd4UGzKfGB42h6oV',
              'sess-at-main': '"wgcyvBZjDCBuncoS/H9VjJhOy2O+nEBp4LkKLFs8ua0="',
              'sst-main': 'Sst1|PQFl-RHLfKFhBLGI63CHtnpQC96pev6fVPbp'
                          '-FLBZ62Br7c6GMrNs28Q7JXZB7wjwgBrBwUu9rl1be8'
                          'lwbCyWbhu0zfCRG6bB6-_bIYtr25IGljiKCF_6'
                          'DrunZCtYtSDqvbfubXSgbydAgsZ6IM586uTGnjS'
                          'ldtkg4_ViqQNq5DLvBhqWFhfv8lTBAiAS32TM1O'
                          'Cm4YoIAu92DiMCPFepL4l7Q8n6WxHxgFHmRauK4p'
                          'iKioYvIGyu4LAkZ_yuiSUcjp2yarN8fL-8GcQiZiH'
                          'YjdEKXC3QUzlKkdDjlUHSefH4BMK4ya3ap0b8VUpHO'
                          '81wUO9G9KCL4MY8jtMzacV4Eb7mg',
              'session-id-time': '2082787201l',
              'aws-ubid-main': '146-1514507-8114676',
              'ubid-main': '133-9843259-4548638',
              'session-id': '140-8001059-6493313',
              'x-wl-uid': '1G0Jf35NtTqOpdzgthK84Wx7oJLiCoEtPbTb'
                          '21A08VDZjB6kO5i6dWql++nKfoIUhw4TEvedcbUZ'
                          'Lmpo0sygcG+1jFrupazYD7gyfA5N306XDqLd7PdrW'
                          'UGIa5CvtT9PlSFx7k3cuyI8=',
              'x-main': '"SDJblG8cOpFVYTnRy9K9bxf?DA@?dUjf@C2l8h5@EvAL1ulFAUN@b?iXTdojA@X6"',
              'session-token': '"+Hctf2e+nbgC22ZWAx9MVg8Mo068Q/nNU9BY'
                               '1tXTbgXt4pMaY5FcIw/td5R4KkPKwsGjb4P2JAB'
                               'Vy84cbCTP/NpW6pjjB+0yTzuqmUjwGqxlxqm9qbT'
                               'LK3a6Nh1Szzfs9p92VWL+YZlQ14sbjimLzynDLqhJ'
                               'rlPN5Md7ttUaRaPGoNfpigf1I8DDmwAgbuv/Fo6F3w'
                               'nAoZpoXqapAt8TpOGHKnpVwVHMBq93b/XYFtY1u4Fay'
                               'PvvZFXIisRKur+ohD6lf9idHeRP9/nk+QjXbw=="', }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWe'
                      'bKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
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


def get_price(url):
    soup1 = urlread(url)
    try:
        price = soup1.find(id='priceblock_ourprice')
        dollar = price.string
    # print(dollar)
        return dollar
    except:
        return 0


def price_info(pro_info):
        price = get_price(pro_info)
        print('Getting \'s price: %s' % (price))
        return price


class Producer(Thread):
    global price_group

    def __init__(self):
        Thread.__init__(self)
        self.pages = pro_infos
        self.queue = Queue()

    def run(self):
        while self.pages:
            product = self.pages.pop(0)
            try:
                price_group.append((int(product[0]), price_info(product[1])))
            except AttributeError as e:
                print(e)


def main():
    threads = [Producer() for i in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    price_group.sort(key=lambda x: x[0])

    price_res = [i[1] for i in price_group]
    ncols = worksheet.ncols
    nrows = worksheet.nrows
    for i in range(ncols):
        for j in range(nrows):
            ws.write(j, i, str(worksheet.col_values(i, j, j+1)[0]))
    ws.write_column(1, 17, price_res)
    cost = worksheet.col_values(18, 1)
    ps = worksheet.col_values(15, 1)
    w = worksheet.col_values(16, 1)
    sea = worksheet.col_values(22, 1)
    profit = []
    for i in range(len(price_res)):
        price_res[i] = str(price_res[i]).replace('$', '')
        size = cal_size(ps[i])
        wt = weight(w[i])
        freight = fbafee(size, wt)
        pf = calcu_profit(freight, str(cost[i]), str(price_res[i]))
        profit.append(pf[0]) if sea[i] == '√' else profit.append(pf[1])
    output = [int(i) for i in profit]
    for i in range(len(output)):
        ws.write(i+1, 19, '%.02f' % profit[i])
    for i in range(len(dict2)):
        try:
            ws.write(i+1, 11, '%d' % list(dict2.values())[i])
        except TypeError as e:
            print(dict2.values())
    wb.close()


if __name__ == '__main__':

    excel_path = 'pro_info_backup.xls'
    save_path = 'pro_info.xls'
    workbook = xlrd.open_workbook(excel_path)
    worksheet = workbook.sheet_by_index(0)
    wb = xlsxwriter.Workbook(save_path)
    ws = wb.add_worksheet('Pro_info')
    pro_links = worksheet.col_values(5, 1)
    pro_asins = worksheet.col_values(4, 1)
    pro_sku = worksheet.col_values(3, 1)
    pro_id =worksheet.col_values(0, 1)
    asins = [i for i in pro_asins if str(i).strip() != '']
    links = [i for i in pro_links if i != '']
    sku = [i for i in pro_sku][:len(asins)]
    pro_infos = list(zip(pro_id, links))
    my_lock = Lock()
    price_group = []

    sales_path = r'Z:/8销控表+库存盘点/销控表/'
    file_names = os.listdir(sales_path)
    rep = r'\d{0,2}\.\d{0,2}.*?（新品）\.xlsx'
    for i in file_names:
        if re.match(rep, i):
            file_name = re.match(rep, i).group(0)

    file_path = sales_path + file_name
    print(file_path)

    print('opening sales excel')
    start_time = time.time()
    workbook2 = xlrd.open_workbook(file_path)
    worksheet2 = workbook2.sheet_by_index(1)
    ncols = worksheet2.ncols
    nrows = worksheet2.nrows
    print(time.time() - start_time)

    sku2 = worksheet2.col_values(5, 1, nrows - 2)
    sales = worksheet2.col_values(ncols - 2, 1, nrows - 2)

    dict = {}
    dict2 = {}
    for i in range(len(sku2)):
        dict[sku2[i]] = sales[i]
    for i in range(len(sku)):
        if sku[i] in dict:
            dict2[sku[i]] = dict[sku[i]]
        else:
            dict2[sku[i]] = 0
    main()



