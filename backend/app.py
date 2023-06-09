from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
import logging

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
CORS(app, resources={r"/*": {"origins": "*", "methods": "*"}})

@app.route('/')
def hello_world():
    return 'Flask server running!'

@app.route('/create-database', methods=['POST'])
def create_database():
    db_list = mongo.db.list_collection_names()
    if "svg_collection" in db_list:
        print("Database already exists")
    else:
        mongo.db.create_collection("svg_collection")
        print("Database created")

@app.route('/upload-svg', methods=['POST'])
def upload_svg():
    if 'file' in request.files:
        svg_file = request.files['file']
        svg_data = svg_file.read()
        mongo.db.svg_collection.insert_one({'svg_data': svg_data})
        return 'SVG file uploaded successfully'
    elif 'svg_data' in request.json:
        svg_data = request.json['svg_data']
        mongo.db.svg_collection.insert_one({'svg_data': svg_data})
        return 'SVG data uploaded successfully'
    else:
        return 'No SVG file or data found', 400

@app.route('/api/blogs', methods=['GET'])
def get_blogs():
    blogs = []
    for blog in mongo.db.blogs.find():
        blogs.append({
            "_id": str(blog["_id"]),
            "postName": blog["postName"],
            "components": blog["components"]
        })
    #print('Blogs fetched from database: ', blogs)  # This line prints the blogs.
    result = jsonify(blogs)
    #print('Result: ', result)  # This line prints the result.
    return result

@app.route('/api/blogs', methods=['POST'])
def add_blog():
    data = request.get_json()
    new_blog = mongo.db.blogs.insert_one({
        "postName": data["postName"],
        "components": data["components"]
    })
    return jsonify({"_id": str(new_blog.inserted_id)})

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run()
