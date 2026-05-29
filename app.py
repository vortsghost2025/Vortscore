import os, sys
from flask import Flask, request, jsonify, render_template_string
from src.core.watchdog import verify_vault, update_manifest
from src.core.retrieval_engine import LocalRetrievalEngine
from src.core.memory_engine import MemoryEngine
from brain import get_ripple_payload

app = Flask(__name__)

@app.before_request
def guard():
    if not verify_vault():
        return jsonify({"error": "Integrity violation: Knowledge vault tampered."}), 403

retriever = LocalRetrievalEngine()

@app.route('/ripple', methods=['POST'])
def ripple():
    data = request.get_json(force=True) or {}
    text = data.get("text", "").strip()
    if not text: return jsonify({"error": "Null parameters"}), 400
    try:
        return jsonify(get_ripple_payload(text))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    template_path = os.path.join(os.getcwd(), "templates", "ripple.html")
    with open(template_path, 'r', encoding='utf-8') as f:
        return render_template_string(f.read())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
