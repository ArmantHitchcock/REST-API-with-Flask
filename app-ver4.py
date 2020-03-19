# pip install Flask
# pip install Flask-RESTfull
# pip install Flask-JWT
# pip install Flask-SQLAlchemy
# JWT = Json web Token
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'jose'  # shouldn't be visible
api = Api(app)
jwt = JWT(app, authenticate, identity) # creates a new end point /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':      # only runs app if this file is run, and not if it is run through import
    app.run(port=5000, debug=True)