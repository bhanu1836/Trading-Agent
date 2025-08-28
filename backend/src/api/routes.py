from flask import Blueprint, request, jsonify
from services.langchain_service import process_command

api = Blueprint('api', __name__)

@api.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    command = data.get('command')
    
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
    response = process_command(command)
    
    return jsonify({'response': response})