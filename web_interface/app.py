"""
Flask Web Interface for Jarvis
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
import threading

from jarvis import Jarvis
from database.db_handler import DatabaseHandler
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize components
jarvis = Jarvis()
db = DatabaseHandler()

@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html')

@app.route('/api/command', methods=['POST'])
def process_command():
    """Process voice command via API"""
    try:
        data = request.json
        command = data.get('command', '').strip()
        
        if not command:
            return jsonify({'error': 'Empty command'}), 400
        
        # Process command
        response = jarvis.process_command(command)
        
        if response:
            return jsonify({
                'success': True,
                'command': command,
                'response': response
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No response generated'
            }), 400
    
    except Exception as e:
        logger.error(f"Command processing error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        interactions = db.get_interactions(limit)
        
        return jsonify({
            'success': True,
            'interactions': [
                {
                    'user': inter[0],
                    'response': inter[1],
                    'timestamp': inter[2]
                }
                for inter in interactions
            ]
        })
    
    except Exception as e:
        logger.error(f"History fetch error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    try:
        db.clear_interactions()
        jarvis.clear_history()
        
        return jsonify({
            'success': True,
            'message': 'History cleared'
        })
    
    except Exception as e:
        logger.error(f"Clear history error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get Jarvis status"""
    return jsonify({
        'success': True,
        'status': 'running',
        'version': '1.0.0',
        'active': jarvis.is_active
    })

@app.route('/api/voice-input', methods=['POST'])
def voice_input():
    """Handle voice input"""
    try:
        audio_data = request.files.get('audio')
        
        if not audio_data:
            return jsonify({'error': 'No audio provided'}), 400
        
        # Process audio and get response
        command = jarvis.voice_recognizer.recognize()
        response = jarvis.process_command(command)
        
        return jsonify({
            'success': True,
            'command': command,
            'response': response
        })
    
    except Exception as e:
        logger.error(f"Voice input error: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {error}")
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    logger.info(f"Starting Flask server on {FLASK_HOST}:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)