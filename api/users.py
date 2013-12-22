"""
Main api for users
"""
import sqlite3
import hashlib
import random
import string

from api import *


class UserHandler():
    def __init__(self,connHandler):
        self.connHandler = connHandler
        """:type : ConnectionHandler"""

    #Public--------------------------------------------------------------------------------------------
    # ||
    #_||_
    #\  /
    # \/

    #Creates and stores a user.
    #TODO error handling
    def create(self,username, password, fullname):
        pwsalt = ''.join(random.choice(string.printable) for x in range(10))
        tohash = password + pwsalt
        pwhash = hashlib.sha256(tohash.encode('utf-8')).digest()
        conn = self.connHandler.get()
        curs = conn.cursor()
        curs.execute("INSERT INTO users VALUES (?,?,?,?)",(username, fullname, pwhash, pwsalt))
        conn.commit()
        curs.close()
        self.connHandler.release()

    #Private-------------------------------------------------------------------------------------------
    # ||
    #_||_
    #\  /
    # \/

    #Checks whether a password and a salt hash into the hash parameter
    def salted_password_check(self, password, salt, hash):
        tohash = password + salt
        return hashlib.sha256(tohash.encode('utf-8')).digest() == hash

    #Sets the password of the user
    #WARN! Security threat
    def reset_password(self, username, newpassword):
        pwsalt = ''.join(random.choice(string.printable) for x in range(10))
        tohash = newpassword + pwsalt
        pwhash = hashlib.sha256(tohash.encode('utf-8')).digest()
        conn = self.connHandler.get()
        curs = conn.cursor()
        curs.execute("UPDATE users SET pwhash=?,pwsalt=? WHERE username=?",(pwhash, pwsalt, username))
        curs.close()
        conn.commit()
        self.connHandler.release()

    #Checks whether a username-password pair is valid.
    def validate(self, username, password):
        conn = self.connHandler.get()
        curs = conn.cursor()
        curs.execute("SELECT pwsalt, pwhash FROM users WHERE username = ?", (username,))
        user = curs.fetchone() #[pwsalt, pwhash]
        curs.close()
        self.connHandler.release()
        #print(user)
        return salted_password_check(password, user[0],user[1])
