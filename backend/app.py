from flask import Flask, request, jsonify
import json
from replyToLabel import *
from label import *

app = Flask(__name__)

@app.route('/', methods=['POST'])
def result():
    data = request.data.decode('UTF-8')
    #print(data)  # raw data
    #print("data"+data.labelName)
    #print(request.json)  # json (if content-type of application/json is sent with the request)
    #print(jdata['labelName'])

    print(request.get_json(force=True))  # json (if content-type of application/json is not sent)
    jdata = request.get_json(force=True)
    if(jdata['service']=="send"):
        replyHandler(jdata['labelName'],
                    jdata['template'],
                    jdata['title'],
                    jdata['replyBody'],
                    jdata['tempType'])
    elif(jdata['service']=="label"):
        labelHandler(jdata['newLabelName'],
                    jdata['keyword'],
                    jdata['start'],
                    jdata['end'])
    return "gottcha!"