import glob
import pickle


def main():
  
  term_id = {}
  
  for name in glob.glob('/home/ubuntu/posi-nega-twt-wakati/*'):
    try:
      with open(name, 'r') as f:
        tweet = f.read()
        term = tweet.split() 
    except Exception as e:
      print(e)
      continue

    for t in term:
      if term_id.get(t) is None:
        term_id[t] = len(term_id) + 1

    with open('term_id.pkl', 'wb') as t:
      t.write( pickle.dumps(term_id) )


if __name__ == '__main__':
  main()
