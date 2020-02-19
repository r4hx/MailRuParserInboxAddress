#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter
import tkinter.ttk

import function


def CheckMail(EMAIL, PASSWORD):
    try:
        connect = function.mail_connection()
    except:
        root.title("Нет подключения к серверу IMAP")
        raise ConnectionError("Нет подключения к серверу IMAP")
    try:
        connect = function.mail_auth(connect, EMAIL, PASSWORD)
    except:
        root.title("Неправильный email/пароль")
        raise ConnectionError("Неправильный email/пароль")
    email_uid_list = function.mail_fetch_all_uid(connect)
    email_list = []
    counter = 0
    maximum = len(email_uid_list)
    pbar1["maximum"] = maximum
    for i in email_uid_list:
        try:
            counter += 1
            email_list.append(function.mail_parseaddr(connect, i))
            pbar1["value"] = counter
            root.title("Проверенно: {} из {}".format(counter, maximum))
            root.update()
        except:
            pass

    unique_list = function.UniqueList(email_list)
    result_list = function.CheckBadWords(unique_list)

    with open("result/{}.txt".format(EMAIL), 'w', encoding='utf-8') as f:
        for i in result_list:
            f.write(i + '\n')
    root.title("Результат в папке с программой".format(EMAIL))
    btn1["text"] = "Начать"
    root.update()


def btn1_click():
    btn1["text"] = "Идет поиск"
    email = ent1.get()
    password = ent2.get()
    CheckMail(email, password)


root = tkinter.Tk()
root.title("email address parser")
root.geometry("400x150")
root.resizable(width=False, height=False)
lbl1 = tkinter.Label(text="Ваш email")
lbl1.pack()
ent1 = tkinter.Entry()
ent1.pack()
lbl2 = tkinter.Label(text="Ваш пароль")
lbl2.pack()
ent2 = tkinter.Entry(show="*")
ent2.pack()
pbar1 = tkinter.ttk.Progressbar(orient="horizontal", mode="determinate", length=200)
pbar1.pack()
btn1 = tkinter.Button(text="Начать", command=btn1_click)
btn1.pack()
root.mainloop()
