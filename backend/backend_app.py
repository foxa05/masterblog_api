from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)

@app.route('/api/add', methods=['POST'])
def add_post():
    try:
        data = request.get_json()
        if data and "title" in data and "content" in data:
            new_post = {
                "id": len(POSTS) + 1,
                "title": data["title"],
                "content": data["content"]
            }
            POSTS.append(new_post)
            return jsonify({"message": "Post added successfully", "post": new_post}), 201
        else:
            return jsonify({"error": "Missing 'title' or 'content' in request data"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
