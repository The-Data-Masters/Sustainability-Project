from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mysqldb import MySQL
from datetime import timedelta

app = Flask(__name__)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mysql = MySQL(app)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Use env var in real apps
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    nom = data['nom']
    prenom = data['prenom']
    email = data['email']
    password = data['password']

    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (nom, prenom, email, password_hash) VALUES (%s, %s, %s)", (nom, prenom, email, pw_hash))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nom, prenom, password_hash FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.check_password_hash(user[2], password):
        token = create_access_token(identity={'id': user[0], 'name': user[1], 'email': email})
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    user = get_jwt_identity()
    return jsonify({'user': user}), 200
