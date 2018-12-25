# from tkinter import ttk
# from tkinter import *
#
# root = Tk()  # 初始框的声明
# columns = ("姓名", "IP地址")
# treeview = ttk.Treeview(root, height=18, show="headings", columns=columns)  # 表格
#
# treeview.column("姓名", width=100, anchor='center')  # 表示列,不显示
# treeview.column("IP地址", width=300, anchor='center')
#
# treeview.heading("姓名", text="姓名")  # 显示表头
# treeview.heading("IP地址", text="IP地址")
#
# treeview.pack(side=LEFT, fill=BOTH)
#
# name = ['电脑1', '服务器', '笔记本']
# ipcode = ['10.13.71.223', '10.25.61.186', '10.25.11.163']
# for i in range(min(len(name), len(ipcode))):  # 写入数据
#     treeview.insert('', i, values=(name[i], ipcode[i]))
#
#
def treeview_sort_column(tv, col, reverse):  # Treeview、列名、排列方式
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)  # 排序方式
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):  # 根据排序后索引移动
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
#
#
# def set_cell_value(event):  # 双击进入编辑状态
#     for item in treeview.selection():
#         # item = I001
#         item_text = treeview.item(item, "values")
#         # print(item_text[0:2])  # 输出所选行的值
#     column = treeview.identify_column(event.x)  # 列
#     row = treeview.identify_row(event.y)  # 行
#     cn = int(str(column).replace('#', ''))
#     rn = int(str(row).replace('I', ''))
#     entryedit = Text(root, width=10 + (cn - 1) * 16, height=1)
#     entryedit.place(x=16 + (cn - 1) * 130, y=6 + rn * 20)
#
#     def saveedit():
#         treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
#         entryedit.destroy()
#         okb.destroy()
#
#     okb = ttk.Button(root, text='OK', width=4, command=saveedit)
#     okb.place(x=90 + (cn - 1) * 242, y=2 + rn * 20)
#
#
# def newrow():
#     name.append('待命名')
#     ipcode.append('IP')
#     treeview.insert('', len(name) - 1, values=(name[len(name) - 1], ipcode[len(name) - 1]))
#     treeview.update()
#     newb.place(x=120, y=(len(name) - 1) * 20 + 45)
#     newb.update()
#
#
# treeview.bind('<Double-1>', set_cell_value)  # 双击左键进入编辑
# newb = ttk.Button(root, text='新建联系人', width=20, command=newrow)
# newb.place(x=120, y=(len(name) - 1) * 20 + 45)
#
# for col in columns:  # 绑定函数，使表头可排序
#     treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeview, _col, False))
# '''
# 1.遍历表格
# t = treeview.get_children()
# for i in t:
#     print(treeview.item(i,'values'))
# 2.绑定单击离开事件
# def treeviewClick(event):  # 单击
#     for item in tree.selection():
#         item_text = tree.item(item, "values")
#         print(item_text[0:2])  # 输出所选行的第一列的值
# tree.bind('<ButtonRelease-1>', treeviewClick)
# ------------------------------
# 鼠标左键单击按下1/Button-1/ButtonPress-1 
# 鼠标左键单击松开ButtonRelease-1 
# 鼠标右键单击3 
# 鼠标左键双击Double-1/Double-Button-1 
# 鼠标右键双击Double-3 
# 鼠标滚轮单击2 
# 鼠标滚轮双击Double-2 
# 鼠标移动B1-Motion 
# 鼠标移动到区域Enter 
# 鼠标离开区域Leave 
# 获得键盘焦点FocusIn 
# 失去键盘焦点FocusOut 
# 键盘事件Key 
# 回车键Return 
# 控件尺寸变Configure
# ------------------------------
# '''
#
# root.mainloop()  # 进入消息循环
#
# import tkinter
# import tkinter.ttk
# import os
#
#
# class TreeWindows:
#     def __init__(self):
#         self.win = tkinter.Tk()
#         self.tree = tkinter.ttk.Treeview(self.win, height=500)  # 树状
#         self.ysb = tkinter.ttk.Scrollbar(self.win, orient="vertical", command=self.tree.yview())  # y滚动条
#         self.xsb = tkinter.ttk.Scrollbar(self.win, orient="horizontal", command=self.tree.xview())  # x滚动条
#         self.tree.configure(yscroll=self.ysb.set, xscroll=self.xsb.set)  # y滚动条关联
#         self.tree.grid(row=0, column=0)
#         self.tree.heading("#0", text="Path", anchor="w")  # 初始化头部,表头 west靠近西方
#         self.tree.bind("<<TreeviewSelect>>", self.gosel)  # 事件(选中)绑定
#
#         filepath = "C:\\aa\\Desktop"  # 路径
#         root = self.tree.insert("", "end", text=filepath, open=True)  # 插入一个节点
#         self.loadtree(root, filepath)  # 递归
#
#         self.e = tkinter.StringVar()
#         self.entry = tkinter.Entry(self.win, textvariable=self.e)
#         self.e.set("请选择文件")
#         self.entry.grid(row=0, column=2)
#
#         self.ysb.grid(row=0, column=1, sticky="ns")
#         self.xsb.grid(row=1, column=0, sticky="ew")
#         self.win.grid()  # 表格展示
#
#     def loadtree(self, parent, rootpath):
#         for path in os.listdir(rootpath):  # 遍历当前目录
#             abspath = os.path.join(rootpath, path)  # 连接成绝对路径
#             oid = self.tree.insert(parent, 'end', text=abspath, open=False)  # 插入树枝
#             if os.path.isdir(abspath):
#                 self.loadtree(oid, abspath)  # 递归回去
#
#     def gosel(self, event):
#         self.select = event.widget.selection()  # 获取所选的项(可能是多项，所以要for循环)
#         for idx in self.select:
#             print(self.tree.item(idx)["text"])
#             self.e.set(self.tree.item(idx)["text"])
#
#     def show(self):
#         self.win.mainloop()
#
#
# mytree = TreeWindows()
# mytree.show()


#
# import tkinter as tk
# from tkinter import ttk
#
# root = tk.Tk()
#
# tree = ttk.Treeview(root)
#
# tree["columns"]=("one","two")
# tree.column("one", width=100 )
# tree.column("two", width=100)
# tree.heading("one", text="coulmn A")
# tree.heading("two", text="column B")
#
# tree.insert("" , 0, text="Line 1", values=("1A","1b"))
#
# apple = tree.insert("", 1, text="DDDDD")
# tree.insert(apple, "end", text="ddddd", values=("2A", "2B"))
#
# ##alternatively:
# tree.insert("", 2, "dir3", text="test")
# tree.insert("dir3", "end", text=" kkkkk",values=("3A", "3B"))
#
# tree.pack()
# e=tk.Entry(root,show=None)
# e.pack()
#
# e1=tk.Entry(root,show=None)
# e1.pack()
#
# e2=tk.Entry(root,show=None)
# e2.pack()
#
#
# def add():
#         var=e.get()
#         var1=e1.get()
#         var2=e2.get()
#         tree.insert("","end",text=var,values=(var1,var2))
#         e.delete(0,'end')
#         e1.delete(0,'end')
#         e2.delete(0,'end')
#
# b1=tk.Button(root,text='add',width=15,command=add)
# b1.pack()
#
#
# def delete():
#         selected_item = tree.selection()[0] ## get selected item
#         tree.delete(selected_item)
#
#
# b2=tk.Button(root,text='delete',width=15,command=delete)
# b2.pack()
# root.mainloop()


a = '12.14销控表（新品）.xlsx'