from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.config_manager import ConfigManager
from core.disease_manager import DiseaseManager

def create_app():
    app = Flask(__name__, 
                template_folder='../ui/templates',
                static_folder='../ui/static')
    
    # Load configuration
    config_manager = ConfigManager()
    
    # Configure Flask
    app.config['SECRET_KEY'] = config_manager.get('api.secret_key', 'dev-key')
    app.config['DEBUG'] = config_manager.get('api.debug', True)
    
    # Enable CORS
    CORS(app)
    
    # Initialize disease manager
    try:
        disease_manager = DiseaseManager(config_manager)
        app.disease_manager = disease_manager
        print("✅ Disease manager initialized")
    except Exception as e:
        print(f"❌ Disease manager failed: {e}")
        app.disease_manager = None
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            data = request.get_json()
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return jsonify({'error': 'Message required'}), 400
            
            if not app.disease_manager:
                return jsonify({'error': 'System not ready'}), 500
            
            response = app.disease_manager.process_query(user_message)
            return jsonify(response)
            
        except Exception as e:
            return jsonify({
                'error': 'Server error',
                'ai_response': 'Sorry, please try again.',
                'metadata': {'error': True}
            }), 500
    
    @app.route('/api/diseases', methods=['GET'])
    def get_diseases():
        try:
            if not app.disease_manager:
                return jsonify({'error': 'System not ready'}), 500
            
            diseases = app.disease_manager.get_available_diseases()
            return jsonify(diseases)
        except Exception as e:
            return jsonify({'error': 'Failed to get diseases'}), 500
    
    @app.route('/api/diseases/<disease_name>/statistics', methods=['GET'])
    def get_disease_stats(disease_name):
        try:
            if not app.disease_manager:
                return jsonify({'error': 'System not ready'}), 500
            
            stats = app.disease_manager.get_disease_statistics(disease_name)
            return jsonify(stats)
        except Exception as e:
            return jsonify({'error': f'Failed to get {disease_name} stats'}), 500
    
    @app.route('/api/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'diseases_loaded': len(app.disease_manager.processors) if app.disease_manager else 0
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("\n🏥 Medical AI Chatbot Starting...")
    print("🌐 URL: http://localhost:5000")
    print("="*50)
    app.run(host='0.0.0.0', port=5000, debug=True)