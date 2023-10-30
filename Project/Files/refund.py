import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from datetime import datetime
import json

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/refund'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Refund(db.Model):
    __tablename__ = 'refund'
    refundPaymentID = db.Column(db.Integer(), nullable=False, primary_key=True)
    customerEmail = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    refundAmt = db.Column(db.Float(precision=2), nullable=False)
    phoneNum = db.Column(db.String(20),nullable=False)

    def __init__(self, customerEmail, description, refundAmt, phoneNum):
            self.customerEmail = customerEmail 
            self.description = description 
            self.refundAmt = refundAmt
            self.phoneNum = phoneNum

    def json(self):
        return {"refundPaymentID": self.refundPaymentID, "customerEmail": self.customerEmail, "description": self.description, "refundAmt": self.refundAmt, "phoneNum": self.phoneNum}
    

@app.route("/refund")
def get_all():
    refundlist = Refund.query.all()
    if len(refundlist):
        return jsonify({
            "code": 200,
            "data": {
                "refund": [refund.json() for refund in refundlist]
                    }
            })
    return jsonify({
        "code": 404,
        "message": "There are no orders with refund status."
        }), 404

@app.route("/refund/<int:refundPaymentID>")
def find_by_refundPaymentID(refundPaymentID):
    Refundlist = Refund.query.filter_by(refundPaymentID=refundPaymentID).all()
    if len(Refundlist):
        return jsonify({
            "code": 200,
            "data": {
                "refund": [refund.json() for refund in Refundlist]
                    }
            })
    return jsonify({
        "code": 404,
        "message": "refundPaymentID not found."
        }), 404

@app.route("/refund/", methods=['POST'])
def create_refund():
    data = request.get_json()
    #print(data)
    refund = Refund(**data)

    try:
        db.session.add(refund)
        db.session.commit()
    except:
        return jsonify({
            "code": 500,
            "data": {
            "refundID": refund
                    },
            "message": "An error occurred creating the refund."
            }), 500

    return jsonify({
            "code": 201,
            "data": data
            }), 201

if __name__ == "__main__":
    print("This is flask for " + os.path.basename(__file__) + ": manage refund ...")
    app.run(host='0.0.0.0', port=5010, debug=True)