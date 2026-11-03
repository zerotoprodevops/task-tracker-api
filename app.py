from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# Connect to MongoDB using the Kubernetes Service name
# We use an environment variable here to practice ConfigMaps later
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongo-service:27017/mydb')
client = MongoClient(MONGO_URI)
db = client.mydb
tasks_collection = db.tasks

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = list(tasks_collection.find({}, {'_id': 0}))
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Missing title"}), 400
    
    new_task = {"title": data['title'], "completed": False}
    tasks_collection.insert_one(new_task)
    return jsonify({"message": "Task added!", "task": new_task}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)