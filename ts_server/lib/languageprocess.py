#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-03-16 14:52:02
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-03-16 16:16:04
from nltk.tag import pos_tag

def get_nouns(phrase):
	tagged_sent = pos_tag(phrase.lower().split())
	nouns = [word for word,pos in tagged_sent if pos == 'NNP' or pos =='N' or pos =='NNS' or pos=='NN']
	return ' '.join(nouns)


