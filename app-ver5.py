# pip install Flask
# pip install Flask-RESTfull
# pip install Flask-JWT
# pip install Flask-SQLAlchemy
# JWT = Json web Token
from db import db
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'     #sqlite can be changed to another sql db system
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'  # shouldn't be visible in production
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)          # creates a new end point /auth
api.add_resource(Store, '/store/<string:name>') # CRD for stores
api.add_resource(Item, '/item/<string:name>')   # CRUD for items
api.add_resource(ItemList, '/items')            # returns a list of all the items
api.add_resource(StoreList, '/stores')          # returns a list of all the stores
api.add_resource(UserRegister, '/register')     # register a new user

# only runs app if this file is run, and not if it is run through import
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
