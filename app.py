from flask import Flask, request, jsonify
import mysql.connector as sql

app = Flask(__name__)

def db_connection():
    return sql.connect(host="localhost", user="root", passwd="nishita123", database="go_fit")

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    db = db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT MAX(user_id) FROM users")
    user_id = cursor.fetchone()[0] + 1 if cursor.fetchone() else 101

    query = "INSERT INTO users (user_id, user_name, passw, gen, age, subscription) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (user_id, data['username'], data['password'], data['gender'], data['age'], data['subscription'])

    cursor.execute(query, values)
    db.commit()
    db.close()

    return jsonify({"message": "Signup Successful!", "user_id": user_id})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    db = db_connection()
    cursor = db.cursor()

    query = "SELECT * FROM users WHERE user_id = %s AND passw = %s"
    values = (data['user_id'], data['password'])

    cursor.execute(query, values)
    user = cursor.fetchone()
    db.close()

    if user:
        return jsonify({"message": "Login Successful!", "success": True})
    else:
        return jsonify({"message": "Invalid Credentials", "success": False})

if __name__ == '__main__':
    app.run(debug=True)
