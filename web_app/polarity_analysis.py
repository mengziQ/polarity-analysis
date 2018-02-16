from flask import Flask, render_template, request, redirect, url_for
# import_stringが動かなくなったのでコメントアウト
#from werkzeug.utils import find_modules, import_string 
# Blueprint参考：http://www.yoheim.net/blog.php?q=20160507
from blueprints import judge_sentence

#def register_blueprints(app):
 # for name in find_modules('blueprints'):
  #  mod = import_string(name)
   # if hasattr(mod, 'bp'):
    #  app.register_blueprint(mod.bp)
  #return None

# web_appフォルダ直下で本プログラムを実行する
app = Flask('web_app')

app.register_blueprint(judge_sentence.bp)


@app.route('/')
def top_page():
  title = "自然言語の極性分析ページ"
  return render_template('top_page.html', title=title)
  


@app.route('/post', methods=['GET', 'POST'])
def post():
  # このメソッドいるか謎
  title = "文章のポジティブ判定サイト"
  if request.method == 'POST':
    sentence = request.form['sentence']
    return render_template('top_page.html', sentence=sentence, title=title)
  else:
    # GETでリクエストが来た場合はエラー？
    return redirect(url_for('top_page'))


#@app.route('/display_result', methods=['GET', 'POST'])
#def display_result(polarity, error):
 # title = "自然言語の極性分析ページ"
 # print('display_result開始')
 # if request.method == 'POST':
    # 結果画像と結果文章と元の文章を引数に持たせる　セッションとか使ったほうがいいのかな？フォームの入力値を維持する
  #  return render_template('top_page.html', polarity=polarity, error=error)
 # else:
  #  return redirect(url_for('top_page'))


if __name__ == '__main__':
  app.run(host='ec2-52-69-156-155.ap-northeast-1.compute.amazonaws.com', debug=True)


