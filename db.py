from flask_mongoengine import MongoEngine

db = MongoEngine()   #db object creation

def initialize_db(app):
    db.init_app(app)