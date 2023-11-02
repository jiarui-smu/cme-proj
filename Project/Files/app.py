import os, sys
from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import json

import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51O6HLAL2LHXuITvYbJysUSYDkuAhDf26IHDJQ2n7IyVysdv5ahjU4Ra8pikfRAWypGWl7BTKZXp0q2QQzXlMK1dA00TnSYnPFL'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/quikkarts'
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
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
def get_all_clothes():
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
def get_all_customer():
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

    
class Order(db.Model):
    __tablename__ = 'order1'
    order_id = db.Column(db.Integer(), nullable=False)
    customerEmail = db.Column(db.String(32),db.ForeignKey(customer.customerEmail) ,nullable=False)
    clothesID = db.Column(db.Integer(),db.ForeignKey(Clothes.clothesID), nullable=False)
    clothesName = db.Column(db.String(100),db.ForeignKey(Clothes.name) ,nullable=False)
    size = db.Column(db.String(2),db.ForeignKey(Clothes.size), nullable=False)
    color = db.Column(db.String(80),db.ForeignKey(Clothes.color), nullable=False)
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
def get_all_order():
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

# @app.route("/order1/getRefund")
# def get_refund():
#     refund = Order.query.filter_by(refundStatus=True)
#     if refund:
#         return jsonify({
#             "code": 200,
#             "data": {
#                 "order": [ord.json() for ord in refund]
#                     }
#             })
#     return jsonify({
#         "code": 404,
#         "message": "There is no such refund."
#         }), 404

# @app.route("/order1/deleteMe/<int:order_id>")
# def delete_order(order_id):
#     if (Order.query.filter_by(order_id=order_id).first()):
#         order = Order.query.filter_by(order_id=order_id).all()
#         try:
#             for ord in order:
#                 db.session.delete(ord)    
#             db.session.commit()
#         except:
#             return jsonify({
#                 "code": 500,
#                 "message": "An error occurred deleting the order."
#                 }), 500 
        
#         print("-----Order has been cancelled!-----")
#         return redirect("http://localhost:8080/index.html", code=303)
    
    # return jsonify({
    #     "code": 404,
    #     "data": {
    #         "order_id": order_id
    #     },
    #     "message": "Order not found."
    #     }), 404

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

# @app.route("/order1/refund/<int:order_id>", methods=['PUT'])
# def update_refund(order_id):
#     if (Order.query.filter_by(order_id=order_id).first()):
#         try: 
#             orderMe = Order.query.filter_by(order_id=order_id).all()
#             for i in orderMe:
#                 if (i.refundStatus == False):
#                     i.refundStatus = True
#                     db.session.commit()
#                 else:
#                     i.refundStatus = False
#                     db.session.commit()
#         except:
#             return jsonify({
#                 "code": 500,
#                 "data": {
#                 "order_id": order_id
#                         },
#                 "message": "An error occurred updating the order."
#                 }), 500
        
#         return jsonify({
#                 "code": 201,
#                 "message": "Refund Status has been updated"
#                 }), 201 
    
#     return jsonify({
#         "code": 404,
#         "data": {
#             "order_ID": order_id
#         },
#         "message": "Order not found."
#         }), 404 

class Invoice(db.Model):
    __tablename__ = 'invoice'
    invoiceID = db.Column(db.Integer(), nullable=False, primary_key=True)
    customerEmail = db.Column(db.String(32),db.ForeignKey(customer.customerEmail), nullable=False)
    order_ID = db.Column(db.Integer(),db.ForeignKey(Order.order_id) ,nullable=False)
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
def get_all_invoice():
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
def find_invoice_by_orderID(order_ID):
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



# order_URL = "http://order:5001/order1"
# invoice_URL = "http://invoice:5002/invoice"

@app.route("/make_payment", methods=['POST'])
def make_payment():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            payment = request.get_json()
            print("\nReceived a payment request in JSON:", payment)

            # do the actual work
            # 1. Send order info {cart items}
            result = processPaymentRequest(payment)
            print(result)
            print(result["code"])
            return result["code"], jsonify(result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "make_payment.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processPaymentRequest(payment):
    # Send the order info {cart items}
    # Invoke the order microservice, calls the api /order1
    print('\n-----Invoking Order Microservice-----')
    order_result = create_order(payment)
    print('order_result:', order_result)
    code = order_result[1]
    if code not in range(200, 300):
        return {
            "code": 500,
            "data": {"order_result": order_result},
            "message": "Order creation failure."
            }     

    return {
        "code": 201,
        # "data": {
        #     "order_result": order_result
        #     # "invoice_result": invoice_result
        #     }
    }

def create_order(data):

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


@app.route("/make_payment/invoice/<string:invoice_id>")
def finalizePayment(invoice_id, session_id=None):
    # print('\n\n-----Publishing new order message with routing_key=announcement.msg-----')        
    # message = {
    #     "data": "New Order ID: " + str(invoice_id)
    #     }
    # message1 = json.dumps(message)

    # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="announcement.msg", 
    #     body=message1, properties=pika.BasicProperties(delivery_mode = 2))
    
    # print("\nOrder published to RabbitMQ Exchange.\n")

    print('\n-----Invoking Get OrderID-----')
    order_result = find_by_orderID(invoice_id)
    print('order_result:', order_result)

    totalMe = 0
    clothesMe = []
    for i in order_result['data']['order']:
        # print(i)
        totalMe += i['totalPrice']
        clothesMe.append(i['clothesName'])
    finalClothes = ', '.join(clothesMe)

    # Send invoice
    # record the invoice 
    print('\n\n-----Invoking Invoice Microservice-----')
    invoice = {'customerEmail': 'ahkao@gmail.com','order_ID': invoice_id, 
               'description': finalClothes, 'totalPrice': totalMe, 'payMethod': 'Card', 'stripe_id': '_blank'}
    invoice_result = create_an_invoice(invoice)
    print('invoice_result:', invoice_result)
    print("\nOrder sent to invoice.\n")
    
    code = invoice_result["code"]
    if code not in range(200, 300):
        return {
            "code": 500,
            "data": {"invoice_result": invoice_result},
            "message": "Invoice creation failure."
            } 

    # Get the session ID from the query parameters
    payment_intent = request.args.get('session_id')
    if payment_intent is None:
        payment_intent = session_id
    # Retrieve the PaymentIntent object
    checkout_session = stripe.checkout.Session.retrieve(payment_intent)
    payment_intent_id = checkout_session.payment_intent

    # Retrieve the PaymentIntent object to get the payment ID
    payment_intentMe = stripe.PaymentIntent.retrieve(payment_intent_id)
    payment_id = payment_intentMe.id
    # print(payment_id)
    print('\n-----Invoking Update of Invoice Stripe ID -----')
    stripe_id = update_invoice(invoice_id, payment_id)
    print('stripe_id_result:', stripe_id)
    code = stripe_id["code"]
    if code not in range(200, 300):
        return {
            "code": 500,
            "message": "Update of Invoice Stripe ID failure."
            }   

    # # print(invoice_id)
    # print('\n-----Invoking SMS -----')
    # sms_result = invoke_http(invoice_URL + "/" + str(invoice_id), method='GET')
    # print('sms_result:', sms_result)
    # code = sms_result["code"]
    # if code not in range(200, 300):
    #     return {
    #         "code": 500,
    #         "data": {"sms_result": sms_result},
    #         "message": "SMS creation failure."
    #         }   
    
    # totalAmt = 0
    # clothes = []
    # payMethod = sms_result["data"]["invoice"][0]["payMethod"]
    # for i in sms_result["data"]["invoice"]:
    #     totalAmt += float(i["price"])
    #     clothes.append(i["description"])
    
    # clothesList = ", ".join(clothes)

    # account_sid = "AC8fde687bceb07e79ffcc2dd38fbf8f0d"
    # auth_token = "c64beec77243d5148616dcb08c85b5dd"
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(
    # body="A charge of $" + str("{:.2f}".format(totalAmt)) + " has been made to your " + payMethod + " account\nOrdered: " + clothesList,
    # from_="+15673392848",
    # to="+6590664833" #can implement a loop to include different phone number
    # )
    # print("Following message has been successfully sent! ", message.sid)
    
    # #print(totalAmt, payMethod)

    return redirect("http://localhost:8080/index.html", code=303)
    
    # return {
    #     "code": 200,
    #     "data": {
    #         "sms_result": sms_result
    #         }
    # }

def create_an_invoice(data):
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

def update_invoice(order_id,data):
    if (Invoice.query.filter_by(order_ID=order_id).first()):
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


@app.route('/create-checkout-session/<string:product_ids>', methods=['GET'])
def create_checkout_session(product_ids):
    print('\n-----Invoking Stripe -----')
    productList = product_ids.split(",")
    print(productList)
    # 4242 4242 4242 4242
    testList = []
    testMe = []
    idx = 0
    for i in productList:
        # print(i)
        nameMe = ''
        if (idx % 2 == 1 and (idx + 1) != len(productList)):
            if (testMe[0] == 'Blue Shirt'):
                nameMe = 'price_1Mp3fWApb0N8o5GMsoJ4uN0w'
            elif (testMe[0] == 'Red Shirt'):
                nameMe = 'price_1Mp8ShApb0N8o5GMVFE2ngWR'
            elif (testMe[0] == 'Short sleeve waffle shirt in true navy'):
                nameMe = 'price_1Mp8Z7Apb0N8o5GM7iliidEQ' 
            elif (testMe[0] == 'Slim fit cotton oxford shirt in burgundy'):
                nameMe = 'price_1Mp8ZRApb0N8o5GMNp3gOHns' 
            elif (testMe[0] == 'Lettuce edge t-shirt in white'):
                nameMe = 'price_1Mp8ZkApb0N8o5GMchNfcks9' 
            elif (testMe[0] == 'Suny v neck t-shirt in black'):
                nameMe = 'price_1Mp8a3Apb0N8o5GMxUBcp3rm' 
            elif (testMe[0] == 'Cotton checkered shirt in cream'):
                nameMe = 'price_1Mp8aSApb0N8o5GMRYo8cLLT' 
            elif (testMe[0] == 'Cotton T-Shirt'):
                nameMe = 'price_1Mp8akApb0N8o5GMup0COuad' 
            elif (testMe[0] == 'Denim Jeans'):
                nameMe = 'price_1Mp8b3Apb0N8o5GMlffbU4d0' 
            elif (testMe[0] == 'Leather Jacket'):
                nameMe = 'price_1Mp8bLApb0N8o5GMvb6YS8yj' 
            elif (testMe[0] == 'Athletic Shorts'):
                nameMe = 'price_1Mp8bYApb0N8o5GMBiJ59O3x' 
            testList.append({'price': nameMe, 'quantity': int(i)})
            testMe = []
        else:
            testMe.append(i)
        idx += 1
    print(testList)
    try:
        checkout_session = stripe.checkout.Session.create(
        line_items=testList,
        mode='payment',
        success_url = finalizePayment(productList[-1]+'?session_id={CHECKOUT_SESSION_ID}'),
        cancel_url=delete_order(productList[-1])
        )
        checkout_session_success_url = checkout_session.success_url.replace('{CHECKOUT_SESSION_ID}', checkout_session.id)
        
    except Exception as e:
        print(str(e))
        return str(e)
    
    return redirect(checkout_session.url, code=303)


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

if __name__ == "__main__":
    print("This is flask for " + os.path.basename(__file__) + ": Everything")
    app.run(host='0.0.0.0', port=5000, debug=True)