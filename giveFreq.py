import glob
import pickle

def main():
  term_freq = {}

  for name in glob.glob('/home/ubuntu/posi-nega-twt-wakati/*'):
    try:
      with open(name, 'r') as f:
        tweet = f.read()
        term = tweet.split() 
    except Exception as e:
      print(e)
      continue

    uni_term = set(term)

    for u in uni_term:
      if term_freq.get(u) is None:
        term_freq[u] += 1

  with open('term_freq.pkl', 'wb') as t:
    t.write(pickle.dumps(term_freq))


if __name__ == '__main__':
  main()


