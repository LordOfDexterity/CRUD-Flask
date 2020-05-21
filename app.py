# dependecies : Flask_PyMongo, bycrypt, werkzeug==0.16.1
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/Users"

mongo = PyMongo(app)

@app.route('/add', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _pwd = _json['pwd']

    if _name and _email and _pwd and request.method == 'POST':
        _hashed_password = generate_password_hash(_pwd)
        id = mongo.db.user.insert({'name': _name, 'email':_email, 'pwd':_hashed_password})
        resp = jsonify("<h1>user added succesfully</h1>")
        resp.status_code = 200

        return resp
    
    else:
        return "Not found"

@app.route('/')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp

@app.route('/user/<id>')
def user(id):
    user = mongo.db.user.find_one({"_id":ObjectId(id)})
    resp = dumps(user)
    return resp

@app.route('/delete_user/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({"_id":ObjectId(id)})
    return "User deleted succesfully"

@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    _id=id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _pwd = _json['pwd']

    if _name and _email and _pwd and request.method == 'PUT':
        _hashed_password = generate_password_hash(_pwd)
        mongo.db.user.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name':_name, 'email':_email, 'pwd':_hashed_password}})
        resp = jsonify("<h1>user updated succesfully</h1>")
        resp.status_code = 200

        return resp
    else:
        return "Error, something went wrong"
if __name__ == '__main__':
    app.run(debug=True) 