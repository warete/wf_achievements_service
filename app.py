from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

import parser

app = Flask(__name__, static_folder='assets')
# enable CORS
CORS(app, origins=['warete.lh1.in', 'localhost:3000'])

OUT_DIR = os.environ.get('OUT_DIR', None)
BASE_URL = os.environ.get('BASE_URL', None)
PARSE_ENDPOINT = os.environ.get('PARSE_ENDPOINT', None)


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


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
