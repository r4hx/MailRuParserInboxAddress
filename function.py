#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import imaplib
import email


def uniquelist(LIST) -> list:
    seen = set()
    result = []
    for mail in LIST:
        if mail in seen:
            continue
        seen.add(mail)
        result.append(mail)
    LIST = result
    return LIST


def checkbadwords(LIST) -> list:
    BADWORDS = [words.strip() for words in open('badwords.txt').readlines()]
    bad_list = []
    for mail in LIST:
        for word in BADWORDS:
            if word in mail:
                bad_list.append(mail)
                break
    for bad in bad_list:
        LIST.remove(bad)
    return LIST


def mail_connection(server='imap.mail.ru') -> object:
    mail = imaplib.IMAP4_SSL(server)
    return mail


def mail_auth(connect, login, password) -> object:
    connect.login(login, password)
    connect.select("Inbox")
    return connect


def mail_fetch_all_uid(connect) -> list:
    result, data = connect.uid('search', None, "ALL")
    email_uid_list = data[0].split()
    return email_uid_list


def mail_parseaddr(connect, i) -> str:
    result, data = connect.uid('fetch', i, '(RFC822)')
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)
    return email.utils.parseaddr(email_message['From'])[1]
