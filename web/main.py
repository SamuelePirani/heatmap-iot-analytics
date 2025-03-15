import os
from datetime import datetime

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

def fix_date_format(date_string):
    return date_string.replace(" ", "+")

def main():
    app = Flask(__name__)
    CORS(app)

    db = connect_to_mongo()

    @app.route('/range')
    def get_range():
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "max_end_date": {"$max": "$end"},
                    "min_start_date": {"$min": "$start"}
                }
            }
        ]
        return jsonify(list(db[f'interval_30'].aggregate(pipeline))[0])

    @app.route('/data_room', methods=['GET'])
    def get_sensors():

        room_name = request.args.get('room_name')
        interval = request.args.get('interval')
        start = request.args.get('start')
        end = request.args.get('end')

        start = fix_date_format(start)
        end = fix_date_format(end)

        query = {"start": {"$gte": datetime.fromisoformat(start)}, "end": {"$lte": datetime.fromisoformat(end)}, "room_name": room_name}

        if room_name:
            query["room_name"] = room_name

        print(query)

        sensors = list(db[f"interval_{interval}"].find(query, {"_id": 0}))
        return jsonify(sensors)

    app.run()


if __name__ == "__main__":
    main()
