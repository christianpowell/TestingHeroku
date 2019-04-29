from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
#SQLAlchemy DB lives at root folder of our project and 'sqlite' can be changed to other DBs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'test'
api = Api(app)

jwt = JWT(app, authenticate, identity) #creates a new endpoint; /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') #http://127.0.0.1:5000/item/Chair
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register') #when POST request, calls post method in user.py

#incase we import app.py later; doesn't run our app
#runs when we do this from command prompt, uwsgi doesn't see this
if __name__ == '__main__':
    #import this here due to "circular imports"
    #our other items are going to import DB as well
    #when we import the model, it's going to import the DB in app
    from db import db
    db.init_app(app)
    app.run(port=5000, debug = True)
