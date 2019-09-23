from flask import Flask, render_template, url_for, flash, redirect, request, Response, session, abort, escape
import mysql.connector
from mysql.connector import errorcode
import os

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(12)

db = mysql.connector.connect(
    host='localhost', user='root', password='', database='users')
db.autocommit = True
cursor = db.cursor(buffered=True)

user_query = ('SELECT * FROM user WHERE username = %s AND password = %s')


def close_session():
    [session.pop(key) for key in list(session.keys())]


def insert_user(username, password, firstname, lastname, email):
    query = "INSERT INTO user(username, password, firstname, lastname, email) \
            VALUES(%s, %s, %s, %s, %s)"

    args = (username, password, firstname, lastname, email)
    cursor.execute(query, args)
    db.commit()


@app.route('/')
def index():
    return infomation()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['action'] == 'Login' and 'username' in request.form and 'password' in request.form:

        userdetails = request.form
        username = userdetails['username']
        password = userdetails['password']
        args = (username, password)
        cursor.execute(user_query, args)
        account = cursor.fetchone()

        print(username, password)

        if account:
            print('account')

            session['username'] = username
            session['password'] = password
            session['logged_in'] = True

            return infomation()
        else:
            print('not account')

            session['logged_in'] = False

            render_template('Login.html')

    if request.method == 'POST' and request.form['action'] == 'Register':
        return render_template("Register.html")

    return render_template('Login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and request.form['action'] == 'Register':
        userdetails = request.form
        username = userdetails['username']
        password = userdetails['password']
        args = (username, password)
        cursor.execute(user_query, args)
        result = cursor.fetchone()

        if result:
            return render_template('Register.html')
        else:
            firstname = userdetails['firstname']
            lastname = userdetails['lastname']
            email = userdetails['email']

            session['username'] = username
            session['password'] = password
            session['firstname'] = firstname
            session['lastname'] = lastname
            session['email'] = email
            session['logged_in'] = True

            insert_user(username, password, firstname, lastname, email)

            return render_template('Infomation.html', firstname=session['firstname'], lastname=session['lastname'], email=session['email'])

        return infomation()

    return render_template('Register.html')


@app.route('/infomation', methods=['GET', 'POST'])
def infomation():
    if request.method == 'POST' and request.form['action'] == 'Logout':
        close_session()
        session['logged_in'] = False

        return render_template('Login.html')

    if not session.get('logged_in'):
        return render_template('Login.html')
    else:
        username = session['username']
        password = session['password']
        cursor.execute(user_query, (username, password))
        account = cursor.fetchone()

        if account:
            username = account[0]
            password = account[1]
            firstname = account[2]
            lastname = account[3]
            email = account[4]

            return render_template('Infomation.html', firstname=firstname, lastname=lastname, email=email)

    return infomation()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
