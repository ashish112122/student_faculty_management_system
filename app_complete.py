from flask import Flask, request, jsonify
from flask_cors import CORS
import oracledb
import jwt
import datetime
from functools import wraps
import os
from backend.config import Config

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = Config.SECRET_KEY

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def get_db_connection():
    return oracledb.connect(**DB_CONFIG)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_id = data['user_id']
            request.role = data['role']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    return "Backend running successfully"

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'message': 'Email and password required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT user_id, name, role, password
                FROM users
                WHERE email = :email
            """, {'email': email})
            
            user = cursor.fetchone()
            
            if not user or password != user[3]:
                return jsonify({'message': 'Invalid email or password'}), 401
            
            user_id, name, role = user[0], user[1], user[2]
            
            token = jwt.encode({
                'user_id': user_id,
                'role': role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            return jsonify({
                'token': token,
                'user_id': user_id,
                'name': name,
                'role': role,
                'message': 'Login successful'
            })
        
        finally:
            cursor.close()
            conn.close()
    
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'message': 'Server error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
