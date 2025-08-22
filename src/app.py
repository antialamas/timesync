from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import numpy as np
from simulation.quantum_channel import QuantumChannelSimulator
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize simulator
simulator = QuantumChannelSimulator()

@app.route('/')
def index():
    """Serve a simple test page"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <h1>Test Page</h1>
        <p>If you can see this, the server is working correctly.</p>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    try:
        static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
        logger.debug(f"Attempting to serve {path} from {static_dir}")
        return send_from_directory(static_dir, path)
    except Exception as e:
        logger.error(f"Error serving {path}: {str(e)}")
        return str(e), 500

@app.route('/api/simulate', methods=['POST'])
def run_simulation():
    """Run quantum channel simulation with provided parameters"""
    try:
        # Get parameters from request
        params = request.get_json()
        logger.debug(f"Received simulation parameters: {params}")
        
        # Convert parameters to simulation format
        config = {
            'alice': {
                'mu1': float(params['alice']['mu1']),
                'mu2': float(params['alice']['mu2']),
                'p1': float(params['alice']['p1'])
            },
            'bob': {
                'darkCount': float(params['bob']['darkCount']),
                'timeBin': float(params['bob']['timeBin'])
            },
            'channel': {
                'loss': float(params['channel']['loss']),
                'syncError': float(params['channel']['syncError'])
            },
            'processing': {
                'blockSize': int(params['processing']['blockSize']),
                'maxOffset': int(params['processing']['maxOffset'])
            }
        }
        
        # Run simulation
        results = simulator.run(config)
        logger.debug("Simulation completed successfully")
        
        return jsonify({
            'status': 'success',
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Error in simulation: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Quantum channel simulation server is running'
    })

if __name__ == '__main__':
    # Get static directory path
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    # Verify static directory exists
    if not os.path.isdir(static_dir):
        raise Exception(f"Static directory not found: {static_dir}")
    
    # List contents of static directory
    logger.info("Static directory contents:")
    for root, dirs, files in os.walk(static_dir):
        level = root.replace(static_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        logger.info(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            filepath = os.path.join(root, f)
            perms = oct(os.stat(filepath).st_mode)[-3:]
            logger.info(f"{subindent}{f} (permissions: {perms})")
            
    # Print paths for debugging
    logger.info(f"Static directory: {static_dir}")
    logger.info(f"Current working directory: {os.getcwd()}")
    
    app.run(debug=True, port=5000)