from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.trading_agent import TradingAgent
import os
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for Chrome extension

# Initialize trading agent
try:
    agent = TradingAgent()
    print("Trading agent initialized successfully!")
except Exception as e:
    print(f"Error initializing trading agent: {e}")
    agent = None

@app.route('/process_command', methods=['POST'])
def process_command():
    try:
        if not agent:
            return jsonify({"error": "Trading agent not initialized"}), 500
            
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400
            
        command = data.get('command', '')
        page_context = data.get('page_context', {})
        
        print(f"Processing command: {command}")
        print(f"Page context: {page_context}")
        
        result = agent.process_command(command, page_context)
        print(f"Result: {result}")
        
        return jsonify(result)
    except Exception as e:
        error_msg = f"Error processing command: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return jsonify({"error": error_msg}), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        if not agent:
            return jsonify({"status": "error", "message": "Agent not initialized"}), 500
        return jsonify({"status": "healthy", "model_info": agent.get_model_info()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "Backend is working!"})

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, port=8000, host='0.0.0.0')