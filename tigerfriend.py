#---------------------------------------------------------------------
# tigerfriend.py
#---------------------------------------------------------------------

from flask import Flask, request, make_response, redirect, url_for, render_template

#---------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')

#---------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    html = render_template('home.html')
    response = make_response(html)
    return response

#---------------------------------------------------------------------

@app.route('/survey', methods=['GET'])
def page2():
    html = render_template('survey.html')
    response = make_response(html)
    return response

#---------------------------------------------------------------------

@app.route('/matches', methods=['GET'])
def page3():
    html = render_template('matches.html')
    response = make_response(html)
    return response

#---------------------------------------------------------------------

@app.route('/chat', methods=['GET'])
def page4():
    html = render_template('chat.html')
    response = make_response(html)
    return response
