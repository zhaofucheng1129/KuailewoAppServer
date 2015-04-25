import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html',page = "index")

if __name__ == '__main__':
    app.run(host='115.28.135.119',port=8080)
