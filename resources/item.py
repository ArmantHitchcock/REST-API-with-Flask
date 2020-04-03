from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity, fresh_jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field can not be left blank')
    parser.add_argument('store_id', type=int, required=True, help='every item needs a store id')
        
    @jwt_required    # now required to authenticate before route func is executed
    def get(self, name):
        item = ItemModel.find_by_name(name)   #could also be Item.find_by_name
        if item is not None:
            return item.json()
        else:
            return {"message":"item not found"}, 404
    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return{'message':"An item with the name '{}' already exists.".format(name)}, 400 # request error
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message':'An error occurred inserting the item'}, 500  # internal server error 
        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilage required.'}, 401
        

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [x.json() for x in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {'items': [x['name'] for x in items], 'message': 'More data available if you log in.'}, 200
