import requests, json

TOKEN = "CWB-6DBD16F3-06CE-4EB3-8123-BBBEF41F6C74"
LINK = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0014-001?Authorization=CWB-6DBD16F3-06CE-4EB3-8123-BBBEF41F6C74&format=JSON&sort=time"

### 中央氣象局開放資料平臺之資料擷取API
# https://opendata.cwb.gov.tw/dist/opendata-swagger.html

### 氣象資料開放平台
# https://opendata.cwb.gov.tw/index#

### Learning Objective
# 1. Data Observation
#   * Paras: event
#   * Req: API(Package Upload)
#   * Func: Close, Delegate
# 2. Event Bridge With CloudWatch
# https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents-expressions.html
# https://docs.aws.amazon.com/lex/latest/dg/API_runtime_DialogAction.html
# https://docs.aws.amazon.com/lex/latest/dg/lambda-input-response-format.html
# https://docs.aws.amazon.com/lex/latest/dg/API_runtime_ResponseCard.html

def lambda_handler(event,context):
    print("="*30 + "【START】Eevent Data " +"="*30)
    # print(event)
    print("="*30 + "【END】Event Data " +"="*30)

    headers = {
        "accept" : "application/json"
    }

    resp = requests.get(LINK,headers=headers)
    
    if all(event['currentIntent']['slots'].values()):
        if resp.status_code == 200:
            warning_data = resp.json()['records']['tsunami'][-1]
            # print(
            #     warning_data['reportContent'],
            #     warning_data['earthquakeInfo']['originTime'],
            #     warning_data['earthquakeInfo']['epiCenter']['location']
            # )
            return close(
                event['sessionAttributes'],
                'Fulfilled',
                {   
                    'contentType': 'PlainText',
                    'content': f'Tsunami Content: {warning_data["reportContent"]}, OriginTime: {warning_data["earthquakeInfo"]["originTime"]}, Location: {warning_data["earthquakeInfo"]["epiCenter"]["location"]}'
                }
            )
    else:
        return delegate(
            event['sessionAttributes'],
            event['currentIntent']['slots']
        )

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }

def close(session_attributes, fulfillment_state, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }

def resp_card(session_attributes):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                "contentType": "application/vnd.amazonaws.card.generic",
                "genericAttachments": [{
                    "attachmentLinkUrl": "null",
                    "buttons": [{
                        "text": "Click Me",
                        "value": "www.google.com"
                    }],
                    "imageUrl": "https://goodder.co/assets/img/%E9%A6%96%E9%A0%81Banner.39668a99.png",
                    "subTitle": "This is subtitle",
                    "title": "This is title"
                }],
                "version": "1"
            }
        }
    }

