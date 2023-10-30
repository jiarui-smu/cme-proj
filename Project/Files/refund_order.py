from flask import Flask, request, jsonify
from flask_cors import CORS
from twilio.rest import Client
import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51Ml6VEApb0N8o5GMbfEwVXAQn6XxeoXwm8OI7p2KvhjGjER9XiUxdRsWBVsYrLqpiZZeVadJA3vtJjkIKCQ54MhL00GGOAgzKX'

import os, sys

import requests
from invokes import invoke_http
import json

app = Flask(__name__)
CORS(app)

order_URL = "http://order:5001/order1"
customer_url = "http://customer:5003/customer" ## customer microservice 
refund_url = "http://refund:5010/refund/" ## refund microservice (to keep track of refundpaymente ID etc
invoice_URL = "http://invoice:5002/invoice/"

# Make a request to flask application to retrieve customer phone number tied to the customerEmail
@app.route("/refund_order", methods=['POST'])
def refund_order():
    if request.is_json:
        try:
            refund_info = request.get_json()
            print("\nReceived a refund request in JSON:",  refund_info)
            # do the actual work
            # 1. Send order info {cart items}
            result = processRefundRequest(refund_info)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "refund_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processRefundRequest(refund_info):
    # Fetch the customer phone number from the customer microservice
    # Invoke customer microservice
    print('\n-----Invoking Customer Microservice-----')
    print(refund_info)
    order_id = refund_info[0]
    customer_email = refund_info[1]
    result1 = invoke_http(customer_url + "/" + customer_email, method='GET')
    print('customer_result:', result1) #result contains a JSON of customer_email and customer number
    code = result1["code"]
    if code not in range(200, 300):
        return {
            "code": 500,
            "data": {"Customer_result": result1},
            "message": "Customer cannot be found."
          } 
    
    print('\n-----Invoking Update of Order Microservice-----')
    #print(order_id)
    # changeOrder = {'order_id': order_id, 'clothesName': clothes_name}
    result = invoke_http(order_URL + "/" + str(order_id), method='PUT')
    print('change_result:', result) 
    code = result["code"]
    if code not in range(200, 300):
        return {
            "code": 500,
            "data": {"Order_ID": order_id},
            "message": "Order cannot be found."
          } 
    
    #Invoking invoice to get the stripe_id to invoke a refund at stripe
    print('\n\n-----Invoking Invoice Microservice-----')
    stripeMe = invoke_http(invoice_URL + str(order_id), method='GET')
    print('stripe_id_Result:', stripeMe)
    stripeID = stripeMe['data']['invoice'][0]['stripe_id']
    stripe.Refund.create(payment_intent=stripeID)
    print("\nStripe Refund was successful\n")

    print('\n\n-----Invoking SMS-----')
    customerNumber = result1['data']['PhoneNum']
    account_sid = "AC8fde687bceb07e79ffcc2dd38fbf8f0d"
    auth_token = "c64beec77243d5148616dcb08c85b5dd"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    body="You have been refunded $" + str("{:.2f}".format(stripeMe['data']['invoice'][0]['price'])) + " for the purchase of a " + stripeMe['data']['invoice'][0]['description'],
    from_="+15673392848",
    to="+65" + customerNumber  #can implement a loop to include different phone number
    )
    print("Following message has been successfully sent! ", message.sid)
    
    code = stripeMe["code"]
    if code not in range(200, 300):
        return {
            "code": 500,
            "message": "Stripe refund was unsuccessful"
            }
    
    print('\n\n-----Invoking Refund Microservice-----')
    refund_transaction = {'customerEmail':customer_email, 'description':stripeMe['data']['invoice'][0]['description'], 'refundAmt':stripeMe['data']['invoice'][0]['price'], 'phoneNum':customerNumber}
    refund_creation_Result = invoke_http(refund_url, method='POST', json=refund_transaction)
    print('refund_creation_Result:', refund_creation_Result)
    print("\nRefund was successful & SMS has been sent.\n")
    
    code = refund_creation_Result["code"]
    if code not in range(200, 300):
        return {
            "code": 500,
            "data": {"refund_creation_Result": refund_creation_Result},
            "message": "Refund was unsuccessful."
            }   

    return {
        "code": 201,
    }


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing a refund request...")
    app.run(host="0.0.0.0", port=5111, debug=True)