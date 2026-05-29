from flask import Flask, request, jsonify
from src.devcore.vitalis_cognitive_engine import VitalisCognitiveEngine

app = Flask(__name__)
engine = VitalisCognitiveEngine()

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    # Ensure mandatory fields
    if not all(k in data for k in ("intent", "token")):
        return jsonify({"error": "Missing intent or token"}), 400
    
    # Execute intent through the hardened engine
    result = engine.think_and_act(
        intent=data['intent'], 
        token=data['token'], 
        module_name=data.get('module_name')
    )
    
    status_code = 200 if result.get("success") else 403
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
