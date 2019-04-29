import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
#a resource is an external representation of an entity

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    #parse request to ensure 'price' exists when updating
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        #if this username exists error check; returns object or None
        if UserModel.find_by_username(data['username']):
            return {'message': 'username already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201
