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
    # commented out because the server not working
    net_id = request.cookies.get('prev_net_id')
    print(net_id)
    if net_id is not None:
        year = get_user_year("net_id")
    else:
        year = get_user_year("testing123")
    html = render_template('matches.html',
                            net_id = net_id,
                            year = year)
    #html = render_template('matches.html', year = "2000, database not working")
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
@app.route('/gatherdata', methods=['GET'])
def page5():
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
    response.set_cookie('prev_net_id', net_id)
    return response