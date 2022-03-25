#---------------------------------------------------------------------
# tigerfriend.py
#---------------------------------------------------------------------

from flask import Flask, request, make_response, redirect, url_for, render_template
from RawData_SQL import api_account_creation, get_user_data, account_creation
from keys import APP_SECRET_KEY
from req_lib import getOneUndergrad

#---------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')

app.secret_key = APP_SECRET_KEY

import auth

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
    user = auth.authenticate().strip()

    # Should do this only first time (currently it does it every time)
    # Eventually move this code + inputting bio and username to end of
    #survey, so only users who do survey get an account made
    req = getOneUndergrad(netid=user)
    if req.ok:
        print(req.json())
        api_account_creation(user, 
                        '20' + str(req.json()['class_year']), 
                        req.json()['major_code'],
                        req.json()['res_college'])
    else:
        print(req.text)
    

    html = render_template('survey.html')
    response = make_response(html)
    return response

#---------------------------------------------------------------------

@app.route('/matches', methods=['GET'])
def page3():
    user = auth.authenticate().strip()

    print(user)
    data = get_user_data(user)
    print(data)
    html = render_template('matches.html',
                            net_id = user,
                            year = data[0],
                            major = data[1])
    response = make_response(html)
    return response

#---------------------------------------------------------------------

@app.route('/chat', methods=['GET'])
def page4():
    user = auth.authenticate().strip()

    html = render_template('chat.html')
    response = make_response(html)
    return response

#---------------------------------------------------------------------

@app.route('/about', methods=['GET'])
def page5():
    user = auth.authenticate().strip()

    html = render_template('about.html')
    response = make_response(html)
    return response

#---------------------------------------------------------------------


@app.route('/data', methods=['GET'])
@app.route('/gatherdata', methods=['GET'])
def page6():
    user = auth.authenticate().strip()

    # getting the input data for the query
    net_id = None
    class_year = None
    res_college = None
    major = None
    bio = None
    if (net_id is None and class_year is None and
        res_college is None and major is None and
        bio is None):
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
    print("Gathered Data:")
    print(net_id, class_year, major)
    # input the data to the database
    if net_id != '':
        print("creating")
        account_creation(net_id, class_year, major)

    html = render_template('data.html')
    response = make_response(html)
    return response