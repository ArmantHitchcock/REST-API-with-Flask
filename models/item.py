# import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__='items'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80))
    price=db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}


    @classmethod
    def find_by_name(cls, name):
        return cls,query.filter_by(name=name)  # SELECT * FROM items WHERE name=name
        # returns an item model object
        # eg1. return ItemModel,query.filter_by(name=name).filter_by(id=1)      SELECT * FROM items WHERE name=name AND id=1
        # eg2. return ItemModel,query.filter_by(name=name, id=1)        SELECT * FROM items WHERE name=name AND id=1
        # eg3. return ItemModel,query.filter_by(name=name).first()      SELECT * FROM items WHERE name=name LIMIT 1
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row is not None:
            return cls(row[0], row[1])
        """

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self.name,self.price))
        connection.commit()
        connection.close()
        """
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    """
    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (self.price,self.name))
        connection.commit()
        connection.close()
        """