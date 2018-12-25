
from requests import Session, Request
from bs4 import BeautifulSoup
import re
from threading import Thread, Lock


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


def get_page_quantity(soup):
    see_all_reviews = soup.find(class_='a-link-emphasis a-text-bold')
    soup2 = urlread(ama_url+see_all_reviews['href'])
    all_cratical_reviews = soup2.find('a', {'data-reftag': 'cm_cr_arp_d_viewpnt_rgt'})
    soup3 = urlread(ama_url+all_cratical_reviews['href'])
    page_quantity = soup3.find_all('li', class_='page-button')
    return page_quantity[-1].a.text, page_quantity[-1].a['href']


def general_urls(url, page_quantity):
    reg = r'(.*?cm_cr_arp_d_paging_btm_)\d+(.*?pageNumber=)\d+(.*)'
    link = re.findall(reg, url)[0]
    return [ama_url + '%s' % str(i+1).join(link) for i in range(int(page_quantity))]


def get_reviews(url):
    soup = urlread(url)
    reviews_info = []
    reviewers_info = soup.find_all(class_='a-section celwidget')
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
        if reviewer_info not in reviews_info:
            reviews_info.append(reviewer_info)
        print(reviews_info)
        return reviews_info


class ReviewGet(Thread):
    def __init__(self, tuple_urls):
        Thread.__init__(self)
        self.tuple_urls = tuple_urls

    def run(self):
        global result
        while self.tuple_urls:
            item = self.tuple_urls.pop(0)
            try:
                res = get_reviews(item)
                lock.acquire()
                result.append(res)
                lock.release()
            except BaseException as e:
                print(e)


ama_url = 'https://www.amazon.com'
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
url = 'https://www.amazon.com/Pet-Zone-Designer-Adjustable-Stainless/dp/B00TV1A6IA/ref=zg_bs_3024200011_1?_encoding=UTF8&psc=1&refRID=HC7TRPJ03T50N0P9ESYW'
soup = urlread(url)

page_quantity = get_page_quantity(soup)
print(page_quantity)
bad_review_urls = general_urls(page_quantity[1], page_quantity[0])
result = []
lock = Lock()
threads = [ReviewGet(bad_review_urls) for i in range(10)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print(result)