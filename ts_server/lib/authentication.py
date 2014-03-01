#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2013-12-07 00:51:32
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-28 23:46:09
########################################################################################################

def constant_time_compare(actual,expected):
	"""
	Returns True if the two strings are equal, False otherwise

	The time taken is dependent on the number of characters provided
	instead of the number of characters that match.
	"""
	actual_len   = len(actual)
	expected_len = len(expected)
	result = actual_len ^ expected_len
	if expected_len > 0:
		for i in xrange(actual_len):
			result |= ord(actual[i]) ^ ord(expected[i % expected_len])
	return result == 0

#TODO
#consider taking the regex qualifications into the client side
import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{6,20}$")
EMAIL_RE=re.compile(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$")

def valid_username(username):
    """
    valids if the username given matches the
    regular expression rule
    """
    return username and USER_RE.match(username)

def valid_password(pw):
    """
    valids if the username given matches the
    regular expression rule
    """
    return pw and PASS_RE.match(pw)

def validate_info(username,password):
    return valid_username(username) and valid_password(password)

def validate_email(email):
    return email and EMAIL_RE.match(email)







