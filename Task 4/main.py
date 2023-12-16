from flask import Flask, request, jsonify
import psycopg2
import random

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="postgres",
    user="hritik_rohilla",
    password="Qwerty",
    host="localhost"
)
cur = conn.cursor()

# don't forget to run below sql query in postgres sql if someone want to run this code

""" CREATE TABLE quiz_results (
       id SERIAL PRIMARY KEY,
       user_id INTEGER,
       quiz_number INTEGER,
       completed BOOLEAN
   ); """


# use this body to access { "user_id": "52039848", "quiz_number": 1 }
# you can generate a new user_id by hitting http://127.0.0.1:5000/register_user

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    user_id = request.json.get('user_id')
    quiz_number = int(request.json.get('quiz_number'))

    if can_start_quiz(user_id, quiz_number):
        return jsonify({"message": "Quiz started"}), 200
    else:
        return jsonify({"message": "You can't start this quiz yet"}), 400


def can_start_quiz(user_id, quiz_number):
    cur.execute("SELECT COUNT(*) FROM quiz_results WHERE user_id = %s AND quiz_number = %s", (user_id, quiz_number - 1))
    previous_quiz_count = cur.fetchone()[0]

    if quiz_number == 1:
        return True  # First quiz can always be started
    elif previous_quiz_count > 0:  # The previous quiz exists
        return True
    else:
        return False


# hit this using postman foir submitting every quiz http://127.0.0.1:5000/submit_quiz 
# json BOdy { "user_id": "52039848", "quiz_number": 1 } write quiz number which ever you want to submit
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    user_id = request.json.get('user_id')
    quiz_number = request.json.get('quiz_number')

    cur.execute("INSERT INTO quiz_results (user_id, quiz_number) VALUES (%s, %s)", (user_id, quiz_number))
    conn.commit()
    return jsonify({"message": "Quiz submitted"}), 200


@app.route('/register_user')
def register_user():
    # Logic for registering a new user
    user_id = generate_user_id()  # Generate a new user ID
    return jsonify({"user_id": user_id}), 201


def generate_user_id():
    new_user_id = random.randint(10000000, 99999999)
    return new_user_id


if __name__ == '__main__':
    app.run()
