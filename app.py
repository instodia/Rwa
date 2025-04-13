from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import time
import hmac
import hashlib

app = Flask(__name__)
CORS(app)  # <--- Add this line

SECRET_KEY = b'3f74459e-14f6-4d50-8de7-50d7a1677cbf'

@app.route('/generate-token', methods=['POST'])
def generate_token():
    data = request.json
    url_prefix = data.get('url_prefix')
    if not url_prefix:
        return jsonify({'error': 'url_prefix is required'}), 400

    expires = int(time.time()) + 86400
    url_prefix_encoded = base64.urlsafe_b64encode(url_prefix.encode()).decode().rstrip('=')
    string_to_sign = f'URLPrefix={url_prefix_encoded}~Expires={expires}'
    signature = hmac.new(SECRET_KEY, string_to_sign.encode(), hashlib.sha256).digest()
    signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip('=')

    token = f'URLPrefix={url_prefix_encoded}~Expires={expires}~Signature={signature_encoded}'
    return jsonify({'token': token})
