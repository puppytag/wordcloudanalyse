#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter
import tkinter.ttk
from tkinter import filedialog
import re
import jieba
jieba.setLogLevel(jieba.logging.INFO)
import numpy as np
from wordcloud import WordCloud
from PIL import Image
import traceback
import os

#创建主页面
root = tkinter.Tk()
root.title("词云分析")
root.geometry("550x450")

notebook = tkinter.ttk.Notebook(root)

frameOne = tkinter.Frame()
frameTwo = tkinter.Frame()
font=os.path.join(os.getcwd(), "font","SourceHanSerifCN-Heavy-4.otf")
picture=os.path.join(os.getcwd(), "images","heart.png")
color="Oranges"
source=" "

# 添加内容
textLf1 = tkinter.StringVar(value = "请输入待分析的源文本：" )
tkinter.Label(frameOne, textvariable=textLf1, height=0, width=20).place(x=5,y=10)
textLf2 = tkinter.StringVar(value = "或" )
tkinter.Label(frameOne, textvariable=textLf2, height=0, width=20).place(x=50,y=160)
textLf3 = tkinter.StringVar(value = "词云图形状：" )
tkinter.Label(frameOne, textvariable=textLf3, height=0, width=20).place(x=-35,y=250)
textLf4 = tkinter.StringVar(value = "词云图配色：" )
tkinter.Label(frameOne, textvariable=textLf4, height=0, width=20).place(x=-35,y=300)
textLf5 = tkinter.StringVar(value = "词云图字体：" )
tkinter.Label(frameOne, textvariable=textLf5, height=0, width=20).place(x=-35,y=350)
textLf6 = tkinter.StringVar(value = "输出文件命名：" )
tkinter.Label(frameOne, textvariable=textLf6, height=0, width=20).place(x=280,y=250)

combobox0 = tkinter.ttk.Combobox(frameOne, state='readonly')
combobox0['value'] = ("爱心", "聊天气泡", "圆" , "五角星")
combobox0.current(0) # 默认显示第一个选项
combobox0.place(x=80,y=250)
combobox1 = tkinter.ttk.Combobox(frameOne, state='readonly')
combobox1['value'] = ("暖色调", "冷色调", "彩虹色")
combobox1.current(0)
combobox1.place(x=80,y=300)
combobox2 = tkinter.ttk.Combobox(frameOne, state='readonly')
combobox2['value'] = ("思源宋体（重）", "思源宋体（轻）")
combobox2.current(0)
combobox2.place(x=80,y=350)
name = tkinter.Text(frameOne, height=1, width=15)
name.place(x=400,y=253)

def GetShape():
    global picture
    if combobox0.get()=='爱心':
        picture=os.path.join(os.getcwd(), "images","heart.png")
    if combobox0.get()=='聊天气泡':
        picture=os.path.join(os.getcwd(), "images","chat.png")
    if combobox0.get()=='圆':
        picture=os.path.join(os.getcwd(), "images","circle.png")
    if combobox0.get()=='五角星':
        picture=os.path.join(os.getcwd(), "images","star.png")
def GetColor():
    global color
    if combobox1.get()=='暖色调':
        color="Oranges"
    if combobox1.get()=='冷色调':
        color="Blues"
    if combobox1.get()=='彩虹色':
        color="rainbow"
def GetFont():
    global font
    if combobox2.get()=='思源宋体（重）':
        font=os.path.join(os.getcwd(), "font","SourceHanSerifCN-Heavy-4.otf")
    if combobox2.get()=='思源宋体（轻）':
        font=os.path.join(os.getcwd(), "font","SourceHanSerifCN-Light-5.otf")
def Start(): 
    GetShape()
    GetColor()
    GetFont()
    if text.get("1.0", "end-1c")=="":
        with open(file_path.get(), 'r', encoding='utf-8') as f:
            source = f.read()
    else:
        source = text.get("1.0", "end-1c")
    # 使用正则表达式匹配非中文字符
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    source = re.sub(pattern, '', source)

    # 加载停用词列表
    stopwords = []
    with open('stopwords_hit.txt', 'r', encoding='utf-8') as f:
        for line in f:
            stopwords.append(line.strip())

    # 对文本进行分词
    words = jieba.cut(source)

    # 去除停用词
    words = [word for word in jieba.cut(source) if word not in stopwords_hit]

    # 将分词结果转换为列表
    words_list = list(words)

    # 使用空格将分词结果连接成字符串
    result = ' '.join(words_list)

    # 读取形状图片
    mask = np.array(Image.open(picture))

    # 创建 WordCloud 对象，指定中文字体
    wc = WordCloud(font_path=font,background_color='white',colormap=color,mask=mask)

    # 生成词云图
    wc.generate(result)

    # 将词云图保存为图片文件
    target=name.get("1.0","end-1c")+".png"
    wc.to_file(os.path.join(os.getcwd(), "result",target))

text = tkinter.Text(frameOne, height=8, width=60)
text.place(x=5,y=40)

# 创建一个文本变量，并将其与一个 Label 小部件关联
number_text = tkinter.StringVar()
label = tkinter.Label(frameOne, textvariable=number_text)
label.place(x=430,y=90)

# 更新文本变量中的文本，并将其显示在 Label 小部件上
def update_number_text(event):
    text_content = text.get("1.0", "end-1c")
    text_length = len(text_content)
    number_text.set("字数：{}".format(text_length))

text.bind("<KeyRelease>", update_number_text)

file_path = tkinter.StringVar(value = "未选择" )
def open_file_dialog():
    file_path.set(filedialog.askopenfilename())
open_button = tkinter.Button(frameOne, text="选择文件", command=open_file_dialog)
open_button.place(x=250,y=155)

def on_file_path_changed(*args):
    label.config(text="文件地址：" + file_path.get())
file_path.trace("w", on_file_path_changed)
label = tkinter.Label(frameOne, text="文件地址：" + file_path.get())
label.place(x=0,y=190)

textL0=tkinter.StringVar(value = "开始！")
tkinter.Button(frameOne,textvariable=textL0, command=lambda:Start(),width=10,height=2).place(x=410,y=330)

button = tkinter.Button(frameTwo, text='请点击')
button.pack(padx=10, pady=5)

labelOther = tkinter.Label(frameTwo, fg='red')
labelOther.pack(padx=10, pady=5)

notebook.add(frameOne, text='          主页          ')
notebook.add(frameTwo, text='        样式浏览        ')
notebook.pack(padx=10, pady=5, fill=tkinter.BOTH, expand=True)

root.mainloop()


# In[ ]:




