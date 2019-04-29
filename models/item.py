from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    #see user.py comments on what this is
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    #"what store do we belong to?"
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))#stores.id type
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name (cls, name):
        #runs a query that filters by name
        return cls.query.filter_by(name=name).first() #SELECT * FROM items WHERE name=name

    def save_to_db(self):
        #can add multiple objects per session then commit but only 1 in this case
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
