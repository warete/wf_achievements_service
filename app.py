from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

from wfparser import run as parser_run

app = Flask(__name__, static_folder='assets')
# enable CORS
CORS(app, origins=['warete.lh1.in', 'localhost:3000'])

OUT_DIR = os.environ.get('OUT_DIR', None)
BASE_URL = os.environ.get('BASE_URL', None)
PARSE_ENDPOINT = os.environ.get('PARSE_ENDPOINT', None)
PARSE_ENDPOINT_SECRET = os.environ.get('PARSE_ENDPOINT_SECRET', None)


@app.route('/api/achievements', methods=['GET'])
def achievements():
    try:
        with open('assets/achievements.json') as f:
            response = json.load(f)
    except IOError:
        response = {
            'mark': [],
            'strip': [],
            'badge': []
        }

    return jsonify(response)


@app.route('/api/parse_achievements', methods=['GET'])
def parse_achievements():
    if request.args.get('secret') == PARSE_ENDPOINT_SECRET:
        data = parser_run(OUT_DIR, BASE_URL, PARSE_ENDPOINT)
        objects_count = len(data.mark) + len(data.strip) + len(data.badge)
        response = {
            'status': 'ok',
            'message': 'objects count: ' + objects_count
        }
        return jsonify(response)
    else:
        response = {
            'status': 'error',
            'message': 'access denied'
        }
        return jsonify(response), 403


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
