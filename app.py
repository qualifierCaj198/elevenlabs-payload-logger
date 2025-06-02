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

        # Log to Render logs
        logging.info("📥 Webhook received at %s:\n%s", timestamp, json.dumps(data, indent=2))

        # Optional: save locally (only works when running locally)
        with open("latest_payload.json", "w") as f:
            json.dump(data, f, indent=2)

        return jsonify({"status": "received"}), 200

    except Exception as e:
        logging.exception("❌ Failed to process payload")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
