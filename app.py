from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'designers.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Designer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    projects = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(10), nullable=False)
    phones = db.Column(db.String(500))  # Store JSON as string

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'rating': self.rating,
            'description': self.description,
            'projects': self.projects,
            'experience': self.experience,
            'price': self.price,
            'phones': json.loads(self.phones) if self.phones else []
        }

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        # Removed sample data initialization
        print("✅ Database initialized")

# API Routes
@app.route('/api/designers', methods=['GET'])
def get_designers():
    designers = Designer.query.all()
    return jsonify([designer.to_dict() for designer in designers])

@app.route('/api/designers', methods=['POST'])
def add_designer():
    data = request.json
    new_designer = Designer(
        name=data['name'],
        rating=data['rating'],
        description=data['description'],
        projects=data['projects'],
        experience=data['experience'],
        price=data['price'],
        phones=json.dumps(data['phones'])
    )
    db.session.add(new_designer)
    db.session.commit()
    return jsonify(new_designer.to_dict()), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)