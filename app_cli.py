#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import email
import imaplib

PARSER = argparse.ArgumentParser(description='Parse inbox email address in mail.ru')
PARSER.add_argument('-e', help='email address', required=True)
PARSER.add_argument('-p', help='password', required=True)
ARGS = vars(PARSER.parse_args())
EMAIL = ARGS['e']
PASSWORD = ARGS['p']
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


mail = imaplib.IMAP4_SSL('imap.mail.ru')
mail.login(EMAIL, PASSWORD)
mail.select("Inbox")

result, data = mail.uid('search', None, "ALL")
email_uid_list = data[0].split()
email_list = []
counter = 0

for i in email_uid_list:
    try:
        counter += 1
        result, data = mail.uid('fetch', i, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        email_list.append(email.utils.parseaddr(email_message['From'])[1])
        print("Cheking mail: {}/{}".format(counter, len(email_uid_list)), end="\r")
    except TypeError as e:
        print(e)
    except AttributeError as e:
        print(e)

unique_list = UniqueList(email_list)
result_list = CheckBadWords(unique_list)

with open("result/{}.txt".format(EMAIL), 'w', encoding='utf-8') as f:
    for i in result_list:
        f.write(i + '\n')
