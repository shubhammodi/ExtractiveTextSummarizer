# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 23:27:05 2020

@author: MODIS1
"""

import summarizer

def test_preprocessing_text():
    clean_text = summarizer.preprocessing_text('[479]   The ""tesT')
    assert clean_text == ' the test'
    
def test_word2count_score():
    word2count = summarizer.word2count_score('[479]   The ""tesT')
    assert word2count.get("test") != None
    
