#---------------------------------------------------------------------
# tigerfriend.py
#---------------------------------------------------------------------

from html import escape
from flask import Flask, request, make_response, redirect, url_for, render_template

#---------------------------------------------------------------------

app = Flask(__name__)

#---------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

#---------------------------------------------------------------------

@app.route('/page2', methods=['GET'])
def page2():
    return render_template('page2.html')

#---------------------------------------------------------------------

@app.route('/page3', methods=['GET'])
def page3():
    return render_template('page3.html')

#---------------------------------------------------------------------

@app.route('/page4', methods=['GET'])
def page4():
    return render_template('page4.html')

#---------------------------------------------------------------------

if __name__ == '__main__':
   app.run(debug=True)