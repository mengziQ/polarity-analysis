import pickle
import glob
import math

def main():
  with open('term_id.pkl', 'rb') as i_pkl:
    loaded_pkl = pickle.load(i_pkl)

  f_svm = open('tweet.svm', 'w')

  files = glob.glob('/home/ubuntu/posi-nega-twt-wakati/*')
  length = len(files)
  for en, name in enumerate(files):
    print('iter', en, '/', length)
    try:
      f_wakati = open(name, 'r')
      tweet = f_wakati.read()
      term = tweet.split()

    except Exception as e:
      print(e)
      continue

    if '_p_' in name:
      freqs = '1' + ' '
    else:
      freqs = '0' + ' '

    for tm, id_num in sorted(loaded_pkl.items(), key=lambda x:x[1]):
      count = term.count(tm)
      log_cnt = math.log(count + 1.0)
      freqs += str(id_num) + ':' + str(log_cnt) + ' '
  
    freqs = freqs.strip()
    f_svm.write(freqs + '\n')


if __name__ == '__main__':
  main()


