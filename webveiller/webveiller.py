import sys
from flask import Flask, escape, request, jsonify, abort
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

sys.path.append('/Users/rpurp/dev/surveiller')
import interface
import config
import datetime
import utils


app = Flask(__name__)


if app.debug:
    config.FILE = "test/data.csv"
else:
    config.FILE = "data.csv"

def get_api_key():
    if app.debug:
        with open("api_key.txt") as f:
          return f.read().strip("\n")
    else:
        with open("api_key.txt") as f:
          return f.read().strip("\n")

api_key = get_api_key()

def requires_auth(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        json_data = request.get_json()
    
        token = json_data['token']
        auth = check_password_hash(get_api_key(), token)
        if auth:
            return f(*args, **kwargs)
        else:
            abort(401)
    return wrapped


@app.route('/api/start', methods=['POST'])
@requires_auth
def start():
    json_data = request.get_json()
    cat = json_data['category']
    task = json_data['task']
    start = json_data['start_datetime']
    interface.track(cat, task, start)
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp


@app.route('/api/end', methods=['POST'])
@requires_auth
def end():
    json_data = request.get_json()
    stop = json_data['end_datetime']

    interface.end(stop)
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp

@app.route('/api/cancel', methods=['POST'])
@requires_auth
def cancel():
    interface.cancel()
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp


@app.route('/api/status', methods=['GET'])
@requires_auth
def status():
    print(request.get_data())
    sys.stdout.flush() 

    return jsonify(status=interface.status())

@app.route('/api/progress', methods=['GET'])
@requires_auth
def progress():
    json_data = request.get_json()
    since = json_data["since"]
    info = interface.get_progress(since)
    info = {k : utils.seconds_to_readable_str(v) for k,v in info.items()}
    resp = jsonify(info=info)
    return resp

