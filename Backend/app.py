from flask import Flask
from routes.ocr_routes import ocr_bp
from routes.plate_routes import plate_bp
from routes.admin_routes import admin_bp
from flask_cors import CORS

app = Flask(__name__)


# Enable CORS for specific origin (your frontend URL)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

app.register_blueprint(plate_bp, url_prefix="/api")
app.register_blueprint(ocr_bp, url_prefix='/ocr-api')
app.register_blueprint(admin_bp, url_prefix="/admin")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
