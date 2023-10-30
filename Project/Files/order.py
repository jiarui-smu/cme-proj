import os
from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
# from fastapi.encoders import jsonable_encoder

# import stripe
# # This is your test secret API key.
# stripe.api_key = 'sk_test_51Ml6VEApb0N8o5GMbfEwVXAQn6XxeoXwm8OI7p2KvhjGjER9XiUxdRsWBVsYrLqpiZZeVadJA3vtJjkIKCQ54MhL00GGOAgzKX'

from datetime import datetime
import json

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/order1'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Order(db.Model):
    __tablename__ = 'order1'
    order_id = db.Column(db.Integer(), nullable=False)
    customerEmail = db.Column(db.String(32), nullable=False)
    clothesID = db.Column(db.Integer(), nullable=False)
    clothesName = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(2), nullable=False)
    color = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    totalPrice = db.Column(db.Float(precision=2), nullable=False)
    refundStatus = db.Column(db.Boolean(), nullable=False)
    transactionID = db.Column(db.Integer(), nullable=False, primary_key=True)

    def __init__(self, order_id, customerEmail, clothesID, clothesName, size, color, quantity, totalPrice, refundStatus):
        self.order_id = order_id
        self.customerEmail = customerEmail
        self.clothesID = clothesID
        self.clothesName = clothesName
        self.size = size
        self.color = color
        self.quantity = quantity
        self.totalPrice = totalPrice
        self.refundStatus = refundStatus

    def json(self):
        return {"order_id": self.order_id, "customerEmail": self.customerEmail, "clothesID": self.clothesID, "clothesName": self.clothesName, "size": self.size, 
                "color": self.color, "quantity": self.quantity, "totalPrice": self.totalPrice, "refundStatus": self.refundStatus, "transactionID": self.transactionID}


@app.route("/order1")
def get_all():
    orderlist = Order.query.all()
    if len(orderlist):
        return jsonify({
            "code": 200,
            "data": {
                "order": [order.json() for order in orderlist]
                    }
            })
    return jsonify({
        "code": 404,
        "message": "There are no orders."
        }), 404

@app.route("/order1/<int:order_id>")
def find_by_orderID(order_id):
    orderlist = Order.query.filter_by(order_id=order_id).all()
    if len(orderlist):
        return jsonify({
            "code": 200,
            "data": {
                "order": [order.json() for order in orderlist]
                    }
            })
    return jsonify({
        "code": 404,
        "message": "order not found."
        }), 404

@app.route("/order1", methods=['POST'])
def create_order():

    data = request.get_json()
    print(data)
    order = Order(**data)

    try:
        db.session.add(order)
        db.session.commit()
    except:
        return jsonify({
            "code": 500,
            "message": "An error occurred creating the order."
            }), 500

    return jsonify({
            "code": 201,
            "data": data
            }), 201

@app.route("/order1/getRefund")
def get_refund():
    refund = Order.query.filter_by(refundStatus=True)
    if refund:
        return jsonify({
            "code": 200,
            "data": {
                "order": [ord.json() for ord in refund]
                    }
            })
    return jsonify({
        "code": 404,
        "message": "There is no such refund."
        }), 404

@app.route("/order1/deleteMe/<int:order_id>")
def delete_order(order_id):
    if (Order.query.filter_by(order_id=order_id).first()):
        order = Order.query.filter_by(order_id=order_id).all()
        try:
            for ord in order:
                db.session.delete(ord)    
            db.session.commit()
        except:
            return jsonify({
                "code": 500,
                "message": "An error occurred deleting the order."
                }), 500 
        
        print("-----Order has been cancelled!-----")
        return redirect("http://localhost:8080/index.html", code=303)
    
    return jsonify({
        "code": 404,
        "data": {
            "order_id": order_id
        },
        "message": "Order not found."
        }), 404

@app.route("/order1/<int:order_id>", methods=['PUT'])
def update_order(order_id):
    if (Order.query.filter_by(order_id=order_id).first()):
        # data = request.get_json()
        # orderMe = data['order_id']
        # clothesName = data['clothesName']
        # print(data)
        
        try: 
            orderMe = Order.query.filter_by(order_id=order_id).all()
            for i in orderMe:
                # print(i.json()['totalPrice'])
                i.totalPrice = 0
                # print(i.json()['totalPrice'])
                db.session.commit()
        except:
            return jsonify({
                "code": 500,
                "data": {
                "order_id": order_id
                        },
                "message": "An error occurred updating the order."
                }), 500
        
        return jsonify({
                "code": 201,
                "message": "Total Price has been updated"
                }), 201 
    
    return jsonify({
        "code": 404,
        "data": {
            "order_id": order_id
        },
        "message": "Order not found."
        }), 404 

@app.route("/order1/refund/<int:order_id>", methods=['PUT'])
def update_refund(order_id):
    if (Order.query.filter_by(order_id=order_id).first()):
        try: 
            orderMe = Order.query.filter_by(order_id=order_id).all()
            for i in orderMe:
                if (i.refundStatus == False):
                    i.refundStatus = True
                    db.session.commit()
                else:
                    i.refundStatus = False
                    db.session.commit()
        except:
            return jsonify({
                "code": 500,
                "data": {
                "order_id": order_id
                        },
                "message": "An error occurred updating the order."
                }), 500
        
        return jsonify({
                "code": 201,
                "message": "Refund Status has been updated"
                }), 201 
    
    return jsonify({
        "code": 404,
        "data": {
            "order_ID": order_id
        },
        "message": "Order not found."
        }), 404 
    

if __name__ == "__main__":
    print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
    app.run(host='0.0.0.0', port=5001, debug=True)
# if __name__ == "__main__":
#     app.run(port=5001, debug=True)