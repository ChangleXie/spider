
def weight(w):
    if w:
        w = float(w)
        w = w / 454
        return w


def fbafee(arr, w):
    list1 = [i for i in arr[1:]]
    list1.sort()
    q = arr[0]
    sw = max([w, q * 200 / 0.454])
    sw = (sw - 0.0001) // 1 + 1
    fw = max([w * 0.454, q * 200])
    if list1[0] <= 8 and list1[1] <= 14 and list1[2] <= 18:
        if sw <= 1:
            p = 3.19
        elif sw <= 2:
            p = 4.71
        else:
            p = 4.71 + 0.38 * (sw - 1)
    else:
        if sw < 2:
            p = 8.13
        else:
            p = 8.13 + 0.38 * (sw - 1)
    return p, q, fw


def calcu_profit(fba, cost, price):
    if price == '':
        return 0, 0
    sfare = fba[1] * 1150 + fba[0] * 6.8
    ffare = fba[2] * 30 + fba[0] * 6.8
    sprofit = float(price) * 6.8 * 0.78 - float(cost) * 0.97 - sfare
    fprofit = float(price) * 6.8 * 0.78 - float(cost) * 0.97 - ffare
    return sprofit, fprofit

def cal_size(a):
    if isinstance(a, float):
        return 0, 0, 0, 0
    a = str(a)
    a = a.replace('*', 'x').replace('×', 'x').replace('X', 'x').replace('cm', '')
    x, y, z = a.split('x')
    x, y, z = float(x), float(y), float(z)
    q = x * y * z / 10 ** 6
    x, y, z = x / 2.54, y / 2.54, z / 2.54
    return q, x, y, z
# cost = 620
# price = 190
# w = weight(10800)
# a = '40*30*28'
# fbaf = fbafee(cal_size(a), w)
# profit = calcu_profit(fbaf, cost, price)
#
# print(cal_size(a))
# print(w, fbaf ,profit)