import os

import pymongo
from flask import Flask, jsonify, request
from pymongo.server_api import ServerApi
from flask_cors import CORS


def connect_to_mongo():
    MONGO_URL = os.environ.get("MONGO_URL")
    MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
    MONGO_USERNAME = os.environ.get("MONGO_USERNAME")

    # Connect to MongoDB
    client = pymongo.MongoClient(
        f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_URL}/test?retryWrites=true&w=majority",
        server_api=ServerApi('1'), socketTimeoutMS=5000, connectTimeoutMS=5000
    )

    try:
        client.db_name.command('ping')
    except Exception as e:
        print("MongoDB is down\n", e)
        return None
    return client['sensor_analysis']


def main():
    app = Flask(__name__)
    CORS(app)

    db = connect_to_mongo()

    @app.route('/range')
    def get_range():
        interval = request.args.get('interval')
        if int(interval) not in [30, 60]:
            return jsonify({"error": f"Invalid interval. Only 30 and 60 are allowed, got {interval}"}), 400
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "max_end_date": {"$max": "$end"},
                    "min_start_date": {"$min": "$start"}
                }
            }
        ]
        return jsonify(list(db[f'interval_{interval}'].aggregate(pipeline))[0])


    app.run()


if __name__ == "__main__":
    main()
