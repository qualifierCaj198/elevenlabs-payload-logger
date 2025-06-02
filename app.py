from flask import Flask, request, jsonify
import logging
import json
import os
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/webhook", methods=["POST"])
def capture_payload():
    try:
        data = request.get_json(force=True)
        timestamp = datetime.utcnow().isoformat()

        # Log to console (Render logs)
        logging.info("📥 Webhook received at %s: %s", timestamp, json.dumps(data, indent=2))

        # Optional: Save to file (useful for local testing)
        with open("latest_payload.json", "w") as f:
            json.dump(data, f, indent=2)

        return jsonify({"status": "received"}), 200
    except Exception as e:
        logging.exception("❌ Failed to process payload")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
