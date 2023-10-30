import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from datetime import datetime
import json

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/customer'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

class customer(db.Model):
    __tablename__ = 'customer'
    customerEmail = db.Column(db.String(255),nullable=False, primary_key=True)
    phoneNum = db.Column(db.String(8),nullable=False)
    bankNum = db.Column(db.String(16),nullable=False)
    homeAddress = db.Column(db.String(255),nullable=False)


    def __init__(self, customerEmail, phoneNum, bankNum, homeAddress):
        self.customerEmail = customerEmail
        self.phoneNum = phoneNum
        self.bankNum = bankNum
        self.homeAddress = homeAddress

    def json(self):
        return {"customerEmail": self.customerEmail,
                "phoneNum": self.phoneNum,
                "bankNum": self.bankNum,
                "homeAddress": self.homeAddress}
     
@app.route("/customer")
def get_all():
    custlist = customer.query.all()
    if len(custlist):
        return jsonify({
            "code": 200,
            "data": {
                "Customer": [customer.json() for customer in custlist]
                    }
            })
    return jsonify({
        "code": 404,
        "message": "There are no such customers."
        }), 404

#@app.route("/customer/<email>",methods=['GET'])
@app.route("/customer/<string:customerEmail>",methods=['GET'])
def get_cust_num(customerEmail):
    #customer = customer.query.filter_by(email=email).first()
    customerMe = customer.query.filter_by(customerEmail=customerEmail).first()
    if customerMe:
        return jsonify({
            'code': 200,
            'data': {
                'CustomerEmail': customerMe.customerEmail,'PhoneNum': customerMe.phoneNum
                    }
            })
    return jsonify({
        "code": 404,
        "message": "There are no such customers."
        }), 404

@app.route("/customer/number")
def get_all_numbers():
    custlist = customer.query.all()
    if len(custlist):
        return jsonify({
            "code": 200,
            "data": {
                "num": [num.phoneNum for num in custlist]
                    }
            })
    return jsonify({
        "code": 404,
        "message": "There are no such numbers."
        }), 404

if __name__ == "__main__":
    print("This is flask for " + os.path.basename(__file__) + ": manage customer ...")
    app.run(host='0.0.0.0', port=5003, debug=True)