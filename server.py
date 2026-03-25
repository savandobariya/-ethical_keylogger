from flask import Flask, request, jsonify
import json
import base64
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def receive_log():
    """Simulated endpoint to receive exfiltrated data"""
    try:
        data = request.json
        encrypted_data = base64.b64decode(data['data'])
        
        # Log the received data
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "client_id": data.get('client_id'),
            "data_size": len(encrypted_data),
            "status": "received"
        }
        
        # Save to server logs
        if not os.path.exists("server_logs"):
            os.makedirs("server_logs")
        
        with open("server_logs/received_logs.json", 'a') as f:
            json.dump(log_entry, f)
            f.write("\n")
        
        return jsonify({"status": "success", "message": "Data received"}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/status', methods=['GET'])
def status():
    """Server status endpoint"""
    return jsonify({
        "status": "running",
        "purpose": "Educational demo server",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    print("Starting mock exfiltration server on http://localhost:8080")
    print("This is for educational purposes only")
    app.run(host='localhost', port=8080, debug=True)