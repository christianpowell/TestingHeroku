from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#Christian's first CRUD API

class Item(Resource):
    TABLE_NAME = 'items'
    parser = reqparse.RequestParser()
    #parse request to ensure 'price' exists when updating
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name'{}' already exists.".format(name)}, 400 #bad request

        #error first development: don't load data before error checking
        data = Item.parser.parse_args()

        #pre-parser course\\ data = request.get_json() #will give error if doesn't attach json payload or wrong content type header
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'an error occurred inserting the item.'}, 500 #internal server error

        return item.json(), 201 #201 is created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None: #create item if doesn't exist
            #since none found, create a new one
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    TABLE_NAME = 'items'

    def get(self):
        #list comrehension
        return {'items': [item.json() for item in ItemModel.query.all()]}
        #using lambda
        #reutrn {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
