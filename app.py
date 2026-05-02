from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user="root",
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "blogdb"),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/health')
def health():
    return "OK", 200

@app.route('/posts', methods=['GET'])
def get_posts():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
    return jsonify(posts)

@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
        post = cursor.fetchone()
    return jsonify(post)

@app.route('/posts/add', methods=['POST'])
def add_post():
    data = request.json
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO posts (title, content) VALUES (%s, %s)",
            (data['title'], data['content'])
        )
    conn.commit()
    return jsonify({"message": "Post added successfully!"})

@app.route('/posts/delete/<int:id>', methods=['DELETE'])
def delete_post(id):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    conn.commit()
    return jsonify({"message": "Post deleted successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_DEBUG', '0') == '1')
