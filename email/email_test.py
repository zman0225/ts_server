#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-28 10:59:23
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-28 15:09:15

import requests


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v2/sandbox38140.mailgun.org/messages",
        auth=("api", "key-2fjxk5t4qzhztrjhawsgx9l-ygndo019"),
        files=[('inline',open('images/header-top.gif')),('inline',open('images/header-bottom.gif')),
        	('inline',open('images/main-image.gif')),('inline',open('images/bg.jpg'))],
        data={"from": "Mailgun Sandbox <postmaster@sandbox38140.mailgun.org>",
              "to": "solomon <Solomonrajput1@gmail.com>",
              "subject": "Hello ziyuan",
              "html": open('template-2.html')})
if __name__ == '__main__':
	r=send_simple_message()
	print r.status_code


