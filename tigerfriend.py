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
    html = render_template('page2.html')
    response = make_response(html)
    return response

#---------------------------------------------------------------------

@app.route('/page2', methods=['GET'])
def page2():
    html = render_template('page2.html')
    response = make_response(html)
    return response

#---------------------------------------------------------------------

@app.route('/page3', methods=['GET'])
def page3():
    html = render_template('page3.html')
    response = make_response(html)
    return response

#---------------------------------------------------------------------

@app.route('/page4', methods=['GET'])
def page4():
    html = render_template('page4.html')
    response = make_response(html)
    return response

#---------------------------------------------------------------------

if __name__ == '__main__':
   app.run(debug=True)