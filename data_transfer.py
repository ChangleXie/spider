import re
import sqlite3
import xlrd
xlname = 'test.xls'
db_name = 'py_sqlite.db'

def drop_table(table_name):
    conn = sqlite3.connect(db_name)
    words = 'drop table %s '
    conn.execute(words % table_name)
    conn.commit()
    conn.close()

drop_table('product')
conn = sqlite3.connect(db_name)

conn.execute('''create table product
                (ID INTEGER primary key autoincrement ,
                 sku TEXT,
                 name TEXT,
                 length INTEGER,
                 width INTEGER,
                 height INTEGER,
                 weight REAL,
                 in_stock_left_1 INTEGER,
                 in_stock_left_2 INTEGER,
                 daily_sale REAL,
                 last_time_rep_date TEXT
                  );''')
conn.commit()

wb = xlrd.open_workbook(xlname)
ws = wb.sheet_by_index(0)
info = []
titles = [(8, 'sku'), (2, 'name'), (3, 'length'), (4, 'width'), (5, "height"), (6, 'weight'), (16, 'in_stock_left_1'), (17, 'daily_sales')]


for i in range(ws.nrows-5):
    arr = []
    for item in titles:
        v = ws.cell(i+5, item[0])
        arr.append(v.value)
    conn.execute("insert into product (sku, name, length, width, height, weight, in_stock_left_1, daily_sale) values (?,?,?,?,?,?,?,?)", arr)
    conn.commit()

cursor = conn.execute("select * from product")
for i in cursor:
    print(i)
conn.close()
