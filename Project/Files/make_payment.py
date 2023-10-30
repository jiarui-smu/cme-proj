from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from twilio.rest import Client
import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51Ml6VEApb0N8o5GMbfEwVXAQn6XxeoXwm8OI7p2KvhjGjER9XiUxdRsWBVsYrLqpiZZeVadJA3vtJjkIKCQ54MhL00GGOAgzKX'

import os, sys
import pika
import requests
from invokes import invoke_http
import json
import amqp_setup

app = Flask(__name__)
CORS(app)

order_URL = "http://order:5001/order1"
invoice_URL = "http://invoice:5002/invoice"

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
            return jsonify(result), result["code"]

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
    # Invoke the order microservice
    print('\n-----Invoking Order Microservice-----')
    order_result = invoke_http(order_URL, method='POST', json=payment)
    print('order_result:', order_result)
    code = order_result["code"]
    if code not in range(200, 300):
        return {
            "code": 500,
            "data": {"order_result": order_result},
            "message": "Order creation failure."
            }     

    return {
        "code": 201,
        "data": {
            "order_result": order_result
            # "invoice_result": invoice_result
            }
    }

@app.route("/make_payment/invoice/<string:invoice_id>")
def finalizePayment(invoice_id):
    print('\n\n-----Publishing new order message with routing_key=announcement.msg-----')        
    message = {
        "data": "New Order ID: " + str(invoice_id)
        }
    message1 = json.dumps(message)

    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="announcement.msg", 
        body=message1, properties=pika.BasicProperties(delivery_mode = 2))
    
    print("\nOrder published to RabbitMQ Exchange.\n")

    print('\n-----Invoking Get OrderID-----')
    order_result = invoke_http(order_URL + '/' + str(invoice_id), method='GET')
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
    invoice_result = invoke_http(invoice_URL, method="POST", json=invoice)
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

    # Retrieve the PaymentIntent object
    checkout_session = stripe.checkout.Session.retrieve(payment_intent)
    payment_intent_id = checkout_session.payment_intent

    # Retrieve the PaymentIntent object to get the payment ID
    payment_intentMe = stripe.PaymentIntent.retrieve(payment_intent_id)
    payment_id = payment_intentMe.id
    # print(payment_id)
    print('\n-----Invoking Update of Invoice Stripe ID -----')
    stripe_id = invoke_http(invoice_URL + "/" + str(invoice_id), method='PUT', json=payment_id)
    print('stripe_id_result:', stripe_id)
    code = stripe_id["code"]
    if code not in range(200, 300):
        return {
            "code": 500,
            "message": "Update of Invoice Stripe ID failure."
            }   

    # print(invoice_id)
    print('\n-----Invoking SMS -----')
    sms_result = invoke_http(invoice_URL + "/" + str(invoice_id), method='GET')
    print('sms_result:', sms_result)
    code = sms_result["code"]
    if code not in range(200, 300):
        return {
            "code": 500,
            "data": {"sms_result": sms_result},
            "message": "SMS creation failure."
            }   
    
    totalAmt = 0
    clothes = []
    payMethod = sms_result["data"]["invoice"][0]["payMethod"]
    for i in sms_result["data"]["invoice"]:
        totalAmt += float(i["price"])
        clothes.append(i["description"])
    
    clothesList = ", ".join(clothes)

    account_sid = "AC8fde687bceb07e79ffcc2dd38fbf8f0d"
    auth_token = "c64beec77243d5148616dcb08c85b5dd"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    body="A charge of $" + str("{:.2f}".format(totalAmt)) + " has been made to your " + payMethod + " account\nOrdered: " + clothesList,
    from_="+15673392848",
    to="+6590664833" #can implement a loop to include different phone number
    )
    print("Following message has been successfully sent! ", message.sid)
    
    #print(totalAmt, payMethod)

    return redirect("http://localhost:8080/index.html", code=303)
    
    # return {
    #     "code": 200,
    #     "data": {
    #         "sms_result": sms_result
    #         }
    # }

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
        success_url='http://localhost:5100/make_payment/invoice/' + productList[-1] + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://localhost:5001/order1/deleteMe/' + productList[-1],
        )
        checkout_session_success_url = checkout_session.success_url.replace('{CHECKOUT_SESSION_ID}', checkout_session.id)
        
    except Exception as e:
        print(str(e))
        return str(e)
    
    return redirect(checkout_session.url, code=303)


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing a payment request...")
    app.run(host="0.0.0.0", port=5100, debug=True)