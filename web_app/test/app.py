from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
  return 'Hello world!'

if __name__ == '__main__':
  app.run(host='ec2-52-68-178-193.ap-northeast-1.compute.amazonaws.com', debug=True)
  
