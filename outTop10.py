import pickle

def main():
  output = open('top10.txt', 'w')
  model = open('tweet_train.svm.fmt.model', 'r')
  termId = open('term_id.pkl', 'rb')
  loaded_termid = pickle.load(termId)

  # モデルファイルから係数を取得
  coefs = []
  cnt = 0
  models = model.readlines()

  for idx, m in enumerate(models):
    if idx > 5:
      coefs.append(m) 

  result = {}
  i = 0

  # termと結合させる
  for term, values in sorted(loaded_termid.items(), key=lambda x:x[1]):
    result[term] = float(coefs[i])
    i += 1
  
  prlt = sorted(result.items(), key=lambda x:x[1], reverse=True)
  nrlt = sorted(result.items(), key=lambda x:x[1])

  output.write('ポジティブワード上位10位  ※順位：ワード（係数）' + '\n')

  for idx, p in enumerate(prlt):
    if idx < 10:
      output.write(str(idx + 1) + '位: ' + p[0] + '（' + str(p[1]) + '）' + '\n')


  output.write('\n' + 'ネガティブワード上位10位　※順位：ワード（係数）' + '\n')
  for idx, n in enumerate(nrlt):
    if idx < 10:
      output.write(str(idx + 1) + '位: ' + n[0] + '（' + str(n[1]) + '）' + '\n')


if __name__ == '__main__':
  main()




