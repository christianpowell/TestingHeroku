import sqlite3
from db import db
#a helper class that is used to store data about user
#a model is our internal representation of an entitiy

class UserModel(db.Model):
    __tablename__ = 'users'
    #the below ensures that username and password properties much match columns
    #there's a column called id of type integer that's a primary key(unique[index])
    id = db.Column(db.Integer, primary_key=True)
    #(80) limits the size
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


    def __init__(self, username, password):
        #these properties much match above Columns
        self.username = username
        self.password = password

    def save_to_db(self):
        #can add multiple objects per session then commit but only 1 in this case
        db.session.add(self)
        db.session.commit()

    #finds user by searching for username
    @classmethod
    def find_by_username(cls, username):
        #see item.py for more info
        return cls.query.filter_by(username=username).first() #returns first row

    #find user by user id
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first() #returns first row
