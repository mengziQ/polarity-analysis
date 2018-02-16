from flask import Blueprint, request, url_for, render_template, redirect
import re
import MeCab
import pickle
import os
import numpy as np
import math
from datetime import datetime

bp = Blueprint('web_app', __name__)

def wakati(strings):
  before_wakati = strings
  m = MeCab.Tagger('-Owakati')

  sentence = m.parse(strings).strip()
  
  status = 0

  #if len(sentence) > 140:
   # status = -1
  #else:
   # status = 0
  
  emojis = re.findall(r'[\U0001F600-\U0001F64F|\U0001F300-\U0001F5FF|\U0001F680-\U0001F6FF|\U0001F1E0-\U0001F1FF]', sentence)

  for e in emojis:
    sentence = sentence.replace(e, '') 

  for e in emojis:
    sentence += ' %s '%e

    sentence = re.sub(r'\s{1,}', ' ', sentence)
  
  return before_wakati, sentence, status
  

def culc_polarity(before_wakati, sentence):

  # ファイルパス要確認★
  with open('/home/ubuntu/repos/Tech-Tools/polarity-analysis/web_app/blueprints/term_id.pkl', 'rb') as i_pkl:
    loaded_pkl = pickle.load(i_pkl)
 
  # print('iter', en, '/', length)
  try:
    #print(sentence)
    term = sentence.split()
    #print(term)

  except Exception as e:
    # 変な文章が入力された場合の例外処理考える必要がある
    return -1, e

  # logファイル出力用
  log_name = '/home/ubuntu/repos/Tech-Tools/polarity-analysis/web_app/logs/' + datetime.now().strftime('%Y-%m-%d %H:%M:%S').replace(' ','') + '.txt'
  with open(log_name, 'w') as log:
    # ファイルパス要確認★
    with open('/home/ubuntu/repos/Tech-Tools/polarity-analysis/web_app/blueprints/tweet_train.svm.fmt.model', 'r') as model:
      weights = []
      models = model.readlines()
    
      for idx, m in enumerate(models):
        if idx > 5:
          weights.append(m)

      term_w = {}
      i = 0
      term_freq = {}
      exist_flg = 0

      for tm, values in sorted(loaded_pkl.items(), key=lambda x:x[1]):
        term_freq[tm] = term.count(tm)
        term_w[tm] = float(weights[i])

        if term.count(tm) > 0:
          print(tm, ' が辞書にあった')
          log.write(tm + ' が辞書にあった\n')
          exist_flg = 1
          print('重さは', term_w[tm])
          log.write('重さは '+ str(term_w[tm]) + '\n')

        i += 1

    sum_list = []

    for term, count in term_freq.items():
      w = term_w[term]
      sum_list.append(w * math.log(count + 1))

    if exist_flg == 0:
      polarity = -1
      result = -1
    else:
      svm_func = sum(sum_list) 
      print(svm_func)
      log.write(str(svm_func) + '\n')

      result = 1 / (1 + math.exp(-1 * svm_func))

      if result < 0.5:
        polarity = 0
      else:
        polarity = 1

      result = int(result * 100)

    return  before_wakati, polarity, result
  

# htmlの方のaction属性のurl_forでメソッド名を指定する
@bp.route('/judge', methods=['POST'])
def polarity_analysis():
  sentence = request.form['sentence']
  origin, wakati_str, status = wakati(sentence)
  title = "文章のポジティブ度判定サイト"

  if status == -1:
    return render_template('top_page.html', title=title, origin=origin, status=status)
  
  origin, polarity, result = culc_polarity(origin, wakati_str)
  print('culc_polarity完了')

  if request.method == 'POST':
    print('POSTに振り分け')
    print(polarity)
    # 結果画像と結果文章と元の文章を引数に持たせる　セッションとか使ったほうがいいのかな？フォームの入力値を維持する
    return render_template('top_page.html',polarity=polarity, title=title, origin=origin, result=result, status=status)
  

  return redirect(url_for('top_page'))


