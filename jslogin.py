from pykeyboard import PyKeyboard
from pymouse import PyMouse
import time
username = '531493190@qq.com'
password = 'amazon5314'
def ctrland(key):
    k = PyKeyboard()
    k.press_key(k.control_key)
    k.tap_key(key)
    k.release_key(k.control_key)
    time.sleep(0.5)

def altand(key):
    k = PyKeyboard()
    k.press_key(k.alt_key)
    time.sleep(0.5)
    k.tap_key(key)
    k.release_key(k.alt_key)

def click_nw():
    m = PyMouse()
    m.click(1, 1)

k = PyKeyboard()
click_nw()
time.sleep(0.5)
ctrland('q')
time.sleep(2)
k.tap_key(k.tab_key)
k.tap_key(k.tab_key)
k.tap_key(k.tab_key)
for i in username:
    k.tap_key(i)
k.tap_key(k.tab_key)
for i in password:
    k.tap_key(i)
k.tap_key(k.tab_key)
k.tap_key(k.tab_key)
k.tap_key(k.enter_key)
