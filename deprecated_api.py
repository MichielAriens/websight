import sqlite3
import hashlib
import random
import string

conn = sqlite3.connect('main.db')


#Checks whether a password and a salt hash into the hash parameter
def salted_password_check(password, salt, hash):
    tohash = password + salt
    return hashlib.sha256(tohash.encode('utf-8')).digest() == hash


#Creates and stores a user.
#TODO error handling
def create_user(username, password, fullname):
    pwsalt = ''.join(random.choice(string.printable) for x in range(10))
    tohash = password + pwsalt
    pwhash = hashlib.sha256(tohash.encode('utf-8')).digest()
    curs = conn.cursor()
    curs.execute("INSERT INTO users VALUES (?,?,?,?)",(username, fullname, pwhash, pwsalt))
    conn.commit()
    
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
def validate_user(username, password):
    curs = conn.cursor()
    curs.execute("SELECT pwsalt, pwhash FROM users WHERE username = ?", (username,))
    user = curs.fetchone() #[pwsalt, pwhash]
    #print(user)
    return salted_password_check(password, user[0],user[1])


#MESSAGES

#Get a list of message id's associated with the user's inbox.
def get_inbox(username, password):
    if validate_user(username, password):
        __get_inbox(username)
    else:
        pass

def __get_inbox(username):
    curs = conn.cursor()
    results = []
    for message in curs.execute("SELECT messageid FROM messages WHERE receiver = ?",(username,)):
        results.append(message[0])
    return results

























