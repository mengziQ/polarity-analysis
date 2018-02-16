from flask import Blueprint, request, redirect, url_for, render_template
from term_id import term_id
import re
import MeCab
import glob

def wakati():
  error = None
  
  if request.method == 'POST':
    m = MeCab.Tagger('-Owakati')
    sentence = request.form['sentence']
    sentence = m.parse(sentence).strip()
    emojis = re.findall(r'[\U0001F600-\U0001F64F|\U0001F300-\U0001F5FF|\U0001F680-\U0001F6FF|\U0001F1E0-\U0001F1FF]', sentence)

    for e in emojis:
      sentence = sentence.replace(e, '') 

    for e in emojis:
      sentence += ' %s '%e

    sentence = re.sub(r'\s{1,}', ' ', sentence)
    nico = '😃'
    namida = '😢'
    
    # ここからterm_id呼び出し処理
    if nico in sentences:
      file_name = name.replace('posi-nega-twt','posi-nega-twt-wakati')
      file_name = file_name.replace('_p.txt', '_p_wakati.txt')
      f = open(file_name, 'w')
    elif namida in tweet:
      file_name = name.replace('posi-nega-twt','posi-nega-twt-wakati')                     
      file_name = file_name.replace('_n.txt', '_n_wakati.txt')                                  
      f = open(file_name, 'w')
    else:
      continue
  
    tweet = tweet.replace(nico, '')
    tweet = tweet.replace(namida, '')
    tweet = re.sub(r'\s{1,}', ' ', tweet)
    f.write(tweet)


def term_id(sentence, polarity):
  term_id_dic = {}


  


