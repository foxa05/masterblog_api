from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Choose a filename to store your blog posts
JSON_FILE = "posts.json"


def read_posts_from_file():
    # Read posts from the JSON file
    try:
        with open(JSON_FILE, 'r') as file:
            posts = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file does not exist or is not valid JSON, return an empty list
        posts = []
    return posts


def write_posts_to_file(posts):
    # Write posts to the JSON file
    with open(JSON_FILE, 'w') as json_file:
        json.dump(posts, json_file, indent=4)


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        data = request.get_json()
        # Read existing posts from the file
        posts = read_posts_from_file()

        post_to_update = next((post for post in posts if post['id'] == post_id), None)
        if post_to_update:
            post_to_update['title'] = data.get('title', post_to_update['title'])
            post_to_update['content'] = data.get('content', post_to_update['content'])

            # Write the updated posts back to the file
            write_posts_to_file(posts)

            return jsonify(post_to_update), 200
        else:
            return jsonify({"error": f"Post with id {post_id} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    # Read existing posts from the file
    posts = read_posts_from_file()

    # Filter out the post to be deleted
    updated_posts = [post for post in posts if post['id'] != post_id]

    # Check if the post was found and deleted
    if len(updated_posts) < len(posts):
        # Write the updated posts back to the file
        write_posts_to_file(updated_posts)
        return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200
    else:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    query = request.args.get('query', '').lower()

    # Read existing posts from the file
    posts = read_posts_from_file()

    matched_posts = [post for post in posts if
                     query in post['title'].lower() or
                     query in post['content'].lower()]

    return jsonify(matched_posts)


@app.route('/api/posts', methods=['GET'])
def get_posts_sorted():
    sort_by = request.args.get('sort', None)
    direction = request.args.get('direction', 'asc')

    valid_sort_fields = ['title', 'content']
    valid_directions = ['asc', 'desc']

    if sort_by and sort_by not in valid_sort_fields:
        return jsonify({"error": f"Invalid sort field. Valid values: {valid_sort_fields}"}), 400

    if direction not in valid_directions:
        return jsonify({"error": f"Invalid direction. Valid values: {valid_directions}"}), 400

    # Read existing posts from the file
    posts = read_posts_from_file()

    # Sort posts based on provided parameters
    if sort_by:
        posts.sort(key=lambda post: post[sort_by].lower(), reverse=(direction == 'desc'))

    return jsonify(posts)


if __name__ == '__main__':
    # Check if the JSON file exists, if not, create an empty one
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w') as file:
            json.dump([], file)
    app.run(host="0.0.0.0", port=5002, debug=True)
