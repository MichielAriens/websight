"""
Main api for users
"""
import sqlite3
import hashlib
import random
import string

from api import *

conn = sqlite3.connect('main.db')

#Public--------------------------------------------------------------------------------------------
# ||
#_||_
#\  /
# \/

#Creates and stores a user.
#TODO error handling
def create(username, password, fullname):
    pwsalt = ''.join(random.choice(string.printable) for x in range(10))
    tohash = password + pwsalt
    pwhash = hashlib.sha256(tohash.encode('utf-8')).digest()
    curs = conn.cursor()
    curs.execute("INSERT INTO users VALUES (?,?,?,?)",(username, fullname, pwhash, pwsalt))
    conn.commit()
    
#Private-------------------------------------------------------------------------------------------
# ||
#_||_
#\  /
# \/

    
#Checks whether a password and a salt hash into the hash parameter
def salted_password_check(password, salt, hash):
    tohash = password + salt
    return hashlib.sha256(tohash.encode('utf-8')).digest() == hash
    
#Sets the password of the user
#WARN! Security threat
def reset_password(username, newpassword):
    pwsalt = ''.join(random.choice(string.printable) for x in range(10))
    tohash = newpassword + pwsalt
    pwhash = hashlib.sha256(tohash.encode('utf-8')).digest()
    curs = conn.cursor()
    curs.execute("UPDATE users SET pwhash=?,pwsalt=? WHERE username=?",(pwhash, pwsalt, username))
    conn.commit()

#Checks whether a username-password pair is valid.
def validate(username, password):
    curs = conn.cursor()
    curs.execute("SELECT pwsalt, pwhash FROM users WHERE username = ?", (username,))
    user = curs.fetchone() #[pwsalt, pwhash]
    #print(user)
    return salted_password_check(password, user[0],user[1])