from flask import Flask, jsonify
from flask_cors import CORS
import pipeline

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


pipeline.schedule_run()

# @app.route('/', methods=['GET'])
# async def webhook():
        
#     try:
        
#         return jsonify({"status": "healthy"}), 200
    
#     except Exception as e:
#         app.logger.error(f"Error: {e}")
#         return jsonify({"error": str(e)}), 500
        
        
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Perform any necessary checks here (e.g., database connection, etc.)
        # For now, we just return a simple success message
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        # If something goes wrong, return an error message
        return jsonify({"status": "unhealthy", "error": str(e)}), 500
                

# Run the Flask app
if __name__ == '__main__':
    app.run(port=8080, debug=True)