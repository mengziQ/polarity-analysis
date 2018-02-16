import json 
import glob

def main():
  for name in glob.glob('/home/ubuntu/date/2017-08-03/tweets/*'):
    try:
      obj = json.loads(open(name).read())
    except Exception as e:
      print(e)
      continue
  
    for time, values in obj.items():
      try:
        tweet = values['text']
        username = values['user']['screen_name']
        t_stamp = time

      except Exception as e:
        print(e)
        continue

      if '😃' in tweet:
        f = open('/home/ubuntu/posi-nega-twt/' + username + '_' + t_stamp + '_p.txt', 'w')
      elif '😢' in tweet:
        f = open('/home/ubuntu/posi-nega-twt/' + username + '_' + t_stamp  + '_n.txt', 'w')
      else:
        continue
    
      f.write(tweet)

if __name__ == '__main__':
  main()



