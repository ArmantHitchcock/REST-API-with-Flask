import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field can not be left blank')
        
    @jwt_required()    # now required to authenticate before route func is executed
    def get(self, name):
        item = ItemModel.find_by_name(name)   #could also be Item.find_by_name
        if item is not None:
            return item.json()
        else:
            return {"message":"item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):      #could also be Item.find_by_name
            return{'message':"An item with the name '{}' already exists.".format(name)}, 400 # request error
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            Item.save_to_db()
        except:
            return {'message':'An error occurred inserting the item'}, 500  # internal server error 
        return item.json(), 201

    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'item deleted'}
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message':'item deleted'}
        """

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:
            try:
                updated_item.insert()
            except:
                return {'message':'An error occured inserting the item'}, 500
        else:
            try:
                updated_item.update()
            except:
                return {'message':'An error occured updating the item'}, 500
        return updated_item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name':row[0],'price':row[1]})
        connection.close()
        return {'items':items}