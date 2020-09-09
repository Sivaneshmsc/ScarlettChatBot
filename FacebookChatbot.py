from waitress import serve
from flask import Flask, request
import requests
import BotEngine

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = 'EAAC3G1QAiUIBAJ5zQwVJE1ctCo50HtDDYZAZAo2druinm4Spr8xhGDNdWNAZCtkoTEXhG61ZAlfNaTZB9D7wlk1Y1al8xGC7ysdATNVkk976DyoZBJ50NKCf5kQDcjVYJ2WxyTb54syTTqC1U5ahURPKxjBUK6HgimXzVwz4ViR0auHDOQxs9b'# <paste your verify token here>
#PAGE_ACCESS_TOKEN = 'EAAN3skIIeiYBAPvC7edcYTwch9til0UjRu2DkhCyZCZBqq9XbglA0BkHkNSJgcFUZBmZCSX2FrRaWyxnDTNm95hjnHZBkB4h2hcHmFuWSYXnMsm8iazwZCnCoqCHZBGcXv21ZBfqt6NLEcnYYZCQLGrT7f1VZCgXPJC4bLZAEo64CWVMyuzwlVBM8X6'# paste your page access token here>"
PAGE_ACCESS_TOKEN = 'EAAC3G1QAiUIBAJ5zQwVJE1ctCo50HtDDYZAZAo2druinm4Spr8xhGDNdWNAZCtkoTEXhG61ZAlfNaTZB9D7wlk1Y1al8xGC7ysdATNVkk976DyoZBJ50NKCf5kQDcjVYJ2WxyTb54syTTqC1U5ahURPKxjBUK6HgimXzVwz4ViR0auHDOQxs9b'


def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    bot_resp = BotEngine.get_response(message)
    return bot_resp #"This is a dummy response to '{}'".format(message)


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    send_message(sender, response, message)

def respond_postback(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""

    send_message(sender, message, message)

def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))

def is_postback_message(message):
    """Check if the message is a message from the user"""
    return (message.get('postback') and
            message['postback'].get('payload') and
            not message['postback'].get("is_echo"))


@app.route("/webhook", methods=['GET','POST'])
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)
            if is_postback_message(x):
                text = x['postback']['payload']
                sender_id = x['sender']['id']
                respond_postback(sender_id, text)

        return "ok"

def structure_message(text, in_message):
    msg = {}
    if 'show me button' in str(in_message).lower():
        msg = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": 'Sample text with sample buttons',
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://www.amazingengineering.in",
                            "title": "Home"
                        },
                        {
                            "type": "web_url",
                            "url": "https://www.amazingengineering.in",
                            "title": "Contact"
                        }
                    ]
                }
            }
        }
    elif 'show me generic' in str(in_message).lower():
        msg = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Welcome !!!",
                            "image_url": "https://koenig-media.raywenderlich.com/uploads/2017/04/InAppPurchasesAutoRenew-feature-1.png",
                            "subtitle": "We have right products for everyone",
                            "default_action": {
                                "type": "web_url",
                                "url": "http://www.amazingengineering.in"
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": "http://www.amazingengineering.in",
                                    "title": "Website"
                                }
                            ]
                        }
                    ]
                }
            }
        }

    elif 'show me postback' in str(in_message).lower():
        msg = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": 'Sample text with sample buttons',
                    "buttons": [
                        {
                            "type": "postback",
                            "payload": "testing",
                            "title": "CLICK ME TO POSTBACK"
                        },
                        {
                            "type": "postback",
                            "payload": "DEVELOPER_DEFINED_PAYLOAD",
                            "title": "CLICK ME TO POSTBACK 2"
                        }
                    ]
                }
            }
        }
    elif 'show me video' in str(in_message).lower():
        msg = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "media",
                    "elements": [
                        {
                           "media_type": "video",
                           "url": "https://www.facebook.com/Formula1/videos/2597031500611521/"
                        }
                    ]
                }
            }
        }

    elif 'show me reply' in str(in_message).lower():
        msg = {
            "text": "Pick a color:",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Red",
                    "payload": "RedPostback",
                    "image_url": "http://example.com/img/red.png"
                },
                {
                    "content_type":"text",
                    "title":"Green",
                    "payload":"GreenPostback",
                    "image_url":"http://example.com/img/green.png"
                }
            ]
        }
    elif 'show me receipt' in str(in_message).lower():
        msg = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "receipt",
                    "recipient_name": "Sivanesh Vanmeeganathan",
                    "order_number": "12345678902",
                    "currency": "INR",
                    "payment_method": "Visa 2345",
                    "order_url": "http://petersapparel.parseapp.com/order?order_id=123456",
                    "timestamp": "1428444852",
                    "address": {
                      "street_1": "23, Kumaran Street",
                      "street_2": "T. Nagar",
                      "city": "Chennai",
                      "postal_code": "600035",
                      "state": "Tamil Nadu",
                      "country": "India"
                    },
                    "summary": {
                      "subtotal": 1650.00,
                      "shipping_cost": 50,
                      "total_tax": 373.8,
                      "total_cost": 3043.8
                    },
                    "adjustments": [
                      {
                        "name": "New Customer Discount",
                        "amount": 20
                      },
                      {
                        "name": "Rs. 10 Off Coupon",
                        "amount": 10
                      }
                    ],
                    "elements": [
                      {
                        "title": "Classic White T-Shirt",
                        "subtitle": "100% Soft and Luxurious Cotton",
                        "quantity": 2,
                        "price": 1980,
                        "currency": "INR",
                        "image_url": "https://images-na.ssl-images-amazon.com/images/I/61-TuCrKZ7L._SY550._SX._UX._SY._UY_.jpg"
                      },
                      {
                        "title": "Classic Gray T-Shirt",
                        "subtitle": "100% Soft and Luxurious Cotton",
                        "quantity": 1,
                        "price": 670,
                        "currency": "INR",
                        "image_url": "https://www.c-and-a.com/productimages/c_scale,h_1968,q_95,e_sharpen:70/v1521564125/2018531-1-08.jpg"
                      }
                    ]
                }
            }
        }
    elif 'show me multiple generic' in str(in_message).lower():
        msg = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Welcome !!!",
                            "image_url": "https://koenig-media.raywenderlich.com/uploads/2017/04/InAppPurchasesAutoRenew-feature-1.png",
                            "subtitle": "We have right products for everyone",
                            "default_action": {
                                "type": "web_url",
                                "url": "http://www.amazingengineering.in"
                            },
                            "buttons": [
                                {
                                    "type": "postback",
                                    "payload": "success",
                                    "title": "Open"
                                },
                                {
                                    "type": "web_url",
                                    "url": "http://www.amazingengineering.in",
                                    "title": "Add"
                                }
                            ]
                        },
                        {
                            "title": "Welcome 2 !!!",
                            "image_url": "https://www.inmobi.com/ui/uploads/blog/4_Path-to-retail.png",
                            "subtitle": "You can buy any products from anywhere",
                            "default_action": {
                                "type": "web_url",
                                "url": "http://www.amazingengineering.in"
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": "http://www.amazingengineering.in",
                                    "title": "Open"
                                },
                                {
                                    "type": "web_url",
                                    "url": "http://www.amazingengineering.in",
                                    "title": "Add"
                                }
                            ]
                        },
                        {
                            "title": "Welcome 3 !!!",
                            "image_url": "https://image.winudf.com/v2/image/Y29tLmFsbGlub25lLnB1cmNoYXNlX3NjcmVlbl80XzE1Mjk3NjEyODVfMDkz/screen-4.jpg?fakeurl=1&type=.jpg",
                            "subtitle": "You can buy any products from any device",
                            "default_action": {
                                "type": "web_url",
                                "url": "http://www.amazingengineering.in"
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": "http://www.amazingengineering.in",
                                    "title": "Open"
                                },
                                {
                                    "type": "web_url",
                                    "url": "http://www.amazingengineering.in",
                                    "title": "Add"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    else:
        msg = {
            "text": text
        }

    return msg

def send_message(recipient_id, text, in_message):
    """Send a response to Facebook"""
    payload = {
        'message': structure_message(text, in_message),
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'REGULAR'
    }

    # payload = {
    #     'recipient': {
    #         'id': recipient_id
    #     },
    #     "get_started": {
    #         "payload": "GET_STARTED_PAYLOAD"
    #     },
    #     'notification_type': 'REGULAR'
    # }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )
    print(response.json())
    return response.json()


serve(app, host='localhost', port=8877)