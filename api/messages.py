"""
Main api for messaging
"""

import sqlite3
import hashlib
import random
import string

from api import *


#Public--------------------------------------------------------------------------------------------
# ||
#_||_
#\  /
# \/


#Get a list of message id's associated with the user's inbox.
def get_inbox(username, password):
    if users.validate(username, password):
        __get_inbox(username)
    else:
        pass

#Private-------------------------------------------------------------------------------------------
# ||
#_||_
#\  /
# \/


def __get_inbox(username):
    curs = conn.cursor()
    results = []
    for message in curs.execute("SELECT messageid FROM messages WHERE receiver = ?",(username,)):
        results.append(message[0])
    return results