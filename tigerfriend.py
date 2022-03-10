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