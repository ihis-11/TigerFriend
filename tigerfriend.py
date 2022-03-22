#---------------------------------------------------------------------
# tigerfriend.py
#---------------------------------------------------------------------

from flask import Flask, request, make_response, redirect, url_for, render_template
from RawData_SQL import account_creation, get_user_year

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
    html = render_template('matches.html', year = get_user_year('testNet1'))
    response = make_response(html)
    return response

#---------------------------------------------------------------------

@app.route('/chat', methods=['GET'])
def page4():
    html = render_template('chat.html')
    response = make_response(html)
    return response

#---------------------------------------------------------------------

@app.route('/data', methods=['GET'])
def page5():
    # getting the input data for the query
    net_id = request.args.get('net_id')
    class_year = request.args.get('class_year')
    res_college = request.args.get('res_college')
    major = request.args.get('major')
    bio = request.args.get('bio')

    if net_id is None:
        net_id = ''
    if class_year is None:
        class_year = ''
    if major is None:
        major = ''
    if bio is None:
        bio = ''
    if res_college is None:
        res_college = ''
    
    # input the data to the database
    if net_id is not '':
        account_creation(net_id, class_year, major)

    html = render_template('data.html')
    response = make_response(html)
    return response