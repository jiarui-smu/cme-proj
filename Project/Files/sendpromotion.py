from flask import Flask, request, jsonify
from flask_cors import CORS
from twilio.rest import Client

import os, sys, amqp_setup

import requests
from invokes import invoke_http

import pika
import json

app = Flask(__name__)
CORS(app)
app.secret_key = 'my_secret_key'

clothes_URL = "http://clothes:5000/clothes"
customer_URL = "http://customer:5003/customer"



@app.route("/sendpromo")
def send_promo():
    try:
        #code to send sms
        promo_msg = "Fashion Fiesta's "
        clothes = getclothesnamebypromo() #function gets a list of clothes name that is on promo
        for clothe in clothes:
            promo_msg += clothe
            promo_msg += ", "
        
        promo_msg += " is on Promotion!!"
        #print("promoMe", promo_msg)
        numbers = getcustomerdata()
        #print("testing", numbers)
        # Your Account SID from twilio.com/console
        account_sid = "AC8fde687bceb07e79ffcc2dd38fbf8f0d"
        auth_token = "c64beec77243d5148616dcb08c85b5dd"

        client = Client(account_sid, auth_token)
        #uncommment after testing
        for num in numbers:
            num = "+65"+num
        
        # for number in numbers: 
        #     message = client.messages.create(
        #         body=promo_msg,
        #         from_='+15674831731',
        #         to=number
        #     )
        #     #print(message.status) #status of message, queued = success
        message = client.messages.create(
                body=promo_msg,
                from_='+15673392848',
                to='+6590664833') 
        # #print("Following message has been successfully sent! ", message.sid)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="promo.promo", 
        body=promo_msg, properties=pika.BasicProperties(delivery_mode = 2))
        return {
        "code": 200,
        "data": {
            "sms_result": "Following numbers have received the SMS: " + ', '.join(numbers),
            "sms":promo_msg
            }
    }
    except Exception as e:
        # Unexpected error in code
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)

        return jsonify({
            "code": 500,
            "message": "sendpromotion.py internal error: " + ex_str
        }), 500


## returns a list of clothes name that is on promotion
def getclothesnamebypromo():
    print('\n-----Invoking clothes microservice-----')
    clothes = invoke_http(clothes_URL, method='GET')
    print('customer_num:', clothes)
    code = clothes["code"]
    if code not in range(200, 300):
        return {
            "code": 500,
            "data": {"Clothes": clothes},
            "message": "Clothes failure sent for error handling."
            } 
    
    clothes_promo = []
    for cloth in clothes['data']['clothes']:
        if cloth['isOnPromotion'] == True:
            clothes_promo.append(cloth['name'])

    return clothes_promo


## returns a list of customer number
def getcustomerdata(): 
    print('\n-----Invoking customer microservice-----')
    customer_num = invoke_http(customer_URL+"/number", method='GET')
    print('customer_num:', customer_num)
    code = customer_num["code"]
    if code not in range(200, 300):
        return {
            "code": 500,
            "data": {"customer_num": customer_num},
            "message": "Customer failure sent for error handling."
            }  
    return customer_num['data']['num'] 


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing a send promo...")
    app.run(host="0.0.0.0", port=5007, debug=True)