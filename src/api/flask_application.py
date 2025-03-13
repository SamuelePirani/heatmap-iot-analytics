from bson.json_util import dumps
from flask import Flask, jsonify, Response, request
from flask_cors import CORS

from src.database.db_config import connect_to_db

app = Flask(__name__)
CORS(app)

client = connect_to_db()
db = client["iot_analytics"]


@app.route("/api/data", methods=["GET"])
def get_data():
    query = {}

    room = request.args.get("room")
    if room:
        query["room"] = room

    start = request.args.get("start")
    if start:
        query["start"] = {"$gte": start}

    end = request.args.get("end")
    if end:
        query["end"] = {"$lte": end}

    # start = request.args.get("start")
    # if start:
    #     try:
    #         # Remove the trailing "Z" if present (indicating UTC)
    #         if start.endswith("Z"):
    #             start = start[:-1]
    #         start_date = datetime.fromisoformat(start)
    #         query["start"] = {"$gte": start_date}
    #     except ValueError:
    #         return jsonify({"error": "Invalid start date format. Expected ISO format."}), 400
    #
    # end = request.args.get("end")
    # if end:
    #     try:
    #         if end.endswith("Z"):
    #             end = end[:-1]
    #         end_date = datetime.fromisoformat(end)
    #         query["end"] = {"$lte": end_date}
    #     except ValueError:
    #         return jsonify({"error": "Invalid end date format. Expected ISO format."}), 400

    sensor = request.args.get("sensor")
    if sensor:
        query["sensor"] = sensor

    data = list(db["data"].find(query))

    if not data:
        app.logger.warning("No data found for the given query: %s", query)
        return jsonify([]), 200

    return Response(dumps(data), status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
