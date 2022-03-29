# --------------------------------------------------------------------
# tigerfriend.py
# --------------------------------------------------------------------

from flask import Flask, request, make_response, render_template, redirect, url_for
from RawData_SQL import api_account_creation, get_user_data, get_account_details
from matching import get_user_match_info
from keys import APP_SECRET_KEY
from req_lib import getOneUndergrad
import psycopg2
from sys import stderr

# --------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')

app.secret_key = APP_SECRET_KEY

import auth


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
        with psycopg2.connect(host="ec2-52-54-212-232.compute-1.amazonaws.com",
                              database="d1qoonauda49lp",
                              user="gehgaeoepuqelg",
                              password="8a2c415ed295edded3641f084099f247971fc720d4c83c7e79bf1951c3dcd38a") as connect:
            with connect.cursor() as cursor:
                stmt = "SELECT net_id FROM account WHERE net_id = (%s)"
                cursor.execute(stmt, [user])
                row = cursor.fetchone()
                if row is not None:
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
def matches():
    # authenticated net id
    user = auth.authenticate().strip()

    match_info = get_user_match_info(user)

    html = render_template('matches.html',
                           overall_match_user=match_info["overall_match"][0],
                           overall_match_bio=match_info["overall_match"][1],
                           academic_match_user=match_info["academic_match"][0],
                           academic_match_bio=match_info["academic_match"][1],
                           extracurricular_match_user=match_info["extracurricular_match"][0],
                           extracurricular_match_bio=match_info["extracurricular_match"][1],
                           personality_match_user=match_info["personality_match"][0],
                           personality_match_bio=match_info["personality_match"][1],
                           opinion_match_user=match_info["opinion_match"][0],
                           opinion_match_bio=match_info["opinion_match"][1]
                           )
    response = make_response(html)
    return response


# --------------------------------------------------------------------

@app.route('/chat', methods=['GET'])
def chat():
    # authenticated net id
    user = auth.authenticate().strip()

    html = render_template('chat.html')
    response = make_response(html)
    return response


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

    q = [0]
    for x in range(1, 25):
        q.append(request.args.get('q' + str(x)))

    try:
        with psycopg2.connect(host="ec2-52-54-212-232.compute-1.amazonaws.com",
                              database="d1qoonauda49lp",
                              user="gehgaeoepuqelg",
                              password="8a2c415ed295edded3641f084099f247971fc720d4c83c7e79bf1951c3dcd38a") as connect:

            with connect.cursor() as cursor:
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

    html = render_template('account.html')
    response = make_response(html)
    return response


# --------------------------------------------------------------------

@app.route('/accountdetails', methods=['GET'])
def accountdetails():
    # authenticated net id
    user = auth.authenticate().strip()

    account_info = get_account_details(user)
    username = ""
    bio = ""
    # Only happens when coming from account creation
    if request.args.get('username') is not None:
        username = request.args.get('username')  # DEAL WITH EMPTY USERNAME INPUT HERE
        bio = request.args.get('bio')
    else:
        username = account_info[0]
        bio = account_info[1]

    # checking if the username is unique
    try:
        with psycopg2.connect(host="ec2-52-54-212-232.compute-1.amazonaws.com",
                              database="d1qoonauda49lp",
                              user="gehgaeoepuqelg",
                              password="8a2c415ed295edded3641f084099f247971fc720d4c83c7e79bf1951c3dcd38a") as connect:

            with connect.cursor() as cursor:
                stmt = "SELECT username FROM account WHERE username=\'" + username + "\'"
                cursor.execute(stmt)
                row = cursor.fetchone()
                if row is not None:
                    return 

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)

    # if the user doesn't already have an account
    if account_info is None:
        req = getOneUndergrad(netid=user)
        yr = ''
        major = ''
        res = ''
        if req.ok:
            print(req.json())
            yr = '20' + str(req.json()['class_year'])
            major = req.json()['major_code']
            res = req.json()['res_college']
        else:
            print("Error w/API call: " + req.text)

        api_account_creation(user, yr, major, res, username, bio)

    data = get_user_data(user)
    html = render_template('accountdetails.html',
                           net_id=user,
                           year=data[0],
                           major=data[1],
                           username=username,
                           bio=bio)
    response = make_response(html)
    return response

# --------------------------------------------------------------------

@app.route('/surveydetails', methods=['GET'])
def surveydetails():
    # authenticated net id
    user = auth.authenticate().strip()

    try:
        with psycopg2.connect(host="ec2-52-54-212-232.compute-1.amazonaws.com",
                              database="d1qoonauda49lp",
                              user="gehgaeoepuqelg",
                              password="8a2c415ed295edded3641f084099f247971fc720d4c83c7e79bf1951c3dcd38a") as connect:
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
                    for x in range(0,24):
                        answers.append(row[x])

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)

    html = render_template('surveydetails.html', questions=questions, answers=answers)
    response = make_response(html)
    return response