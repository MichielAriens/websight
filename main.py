import sqlite3
from bottle import *
from dbus.decorators import method
from api import *

conn = sqlite3.connect('main.db')
curs = conn.cursor()


#VIEWS#

@route('/usersubmit', method = 'POST')
def registerUser():
    fullname = request.forms.get('fullname')
    username = request.forms.get('username')
    password = request.forms.get('password')
    if len(fullname) > 255 or len(username) > 255 or len(password) > 255:
        return "<p>One field was too long</p>"
    else:
        curs.execute("INSERT INTO users VALUES ('{0}','{1}','{2}')".format(username,password,fullname))
        conn.commit()
        return "<p>Welcome {0}!</p>".format(fullname)
        

@route('/newuser')
def newuserPage():
    return static_file('newuser.html', root='')


@route('/')
def index():
    return "hello!"

run(host='localhost', port=8080)

