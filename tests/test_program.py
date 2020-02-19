#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from pathlib import Path

import function


class TestFileBadwords(unittest.TestCase):
    def setUp(self):
        self.badwords_file = Path(Path.cwd(), "badwords.txt")

    def test_badwords_file_exist(self):
        self.assertTrue(self.badwords_file.exists())

    def test_badwords_file_not_null(self):
        with open(self.badwords_file) as self.f:
            self.num = sum(1 for self._ in self.f)
        self.assertTrue(self.num > 0)


class TestDirectoryResult(unittest.TestCase):
    def setUp(self):
        self.result_dir = Path(Path.cwd(), "result")

    def test_result_dir_exist(self):
        self.assertTrue(self.result_dir.is_dir())


class TestRunFunction(unittest.TestCase):
    def test_unique_list_function(self):
        self.test_list = ['one', 'two', 'five', 'six', 'one', 'six']
        self.result_address_list = function.UniqueList(self.test_list)
        self.assertTrue(len(self.result_address_list) == 4)

    def test_check_badwords_function(self):
        self.test_address_list = ['robot@yandex.ru', 'test@mail.ru', 'admin@vk.com', 'raduga@mail.ru', 'no-reply@gmail.com']
        self.len_test_address_list = len(self.test_address_list)
        self.test_address_list = function.CheckBadWords(self.test_address_list)
        self.assertNotEqual(self.len_test_address_list, len(self.test_address_list))


class TestCheckingEmail(unittest.TestCase):
    def setUp(self):
        self.test_connection = function.mail_connection()
        self.login = ''
        self.password = ''

    def test_connection(self):
        self.assertIsInstance(self.test_connection, object)

    @unittest.expectedFailure
    def test_auth(self):
        self.connect = function.mail_auth(self.test_connection, self.login, self.password)
        self.assertIsInstance(self.connect, object)

    @unittest.expectedFailure
    def test_get_all_uid(self):
        self.connect = function.mail_auth(self.test_connection, self.login, self.password)
        self.uid_list = function.mail_fetch_all_uid(self.connect)
        self.assertTrue(len(self.uid_list) > 0)

    @unittest.expectedFailure
    def test_mail_parseaddr(self):
        self.connect = function.mail_auth(self.test_connection, self.login, self.password)
        self.uid_list = function.mail_fetch_all_uid(self.connect)
        self.emailaddress = function.mail_parseaddr(self.connect, self.uid_list[0])
        self.assertIsInstance(self.emailaddress, str)


if __name__ == '__main__':
    unittest.main()
