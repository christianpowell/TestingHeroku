from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    #see user.py comments on what this is
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    #"we have a relationship with ItemModel"
    #sqlalchemy: okay, what's the relationship?
    #goes into item.py and finds 'stores.id'
    ##lazy dynamic loads when json is called, remove if wanting to load WHOLE table once 
    items = db.relationship('ItemModel', lazy='dynamic') #many to one list of item models

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

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
