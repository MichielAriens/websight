import sqlite3
from bottle import *
import api.users
import api.messages

class ConnectionHandler():
    def __init__(self, loc='main.db'):
        self.connection = sqlite3.connect(loc)
        self.semaphore = threading.Semaphore()

    def get(self):
        self.semaphore.acquire()
        return self.connection

    def release(self):
        self.semaphore.release()

connHandler = ConnectionHandler()
userHandler = api.users.UserHandler(connHandler)

#VIEWS#
@route('/')
def homepage():
    return static_file('home.html',root='views')


#Public-API#
@route('/usersubmit', method = 'POST')
def registerUser():
    fullname = request.forms.get('fullname')
    username = request.forms.get('username')
    password = request.forms.get('password')
    userHandler.create(username,password,fullname)

@route('/newuser')
def newuserPage():
    return static_file('newuser.html', root='')

run(host='localhost', port=8080)

