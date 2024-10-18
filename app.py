from flask import Flask, jsonify, request
from models import db, Student, Achievement
from ranking import calculate_rankings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_recognition.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@app.route('/achievements', methods=['POST'])
def add_achievement():
    data = request.json
    new_achievement = Achievement(student_id=data['student_id'], description=data['description'])
    db.session.add(new_achievement)
    db.session.commit()
    return jsonify({'message': 'Achievement added successfully!'}), 201

@app.route('/rankings', methods=['GET'])
def get_rankings():
    rankings = calculate_rankings()
    return jsonify(rankings)

if __name__ == '__main__':
    app.run(debug=True)
