from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies
import psycopg2
from datetime import timedelta

app = Flask(__name__)

# Database connection setup
conn = psycopg2.connect(
    dbname="postgres",
    user="hritik_rohilla",
    password="Qwerty",
    host="localhost"
)
cur = conn.cursor()

# don't forget to run below sql query in postgres sql if someone want to run this code
""" CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       username VARCHAR(50) UNIQUE NOT NULL,
       password VARCHAR(80) NOT NULL
   ); """

# Configure application to store JWTs in cookies
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)


@app.route('/')
def home():
    return 'Please access this  http://127.0.0.3:8080/register using Postman or ThunderClient in VS code to \
        Register your user {"username": "your username","password": "your password" } and login using this http://127.0.0.3:8080/login \
        {"username": "postgres", "password": "Qwerty"}'


@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    cur.execute(
        "SELECT * FROM users WHERE username = %s and password = %s", (username, password))
    user = cur.fetchone()

    if user:
        access_token = create_access_token(identity=username)
        response = jsonify(access_token=access_token)
        set_access_cookies(response, access_token)
        return response, 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

if __name__ == '__main__':
    app.run(host='127.0.0.3', port=8080, debug=True)