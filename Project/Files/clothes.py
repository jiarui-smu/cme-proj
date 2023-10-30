import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from datetime import datetime
import json

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/clothes'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Clothes(db.Model):
    __tablename__ = 'clothes'
    clothesID = db.Column(db.Integer(), nullable=False, primary_key=True)
    size = db.Column(db.String(2), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    color = db.Column(db.String(80), nullable=False)
    cost = db.Column(db.Float(precision=2), nullable=False)
    image = db.Column(db.String(4000), nullable=False)
    isOnPromotion = db.Column(db.Boolean())

    def __init__(self, clothesID, size, name, description, color, cost, image, isOnPromotion):
        self.clothesID = clothesID
        self.size = size
        self.name = name
        self.description = description
        self.color = color
        self.cost = cost
        self.image = image
        self.isOnPromotion = isOnPromotion

    def json(self):
        return {"clothesID": self.clothesID, "size": self.size, "name": self.name, "description": self.description, "color": self.color,
                "cost": self.cost, "image": self.image, "isOnPromotion": self.isOnPromotion}

@app.route("/clothes")
def get_all():
    clotheslist = Clothes.query.all()
    if len(clotheslist):
        return jsonify({
            "code": 200,
            "data": {
                "clothes": [clothe.json() for clothe in clotheslist]
                    }
            })
    return jsonify({
        "code": 404,
        "message": "There are no such clothes."
        }), 404

@app.route("/clothes/<int:clothesID>")
def find_by_clothesID(clothesID):
    clothes = Clothes.query.filter_by(clothesID=clothesID).first()
    if clothes:
        return jsonify({
            "code": 200,
            "data": clothes.json()
            })
    return jsonify({
        "code": 404,
        "message": "clothes not found."
        }), 404

# @app.route("/clothes/<string:isbn13>", methods=['POST'])
# def create_clothes(isbn13):
#     if (clothes.query.filter_by(isbn13=isbn13).first()):
#         return jsonify({
#             "code": 400,
#             "data": {
#             "isbn13": isbn13
#                     },
#             "message": "clothes already exists."
#             }), 400

#     data = request.get_json()
#     clothes = Clothes(isbn13, **data)

#     try:
#         db.session.add(clothes)
#         db.session.commit()
#     except:
#         return jsonify({
#             "code": 500,
#             "data": {
#             "isbn13": isbn13
#                     },
#             "message": "An error occurred creating the clothes."
#             }), 500

#     return jsonify({
#             "code": 201,
#             "data": clothes.json()
#             }), 201

# @app.route("/clothes/<string:isbn13>", methods=['DELETE'])
# def delete_clothes(isbn13):
#     if (clothes.query.filter_by(isbn13=isbn13).first()):
#         clothes = clothes.query.filter_by(isbn13=isbn13).first()
#         try:
#             db.session.delete(clothes)
#             db.session.commit()
#         except:
#             return jsonify({
#                 "code": 500,
#                 "data": {
#                 "isbn13": isbn13
#                         },
#                 "message": "An error occurred deleting the clothes."
#                 }), 500

#         return jsonify({
#                 "code": 201,
#                 "data": {
#                     "isbn13": isbn13
#                 }
#                 }), 201 
#     return jsonify({
#         "code": 404,
#         "data": {
#             "isbn13": isbn13
#         },
#         "message": "clothes not found."
#         }), 404

# @app.route("/clothes/<string:isbn13>", methods=['PUT'])
# def update_clothes(isbn13):
#     if (Clothes.query.filter_by(isbn13=isbn13).first()):
#         # clothes = clothes.query.filter_by(isbn13=isbn13).first()
#         # try:
#         #     db.session.delete(clothes)
#         #     db.session.commit()
#         # except:
#         #     return jsonify({
#         #         "code": 500,
#         #         "data": {
#         #         "isbn13": isbn13
#         #                 },
#         #         "message": "An error occurred deleting the clothes."
#         #         }), 500

#         data = request.get_json()
#         isbn = data['isbn13']
#         title = data['title']
#         price = data['price']
#         avail = data['availability']

#         print(data)
        
#         try: 
#             clothesMe = Clothes.query.filter_by(isbn13=isbn13).first()
#             clothesMe.title = title
#             clothesMe.price = price
#             clothesMe.availability = avail
#             clothesMe.isbn13 = isbn
#             db.session.commit()
#         except:
#             return jsonify({
#                 "code": 500,
#                 "data": {
#                 "isbn13": isbn13
#                         },
#                 "message": "An error occurred updating the clothes."
#                 }), 500
#         return jsonify({
#                 "code": 201,
#                 "data": {
#                     "Old isbn13": isbn13,
#                     "New isbn13": isbn
#                 }
#                 }), 201 
#     return jsonify({
#         "code": 404,
#         "data": {
#             "isbn13": isbn13
#         },
#         "message": "clothes not found."
#         }), 404 
    
if __name__ == "__main__":
    print("This is flask for " + os.path.basename(__file__) + ": manage clothes ...")
    app.run(host='0.0.0.0', port=5000, debug=True)