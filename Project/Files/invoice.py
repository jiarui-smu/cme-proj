import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from datetime import datetime
import json

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/invoice'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Invoice(db.Model):
    __tablename__ = 'invoice'
    invoiceID = db.Column(db.Integer(), nullable=False, primary_key=True)
    customerEmail = db.Column(db.String(32), nullable=False)
    order_ID = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    totalPrice = db.Column(db.Float(precision=2), nullable=False)
    payMethod = db.Column(db.String(100), nullable=True)
    stripe_id = db.Column(db.String(500), nullable=True)

    def __init__(self, customerEmail, order_ID, description, totalPrice, payMethod, stripe_id):
        self.customerEmail = customerEmail
        self.order_ID = order_ID 
        self.description = description 
        self.totalPrice = totalPrice
        self.payMethod = payMethod
        self.stripe_id = stripe_id

    def json(self):
        return {"customerEmail": self.customerEmail,"order_ID": self.order_ID, "description": self.description, 
                "price": self.totalPrice, "payMethod": self.payMethod, "stripe_id": self.stripe_id}

@app.route("/invoice")
def get_all():
    invoicelist = Invoice.query.all()
    if len(invoicelist):
        return jsonify({
            "code": 200,
            "data": {
                "invoice": [invoice.json() for invoice in invoicelist]
                    }
            })
    return jsonify({
        "code": 404,
        "message": "There are no such invoices."
        }), 404

@app.route("/invoice/<int:order_ID>")
def find_by_orderID(order_ID):
    invoicelist = Invoice.query.filter_by(order_ID=order_ID).all()
    if len(invoicelist):
        return jsonify({
            "code": 200,
            "data": {
                "invoice": [invoice.json() for invoice in invoicelist]
                    }
            })
    return jsonify({
        "code": 404,
        "message": "invoice not found."
        }), 404

@app.route("/invoice", methods=['POST'])
def create_invoice():

    data = request.get_json()
    print(data)
    invoice = Invoice(**data)

    try:
        db.session.add(invoice)
        db.session.commit()
    except:
        return jsonify({
            "code": 500,
            "message": "An error occurred creating the invoice."
            }), 500

    return jsonify({
            "code": 201,
            "data": data
            }), 201

@app.route("/invoice/<int:order_id>", methods=['PUT'])
def update_invoice(order_id):
    if (Invoice.query.filter_by(order_ID=order_id).first()):
        data = request.get_json()
        # print(data)
        try: 
            invoiceMe = Invoice.query.filter_by(order_ID=order_id).all()
            # print(invoiceMe)
            for i in invoiceMe:
                # print(i.json()['stripe_id'])
                i.stripe_id = data
                # print(i.json()['stripe_id'])
                db.session.commit()
            
        except:
            return jsonify({
                "code": 500,
                "message": "An error occurred updating the invoice stripe_id."
                }), 500
        
        return jsonify({
                "code": 201,
                "message": "Stripe ID has been updated."
                }), 201 
    
    return jsonify({
        "code": 404,
        "message": "Invoice not found."
        }), 404 
    

if __name__ == "__main__":
    print("This is flask for " + os.path.basename(__file__) + ": manage invoices ...")
    app.run(host='0.0.0.0', port=5002, debug=True)
# if __name__ == "__main__":
#     app.run(port=5002, debug=True)