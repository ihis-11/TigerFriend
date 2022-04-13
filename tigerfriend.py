# --------------------------------------------------------------------
# tigerfriend.py
# --------------------------------------------------------------------
from flask import Flask, request, make_response, render_template, redirect, url_for

from admin_sql import is_admin
from html import escape
from account_sql import api_account_creation, get_year_major, get_user_bio, get_bio, update_bio
from matching import input_match_scores, get_matches
from keys import APP_SECRET_KEY
from req_lib import getOneUndergrad
import psycopg2
from chat_sql import get_messages, get_chat_id, send_chat, get_all_chats
from reports_sql import get_all_reports
from sys import stderr

# --------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')

app.secret_key = APP_SECRET_KEY

import auth

#-----------------------------------------------------------------------

@app.before_request
def before_request():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
        
# --------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    html = render_template('home.html')
    response = make_response(html)
    return response

# --------------------------------------------------------------------

@app.route('/survey', methods=['GET'])
def survey():
    # authenticated net id
    user = auth.authenticate().strip()

    try:
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:
            with connect.cursor() as cursor:
                stmt = "SELECT net_id FROM account WHERE net_id = (%s)"
                cursor.execute(stmt, [user])
                row = cursor.fetchone()
                if row is not None:
                    stmt = "SELECT username FROM account WHERE net_id = (%s)"
                    cursor.execute(stmt, [user])
                    row = cursor.fetchone()
                    if row is None:
                        return redirect(url_for("account", code=302))
                    return redirect(url_for("accountdetails", code=302))

                stmt = "SELECT question, answer1, answer2, answer3, answer4, answer5 FROM survey"
                cursor.execute(stmt)

                questions = [0]
                row = cursor.fetchone()
                while row is not None:
                    questions.append([row[0], row[1], row[2], row[3], row[4], row[5]])
                    row = cursor.fetchone()

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)

    html = render_template('survey.html', questions=questions)
    response = make_response(html)
    return response

# --------------------------------------------------------------------

@app.route('/matches', methods=['GET'])
def match():
    # authenticated net id
    user = auth.authenticate().strip()

    matches = get_matches(user)

    admin = is_admin(user)

    html = render_template('matches.html',
                           overall=matches["overall"],
                           academic=matches["academic"],
                           ec=matches["ec"],
                           personality=matches["personality"],
                           opinion=matches["opinion"],
                           isAdmin=admin
                           )
    response = make_response(html)
    return response

# --------------------------------------------------------------------

@app.route('/allChats', methods=['GET'])
def all_chats():
    # authenticated net id
    user = auth.authenticate().strip()
    receiver = request.cookies.get('cur_receiver')
    bio = get_bio(receiver)
    admin = is_admin(user)
    html = render_template('chat.html', receiver=receiver, bio_receiver=bio, isAdmin=admin)
    response = make_response(html)
    return response

# --------------------------------------------------------------------

@app.route('/getChats', methods=['GET'])
def fetching_chats():
    # authenticated net id
    user = auth.authenticate().strip()

    # fetching all the chats for the user
    open_chats = get_all_chats(user)
    if type(open_chats) is not list:
        html = ''
        return make_response(html)

    html = '<table class="table table-striped"><tbody>'
    for chat in open_chats:
        link = '<a href="chat?receiver=%s">%s</a>' % (chat, chat)
        html += '<tr><td>%s</td></tr>' % link

    html += '</tbody></table>'
    return make_response(html)

# --------------------------------------------------------------------

@app.route('/chat', methods=['GET'])
def chat():
    # authenticated net id
    receiver = request.args.get('receiver')

    # fetch the bio of the receiver
    receiver_bio = get_bio(receiver)

    html = render_template('chat.html',
                           receiver=receiver,
                           bio_receiver=receiver_bio,
                           isAdmin=admin)
    response = make_response(html)
    response.set_cookie('cur_receiver', receiver)
    return response

# --------------------------------------------------------------------

@app.route('/sendchat', methods=['GET'])
def send_message():
    # authenticated net id
    user = auth.authenticate().strip()
    receiver = request.cookies.get('cur_receiver')
    chat_sent = request.args.get('message')
    message = escape(chat_sent) # handling the attacks on the html pages

    # fetch add the message to the database
    chat_id = get_chat_id(user, receiver)

    # when the user sends a non-empty message
    if chat_sent.strip() != "":
        send_chat(chat_id, user, message)

    # getting all the messages then
    messages = reversed(get_messages(chat_id))

    return make_response(render_template('messages.html', 
    messages=messages, receiver=receiver))

# --------------------------------------------------------------------

@app.route('/getmessages', methods=['GET'])
def get_chats():
    # authenticated net id
    user = auth.authenticate().strip()
    receiver = request.cookies.get('cur_receiver')

    # fetch add the message to the database
    chat_id = get_chat_id(user, receiver)

    # refreshing the messages
    messages = reversed(get_messages(chat_id))

    return make_response(render_template('messages.html', 
    messages=messages, receiver=receiver))


# --------------------------------------------------------------------

@app.route('/about', methods=['GET'])
def about():
    html = render_template('about.html')
    response = make_response(html)
    return response

# --------------------------------------------------------------------

@app.route('/account', methods=['GET'])
def account():
    # authenticated net id
    user = auth.authenticate().strip()

    # error handling
    error_msg = request.args.get('error_msg')
    if error_msg is None:
        error_msg = ''

    q = [0]
    for x in range(1, 25):
        q.append(request.args.get('q' + str(x)))

    try:
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:
            with connect.cursor() as cursor:
                stmt = "SELECT username FROM account WHERE net_id = (%s)"
                cursor.execute(stmt, [user])
                row = cursor.fetchone()
                if row is not None:
                    return redirect(url_for("accountdetails", code=302))

                stmt = "INSERT INTO rawdata (net_id, q1_response, q2_response, q3_response, q4_response, q5_response, \
                q6_response, q7_response, q8_response, q9_response, q10_response, q11_response, q12_response, q13_response, \
                q14_response, q15_response, q16_response, q17_response, q18_response, q19_response, q20_response, q21_response, \
                q22_response, q23_response, q24_response) VALUES \
                (\'" + user + "\', \'" + q[1] + "\', \'" + q[2] \
                       + "\', \'" + q[3] + "\', \'" + q[4] + "\', \'" + \
                       q[5] + "\', \'" + q[6] + "\', \'" + q[7] + "\', \'" + \
                       q[8] + "\', \'" + q[9] + "\', \'" + q[10] + "\', \'" + q[11] \
                       + "\', \'" + q[12] + "\', \'" + q[13] + "\', \'" + q[14] \
                       + "\', \'" + q[15] + "\', \'" + q[16] + "\', \'" + q[17] \
                       + "\', \'" + q[18] + "\', \'" + q[19] + "\', \'" + q[20] \
                       + "\', \'" + q[21] + "\', \'" + q[22] + "\', \'" + q[23] \
                       + "\', \'" + q[24] + "\');"
                print(stmt)
                cursor.execute(stmt)

                connect.commit()

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)

    html = render_template('account.html', error_msg=error_msg)
    response = make_response(html)
    return response

# --------------------------------------------------------------------

@app.route('/accountdetails', methods=['GET'])
def accountdetails():
    # authenticated net id
    user = auth.authenticate().strip()

    account_info = get_user_bio(user)
    username = ""
    bio = ""
    # Only happens when coming from account creation
    if request.args.get('username') is not None:
        username = escape(request.args.get('username'))  # DEAL WITH EMPTY USERNAME INPUT HERE
        bio = escape(request.args.get('bio'))
    else:
        username = account_info[0]
        bio = account_info[1]

    # Dealing with empty username input
    if username.strip() == '':
        error_msg = "Please input a username."
        return redirect(url_for('account', error_msg=error_msg))

        # if the user doesn't already have an account
    if account_info is None:
        # checking if the username is unique
        try:
            with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                                  database="dd4c5lulvqtkld",
                                  user="fpzzhwdkkymqrr",
                                  password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:

                with connect.cursor() as cursor:
                    stmt = "SELECT username FROM account WHERE username=\'" + username + "\'"
                    cursor.execute(stmt)
                    row = cursor.fetchone()
                    if row is not None:
                        error_msg = 'Please choose another username, the one entered already exist!'
                        return redirect(url_for("account", error_msg=error_msg))

        except (Exception, psycopg2.Error) as ex:
            print(ex, file=stderr)

        req = getOneUndergrad(netid=user)
        yr = ''
        major = ''
        res = ''
        if req.ok:
            # print(req.json())
            yr = '20' + str(req.json()['class_year'])
            major = req.json()['major_type']
            res = req.json()['res_college']
        else:
            print("Error w/API call: " + req.text)

        api_account_creation(user, yr, major, res, username, bio)
        input_match_scores(user)

    if request.args.get('newbio') is not None:
        update_bio(user, request.args.get('newbio'))

    data = get_year_major(user)
    admin = is_admin(user)
    html = render_template('accountdetails.html',
                           net_id=user,
                           year=data[0],
                           major=data[1],
                           res = data[2],
                           username=username,
                           bio=bio,
                           isAdmin=admin)
    response = make_response(html)
    return response

# --------------------------------------------------------------------

@app.route('/surveydetails', methods=['GET'])
def surveydetails():
    # authenticated net id
    user = auth.authenticate().strip()

    try:
        with psycopg2.connect(host="ec2-3-217-113-25.compute-1.amazonaws.com",
                              database="dd4c5lulvqtkld",
                              user="fpzzhwdkkymqrr",
                              password="b87ef0b3ae33d79f063d25d7ec8dde6871405d7d85b67ddff7f1ddaec3d00361") as connect:
            with connect.cursor() as cursor:
                stmt = "SELECT question, answer1, answer2, answer3, answer4, answer5 FROM survey"
                cursor.execute(stmt)

                questions = [0]
                row = cursor.fetchone()
                while row is not None:
                    questions.append([row[0], row[1], row[2], row[3], row[4], row[5]])
                    row = cursor.fetchone()

                stmt = "SELECT q1_response, q2_response, q3_response, q4_response, q5_response, \
                q6_response, q7_response, q8_response, q9_response, q10_response, q11_response, q12_response, q13_response, \
                q14_response, q15_response, q16_response, q17_response, q18_response, q19_response, q20_response, q21_response, \
                q22_response, q23_response, q24_response FROM rawdata WHERE net_id = (%s)"
                cursor.execute(stmt, [user])

                answers = [0]
                row = cursor.fetchone()
                if row is not None:
                    for x in range(0, 24):
                        answers.append(row[x])

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)

    admin = is_admin(user)
    html = render_template('surveydetails.html', questions=questions, answers=answers, isAdmin=admin)
    response = make_response(html)
    return response

# --------------------------------------------------------------------

@app.route('/admin', methods=['GET'])
def admin():
    # authenticated net id
    user = auth.authenticate().strip()
    admin = is_admin(user)
    if admin:
        html = render_template('admin.html', isAdmin=admin)
    else:
        html = render_template('deniedaccess.html')

    response = make_response(html)
    return response

# --------------------------------------------------------------------

@app.route('/getReports', methods=['GET'])
def fetching_reports():
    # authenticated net id
    user = auth.authenticate().strip()
    admin = is_admin(user)
    if admin is False:
        return None
    
    # fetching all the chats for the user
    reports = get_all_reports()
    if reports == []:
        html = '<h2 style="font-size:20px; color:black; margin:10px;">There are no reports to view at this time</h2>'

    html = ('<table class="table table-striped table-borderless">'
            '<thead><tr><th>ReportID</th><th>Reported</th><th>Type</th>'
            '<th>Comment</th></thead><tbody>')
    for report in reports:
        html += '<tr>'
        pattern = '<td>%s</td>'
        link = '<a href="viewreport?=%s">%s</a>' % (report[0], report[0])
        html += pattern % link
        html += pattern % report[1]
        html += pattern % report[2]
        html += pattern % report[3]
        html += '</tr>'
        

    html += '</tbody></table>'
    return make_response(html)
