#!flask/bin/python
from flask import Flask,request,jsonify,abort
import json

def parse_marathon_json(marathon_json):
   eventType = marathon_json['eventType']
   taskStatus = marathon_json['taskStatus']
   host = marathon_json['host']
   appId = marathon_json['appId']
   timestamp = marathon_json['timestamp']
   return {'appId':appId, 'timestamp':timestamp, 'host':host,'taskStatus':taskStatus, 'eventType':eventType}

def check_event(content):
    if content['eventType'] == 'status_update_event':
       marathonEventJson=parse_marathon_json(content)
    if marathonEventJson['taskStatus'] in {'TASK_FAILED','TASK_KILLED','TASK_LOST'}:
       print marathonEventJson


app = Flask(__name__)

@app.route('/', methods=['POST'])
def notify():
    content = request.get_json(silent=True)
    print content
    check_event(content)
    return jsonify({'notify': 'success'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7080, debug=True)
