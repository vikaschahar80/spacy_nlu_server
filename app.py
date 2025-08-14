import os
import glob
import re
import spacy
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# --- App and Database Configuration ---
app = Flask(__name__)
CORS(app)

# General Configurations
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "a-simple-secret-key-for-testing")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# --- Database Model Definition ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# --- spaCy Model Loading ---
def find_latest_model_path():
    """Finds the most recently created model directory."""
    model_dirs = glob.glob("output_model_*")
    if not model_dirs:
        return None
    latest_dir = max(model_dirs, key=os.path.getmtime)
    return os.path.join(latest_dir, "model-best")

latest_model = find_latest_model_path()
if not latest_model or not os.path.exists(latest_model):
    print("WARNING: Could not find a trained spaCy model. NLP features will be limited.")
    nlp = spacy.blank("en")
else:
    print(f"Loading latest model from: {latest_model}")
    nlp = spacy.load(latest_model)
    print("Model loaded successfully.")

# --- NLP Helper Functions (Your existing code) ---
def detect_intent(text):
    text = text.lower()
    if any(kw in text for kw in ["add", "create", "enroll", "insert"]): return "add_person"
    if any(kw in text for kw in ["edit", "change", "update", "move"]): return "edit_person"
    if any(kw in text for kw in ["block", "remove", "delete"]): return "block_person"
    if any(kw in text for kw in ["promote"]): return "promote_person"
    if any(kw in text for kw in ["get", "find", "show", "what", "who", "details"]): return "get_person_details"
    return "clarify_action"

def split_class_section(entities):
    if 'classSection' in entities:
        class_section_value = entities['classSection']
        match = re.match(r"(\d+)([A-Za-z]*)", class_section_value)
        if match:
            class_name, section = match.groups()
            entities['className'] = class_name
            if section:
                entities['section'] = section
            del entities['classSection']
    return entities

# --- API Endpoints ---

# THIS IS THE NEWLY ADDED ENDPOINT
@app.route("/api/register", methods=["POST"])
def register():
    """Endpoint for new user registration."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 409

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201

@app.route("/api/login", methods=["POST"])
def login():
    """Endpoint to log in and get a token."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token)

@app.route("/api/parse", methods=["POST"])
@jwt_required()
def parse_message():
    """Protected endpoint to parse user messages."""
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    doc = nlp(text)
    entities = {ent.label_: ent.text for ent in doc.ents}
    entities = split_class_section(entities)
    intent = detect_intent(text)
    # ... your existing NLP logic ...
    
    response_json = { "action": intent, "parameters": entities }
    return jsonify(response_json)

# --- Application Runner ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5005, debug=True)
