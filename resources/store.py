from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

    #returns a specific store
    def get(self, name):
        #may return store object or None
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {'message': 'Store not found'}, 404

    #creates a store
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': "Store '{}' created.".format(name)}
        return store.json(), 201

    #deletes a store
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        #refer to item.py for more information
        return {'stores': [store.json() for store in StoreModel.query.all()]}
