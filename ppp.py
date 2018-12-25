
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pykeyboard import PyKeyboard
from bs4 import BeautifulSoup
from tkinter import Tk, Label, Text, Button, RAISED, END



def ctrland(key):
    k = PyKeyboard()
    k.press_key(k.control_key)
    k.tap_key(key)
    k.release_key(k.control_key)


def main():
    username = '531493190@qq.com'
    password = 'amazon5314'
    jslogin = 'chrome-extension://bckjlihkmgolmgkchbpiponapgjenaoa/login.html'
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }
    options.add_experimental_option('prefs', prefs)
    # options.add_extension('extensions/3.30_0.crx')
    options.add_extension('extensions/2.2.2_0.crx')
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    action = ActionChains(browser)
    url = xlsbox.get('1.0', END).strip()


    browser.get('chrome://extensions/shortcuts')
    browser.find_element_by_tag_name('body').send_keys(Keys.TAB, Keys.TAB, Keys.CONTROL, 'q', Keys.ENTER)

    js2 = 'window.open("%s")' % jslogin

    def swift_hand(i):
        handles = browser.window_handles
        browser.switch_to.window(handles[i])

    signal = True
    while signal:
        browser.execute_script(js2)
        swift_hand(1)
        browser.find_element_by_xpath('//*[@id="username"]').send_keys(username)
        browser.find_element_by_xpath('//*[@id="password"]').send_keys(password)
        browser.find_element_by_xpath('//*[@id="submit"]').click()
        ctrland(PyKeyboard().tab_key)
        action.key_down(Keys.CONTROL).send_keys('w').key_up(Keys.CONTROL)
        ctrland('w')
        time.sleep(3)
        js = 'window.open("%s");' % url
        print(js)
        browser.execute_script(js)
        swift_hand(1)
        ctrland(PyKeyboard().tab_key)
        ctrland('w')
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        time.sleep(3)
        ctrland('q')
        soup = BeautifulSoup(browser.page_source, 'lxml')
        res = soup.find_all('a', class_='js-est-sales-mo')
        print(res)
        if res is not None:
            signal = False

    for i in res:
        print(i.text)


def main2(self):
    main()


if __name__ == '__main__':

    root = Tk()
    root.title('一键登录JS')
    root.geometry('500x150')
    l1 = Label(root, text="输入网址")
    l1.pack()
    xlsbox = Text(root, width=50, height=5)
    xlsbox.pack()

    btn = Button(root, text="查看Js", relief=RAISED, command=main)
    btn.pack()
    xlsbox.bind('<Return>', main2)
    root.mainloop()


