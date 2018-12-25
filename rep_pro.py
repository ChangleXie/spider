import re
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox


class View:
    def __init__(self, master):
        self.parent = master
        self.column = ['SKU', '产品名称', '长', '宽', '高', '重量', '总库存', '谷仓库存', '万邑通库存', '日销量', '上次补货时间']
        self.column2 = ['SKU', '产品名称', '体积', '重量', '总库存', '谷仓库存', '万邑通库存',  '日销量', '上次补货时间', '补货数量']
        self.frame = ttk.Frame(self.parent)
        self.frame2 = Frame(self.parent, height=1100, width=200)

        self.tree = ttk.Treeview(self.frame, height=20, show='headings', column=self.column)
        self.tree2 = ttk.Treeview(self.frame, height=20, show='headings', column=self.column2)
        self.ysb = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.ysb2 = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree2.yview)

        Label(self.frame2, width=20,text='推荐补货：').grid(row=0, column=1)
        Button(self.frame2, width=8, text='推荐', command=self.rec_rep).grid(row=0, column=2)
        Label(self.frame2, width=20, text='取消选中：').grid(row=1, column=1)
        Button(self.frame2, width=8, text='取消', command=self.clear_content).grid(row=1, column=2)
        # 添加空白标签隔开
        Label(self.frame2, height=20).grid(row=2, column=1)

        self.part2 = [['选中补货： ', '补货', self.rep_pro], ['添加产品： ', '添加', self.add_pro], ['删除产品： ', '删除', self.del_pro]]
        self.init_options()

        self.frame.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1)
        self.init_master()
        self.init_tree()
        self.db_name = 'py_sqlite.db'
        self.db_table = 'product'

    def init_master(self):
        self.parent.geometry('1400x900+200+100')
        self.parent.title('补货计划')

    def init_tree(self):
        self.tree.configure(yscrollcommand=self.ysb.set)
        self.tree2.configure(yscrollcommand=self.ysb2.set)
        for item in self.column:
            self.tree.column(item, width=100, anchor='center')
            self.tree.heading(item, text=item, command=lambda _col=item: self.tv_sort_col(self.tree, _col, False))
        for item in self.column2:
            self.tree2.column(item, width=100, anchor='center')
            self.tree2.heading(item, text=item, command=lambda _col=item: self.tv_sort_col(self.tree2, _col, False))

        Label(self.frame, text='全部产品').grid(row=2, column=0)
        self.tree.grid(row=3, column=0)
        self.ysb.grid(row=3, column=1, sticky="ns")
        Label(self.frame, text='补货产品').grid(row=0, column=0)
        self.tree2.grid(row=1, column=0)
        self.ysb2.grid(row=1, column=1, sticky="ns")

    def init_options(self):
        for i, item in enumerate(self.part2):
            Label(self.frame2, width=20, text=item[0]).grid(row=i+3, column=1)
            Button(self.frame2, width=8, text=item[1], command=item[2]).grid(row=i+3, column=2)

    def clear_content(self):
        selected_item = self.tree2.selection()
        val2 = self.tree2.item(selected_item, 'values')[1]
        for item in self.tree.get_children(''):
            val = self.tree.item(item, 'values')
            if val2 == val[1]:
                self.tree.set(item, column=0, value=val[0].replace(' √', ''))

        self.tree2.delete(selected_item[0])

    def search_item(self, val):
        for item in self.tree.get_children(''):
            val2 = self.tree.item(item, 'values')
            if val == val2[1]:
                return item

    def rep_pro(self):
        item_text = self.sorted_data()

        x = self.tree2.get_children()
        repeat = False
        for item in x:
            values = self.tree2.item(item, 'values')
            if values[1] == item_text[1]:
                repeat = True
        if not repeat:
            self.tree2.insert('', 'end', values=item_text)

    def add_pro(self):
        item = self.sorted_data()
        print(item)

    def del_pro(self):
            for item in self.tree.selection():
                item_text = self.tree.item(item, 'values')
            selected_item = self.tree.selection()[0]
            if messagebox.askyesno('正在删除', '请确认是否删除：%s' % item_text[1]):
                self.tree.delete(selected_item)
                conn = sqlite3.connect('py_sqlite.db')
                print(item_text[0])
                conn.execute("delete from product where sku=?", (item_text[0],))
                conn.commit()
                conn.close()

    def sorted_data(self):
        """
        self.column = ['SKU', '产品名称', '长', '宽', '高', '重量', '总库存', '谷仓库存', '万邑通库存', '日销量', '上次补货时间']
                self.column2 = ['SKU', '产品名称', '体积', '重量', '总库存', '谷仓库存', '万邑通库存', '日销量', '上次补货时间', '补货数量']
        """
        for item in self.tree.selection():
            print(item)
            item_text = self.tree.item(item, 'values')
            if '√' not in item_text[0]:
                self.tree.set(item, column=0, value=item_text[0] + ' √')
        res = []
        v = round(float(item_text[3]) * float(item_text[4]) * float(item_text[2]))
        res.extend(item_text[:2])
        res.append(v)
        res.extend(item_text[5:])
        return res

    def rec_rep(self, total_v=67*10**6):

        sales_list = []
        volumn_list = []
        all_stock = []
        for item in self.tree2.get_children(''):
            x = self.tree2.item(item, 'values')
            sales_list.append(float(x[7]))
            volumn_list.append(x[2])
            all_stock.append(int(x[4]))
        sales_percent = list(map(lambda y: round(y/sum(sales_list), 2), sales_list))
        volumn_share = list(map(lambda i, j: float(i)*float(j), sales_percent, volumn_list))
        card_num = total_v/sum(volumn_share)
        rep_num = list(map(lambda i: round(float(i)*card_num), sales_percent))
        print(card_num)
        print(rep_num)
        for i, item in enumerate(self.tree2.get_children('')):
            self.tree2.set(item, column=9, value=rep_num[i])
        def time_left(all_stock, rep_num, sales):
            rec_time = 15
            ship_time = 50
            t1 = all_stock/sales
            t2 = rep_num/sales
            if t2 < rec_time:
                sale_time = rec_time + ship_time + t2
            else:
                sale_time = t1 + t2
            return round(sale_time)
        left_time = map(lambda i, j, k: time_left(i, j, k), all_stock, rep_num, sales_list)
        print(list(left_time))

    def tv_sort_col(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            l.sort(key=lambda x: float(x[0]), reverse=reverse)
        except:
            l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tv_sort_col(tv, col, not reverse))

class Model:
    def __init__(self, master):
        self.master = master
        self.db_name = 'py_sqlite.db'
        self.db_table = 'product'
        # self.master.tree.bind('<Double-1>', self.choose_cell_value)
        # self.master.tree2.bind('<Double-1>', self.choose_cell_value)

    def show_all(self):

        conn = sqlite3.connect(self.db_name)
        res = conn.execute("select * from %s" % self.db_table)

        for i, item in enumerate(res):
            item = list(item)
            if not item[8]:
                item[8] = 0
            item.insert(7, item[7])
            if not item[-1]:
                item[-1] = ''
            self.master.tree.insert('', 'end', values=item[1:])
            Button(self.master.frame, text='点击补货', width=8)
        conn.close()


    def choose_cell_value(self, event):
        for item in self.master.tree.selection():
            print(item)
            item_text = self.master.tree.item(item, "values")
            print(item_text)
            self.master.tree2.insert('', 'end', values=item_text)
        column = self.master.tree.identify_column(event.x)
        row = self.master.tree.identify_row(event.y)
        cn = int(str(column).replace('#', ''), 16)
        rn = int(str(row).replace('I', ''), 16)

    def data_sort(self):
        conn = sqlite3.connect(self.db_name)
        res = conn.execute("select * from %s" % self.db_table)
        sorted_data = []
        for item in res:
            item = list(item)
            if not item[8] or not isinstance(item[8], int):
                item[8] = 0
            if not isinstance(item[7], int):
                item[7] = 0
                item[8] = 0
            if not item[-1]:
                item[-1] = ''
            temp_data = []
            temp_data.extend(item[:3])
            lwh = item[3: 6]
            v = self.caculate_volumn(lwh)
            temp_data.append(v)
            temp_data.append(item[6])
            temp_data.append(item[7]+item[8])
            temp_data.extend(item[7:])
            sorted_data.append(temp_data)
        return sorted_data

    @staticmethod
    def caculate_volumn(lwh):
        l, w, h = lwh
        if not l or not w or not h:
            return 0
        return int(l) * int(w) * int(h)


class Option(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title('添加产品')
        self.geometry('770x100+500+500')
        self.wm_attributes('-topmost', 1)
        self.db_name = 'py_sqlite.db'
        self.conn = sqlite3.connect(self.db_name)
        self.frame = Frame(self)
        self.info = ['SKU', '产品名称', '长', '宽', '高', '重量', '谷仓库存', '万邑通库存', '日销量', '上次补货时间']
        self.entrys = []
        self.res = []
        self.init_ui()
        Button(self.frame, text="录入", command=self.save_quit).grid(row=2, column=4)
        Button(self.frame, text="取消", command=self.quit_window).grid(row=2, column=5)
        self.frame.grid()

    def init_ui(self):
        for i, item in enumerate(self.info):
            Label(self.frame, text=item, width=10).grid(row=0, column=i)
            entry = Entry(self.frame, width=10)
            self.entrys.append(entry)
            entry.grid(row=1, column=i)

    def save_quit(self):
        for entry in self.entrys:
            content = entry.get()
            self.res.append(content.strip())
        self.res.insert(7, self.res[7])
        self.destroy()

    def quit_window(self):
        self.destroy()


class Tkshoot(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.geometry('1100x900+200+100')

        self.title('补货计划')
        self.resizable(width=False, height=False)
        self.protocol('WM_DELETE_WINDOW', self.del_pic)

    def add_product(self):
        progress = Option()
        self.wait_window(progress)
        progress.conn.execute("insert into product (sku, name, length, width, height, weight, in_stock_left_1, in_stock_left_2, daily_sale, last_time_rep_date) values (?,?,?,?,?,?,?,?,?,?)", progress.res[1:])
        progress.conn.commit()
        progress.conn.close()
        return progress.res[1:]


    def del_pic(self):
        if messagebox.askyesno('想好了嘛?', '真的要退出嘛?'):
            self.destroy()


root = Tkshoot()

window = View(root)
control = Model(window)
control.show_all()
root.mainloop()