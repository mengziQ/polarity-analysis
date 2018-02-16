import re
import MeCab
import glob


def main():
  m = MeCab.Tagger('-Owakati')

  for name in glob.glob('/home/ubuntu/posi-nega-twt/*'):
    try:
      f = open(name,'r')
    except Exception as e:
      print(e)
      continue

    tweet = f.read()
    tweet = m.parse(tweet).strip()
    emojis = re.findall(r'[\U0001F600-\U0001F64F|\U0001F300-\U0001F5FF|\U0001F680-\U0001F6FF|\U0001F1E0-\U0001F1FF]', tweet)

    for e in emojis:
      tweet = tweet.replace(e, '') 

    for e in emojis:
      tweet += ' %s '%e

    tweet = re.sub(r'\s{1,}', ' ', tweet)
    nico = '😃'
    namida = '😢'
  
    if nico in tweet:
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


if __name__ == '__main__':
  main()


