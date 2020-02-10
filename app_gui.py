#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import *
import email
import imaplib

BADWORDS = [words.strip() for words in open('badwords.txt').readlines()]


def UniqueList(LIST):
    seen = set()
    result = []
    for mail in LIST:
        if mail in seen:
            continue
        seen.add(mail)
        result.append(mail)
    LIST = result
    return LIST


def CheckBadWords(LIST):
    bad_list = []
    for mail in LIST:
        for word in BADWORDS:
            if word in mail:
                bad_list.append(mail)
                break
    for bad in bad_list:
        LIST.remove(bad)
    return LIST


def CheckMail(EMAIL, PASSWORD):
    try:
        mail = imaplib.IMAP4_SSL('imap.mail.ru')
        mail.login(EMAIL, PASSWORD)
        mail.select("Inbox")
    except (imaplib.IMAP4.error):
        root.title("Неправильный email/пароль")

    result, data = mail.uid('search', None, "ALL")
    email_uid_list = data[0].split()
    email_list = []
    counter = 0
    maximum = len(email_uid_list)
    pbar1["maximum"] = maximum
    for i in email_uid_list:
        try:
            counter += 1
            result, data = mail.uid('fetch', i, '(RFC822)')
            raw_email = data[0][1]
            email_message = email.message_from_bytes(raw_email)
            email_list.append(email.utils.parseaddr(email_message['From'])[1])
            pbar1["value"] = counter
            root.title("Проверенно: {} из {}".format(counter, maximum))
            root.update()
        except:
            pass

    unique_list = UniqueList(email_list)
    result_list = CheckBadWords(unique_list)

    with open("{}.txt".format(EMAIL), 'w', encoding='utf-8') as f:
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

root = Tk()
root.title("email address parser")
root.geometry("400x150")
root.resizable(width=False, height=False)
lbl1 = Label(text="Ваш email")
lbl1.pack()
ent1 = Entry()
ent1.pack()
lbl2 = Label(text="Ваш пароль")
lbl2.pack()
ent2 = Entry(show="*")
ent2.pack()
pbar1 = Progressbar(orient="horizontal", mode="determinate", length=200)
pbar1.pack()
btn1 = Button(text="Начать", command=btn1_click)
btn1.pack()
root.mainloop()
