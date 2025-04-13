from flask import Flask, request, jsonify
import time, hmac, hashlib, base64

app = Flask(__name__)

# Change this to your actual secret key (keep it private!)
SECRET_KEY = b'your-very-secret-key'

@app.route('/')
def home():
    return 'Token Generator is Running.'

@app.route('/generate-token', methods=['POST'])
def generate_token():
    data = request.json
    url_prefix = data.get('url_prefix')

    if not url_prefix:
        return jsonify({"error": "Missing url_prefix"}), 400

    expires = int(time.time()) + 3600  # valid for 1 hour
    token_data = f"URLPrefix={url_prefix}~Expires={expires}"

    signature = hmac.new(SECRET_KEY, token_data.encode(), hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode().rstrip('=')

    token = f"{token_data}~Signature={encoded_signature}"
    return jsonify({"token": token})
