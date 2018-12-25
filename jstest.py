# import time, threading
# from tkinter import *
# from tkinter import messagebox
#
# class Interface(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.attrib1 = "Attrib from Interface class"
#
#     def run(self):
#         #Main Window
#         self.mainWindow = Tk()
#         self.mainWindow.geometry("200x200")
#         self.mainWindow.title("My GUI Title")
#         self.mainWindow.protocol("WM_DELETE_WINDOW", self.quit)
#         #Label
#         lbCommand = Label(self.mainWindow, text="Hello world", font=("Courier New", 16)).place(x=20, y=20)
#         #Start
#         self.mainWindow.mainloop()
#
#     #The Interface class contains methods that use attributes from itself and attributes from Process class.
#     def method1(self):
#         print(self.attrib1)
#         print(SecondThread.attrib2)
#
#     def quit(self):
#         if messagebox.askyesno('App','Are you sure you want to quit?'):
#             #In order to use quit function, mainWindow MUST BE an attribute of Interface.
#             self.mainWindow.destroy()
#             self.mainWindow.quit()
#
# class Process(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.attrib2 = "Attrib from Process class"
#
#     def run(self):
#         global finish
#         while not finish:
#             print("Proceso infinito")
#             #Inside the infinite process a method from Interface class is used.
#             GUI.method1()
#             time.sleep(3)
#
# finish = False
# #Starts the GUI
# GUI = Interface()
# GUI.start()
# #Starts the infinity process
# SecondThread = Process()
# SecondThread.start()
# #Waits until GUI is closed
# GUI.join()
# print("When GUI is closed this message appears")
# #When GUI is closed we set finish to True, so SecondThread will be closed.
# finish = True
#
#
# import socket
# from selectors import DefaultSelector, EVENT_WRITE
#
# def fetch(url):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect(('amazon.com', 80))
#     request = 'GET {} HTTP/1.0\r\nHost: amazon.com\r\n\r\n'.format(url)
#     sock.send(request.encode('ascii'))
#     response = b''
#     chunk = sock.recv(4096)
#     while chunk:
#         response += chunk
#         chunk = sock.recv(4096)
#     print(response)
#     print('done')
#
# url = 'https://www.amazon.com'
# fetch(url)

# !/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from printer_pywin32 import PrinterPywin32
import ttk


class PrinterTkinter:
    def __init__(self):
        self.root = Tk()
        self.root.title("打印机监控系统")

        self.frame_left_top = Frame(width=400, height=200)
        self.frame_right_top = Frame(width=400, height=200)
        self.frame_center = Frame(width=800, height=400)
        self.frame_bottom = Frame(width=800, height=50)

        # 定义左上方区域
        self.left_top_title = Label(self.frame_left_top, text="打印状态:", font=('Arial', 25))
        self.left_top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=30)

        self.var_success = StringVar()  # 声明成功数
        self.var_false = StringVar()  # 声明失败数

        self.left_top_frame = Frame(self.frame_left_top)
        self.left_top_frame_left1 = Label(self.frame_left_top, text="打印成功数", font=('Arial', 20))
        self.left_top_frame_left2 = Label(self.frame_left_top, textvariable=self.var_success, font=('Arial', 15))
        self.get_success()  # 调用方法更新成功数
        self.left_top_frame_right1 = Label(self.frame_left_top, text="打印失败数", font=('Arial', 20))
        self.left_top_frame_right2 = Label(self.frame_left_top, textvariable=self.var_false, font=('Arial', 15))
        self.get_false()  # 调用方法更新失败数
        self.left_top_frame_left1.grid(row=1, column=0)
        self.left_top_frame_left2.grid(row=1, column=1)
        self.left_top_frame_right1.grid(row=2, column=0)
        self.left_top_frame_right2.grid(row=2, column=1)

        # 定义右上方区域
        self.var_entry = StringVar()

        self.right_top_title = Label(self.frame_right_top, text="重新打印的任务编号：", font=('Arial', 20))
        self.right_top_entry = Entry(self.frame_right_top, textvariable=self.var_entry)

        self.number = int
        self.right_top_button = Button(self.frame_right_top, text="确定", command=self.button_restart, font=('Arial', 15))
        self.right_top_title.grid(row=0, column=0)
        self.right_top_entry.grid(row=1, column=0)
        self.right_top_button.grid(row=2, column=0, padx=20, pady=20)

        # 定义中心列表区域
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=("a", "b", "c", "d", "e"))
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("a", width=50, anchor="center")
        self.tree.column("b", width=200, anchor="center")
        self.tree.column("c", width=200, anchor="center")
        self.tree.column("d", width=100, anchor="center")
        self.tree.column("e", width=150, anchor="center")
        self.tree.heading("a", text="编号")
        self.tree.heading("b", text="打印时间")
        self.tree.heading("c", text="打印名称")
        self.tree.heading("d", text="打印任务编号")
        self.tree.heading("e", text="打印状态")

        # 调用方法获取表格内容插入
        self.get_tree()
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        # 整体区域定位
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)

        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.root.mainloop()

    # 得到打印成功数
    def get_success(self):
        self.var_success.set(PrinterPywin32.get_success())
        self.left_top_frame_left2.after(500, self.get_success)

    # 得到打印失败数
    def get_false(self):
        self.var_false.set(PrinterPywin32.get_false())
        self.left_top_frame.after(500, self.get_false)

    # 表格内容插入
    def get_tree(self):
        # 删除原节点
        for _ in map(self.tree.delete, self.tree.get_children("")):
            pass
        # 更新插入新节点
        for i in range(len(PrinterPywin32.get_enumjobs())):
            self.tree.insert("", "end", values=(i + 1, PrinterPywin32.get_enumjobs()[i]["Submitted"],
                                                PrinterPywin32.get_enumjobs()[i]["pPrinterName"],
                                                PrinterPywin32.get_enumjobs()[i]["JobId"],
                                                PrinterPywin32.get_enumjobs()[i]["Status"]))
        self.tree.after(500, self.get_tree)

    # 重新打印
    def button_restart(self):
        self.number = self.right_top_entry.get()
        PrinterPywin32.printer_restart(self.number)


if __name__ == '__main__':
    PrinterTkinter()