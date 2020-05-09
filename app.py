import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')     #sqlite can be changed to another sql db system
from db import db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'jose' #app.config['JWT_SECRET_KEY']
api = Api(app)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:       # Instead of hard-coding, you should read from a config file or a database
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({'description': 'The token has expired.', 'error': 'token_expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'description': 'Signature verification failed.', 'error': 'invalid_token'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'description': 'Request does not contain a access token.', 'error': 'authorization_required'}), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({'description': 'The token is not fresh.', 'error': 'fresh_token_required'}), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({'description': 'The token has been revoked.', 'error': 'token_revoked'}), 401


api.add_resource(Store, '/store/<string:name>') # CRD for stores
api.add_resource(StoreList, '/stores')          # returns a list of all the stores
api.add_resource(Item, '/item/<string:name>')   # CRUD for items
api.add_resource(ItemList, '/items')            # returns a list of all the items
api.add_resource(UserRegister, '/register')     # register a new user
api.add_resource(User, '/user/<int:user_id>')   # find and delete a user
api.add_resource(UserLogin, '/login')           # Login a user
api.add_resource(UserLogout, '/logout')         # Logout a user
api.add_resource(TokenRefresh, '/refresh')      # refresh token for a user

# only runs app if this file is run, and not if it is run through import
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
