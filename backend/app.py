from flask import Flask, Response
import sqlite3
import json
import time


app = Flask(__name__)

DB_LOCATION = "cities_index.sqlite"


@app.route("/cities/<year>")
def cities_by_year(year):
    start_time = time.time()
    db = sqlite3.connect(DB_LOCATION)
    db.row_factory = sqlite3.Row
    cursor = db.execute("SELECT * FROM cities WHERE year = ?", (year,))
    cities = cursor.fetchall()
    cursor.close()
    db.close()
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row["longitude"], row["latitude"]],
                },
                "properties": dict(row),
            }
            for row in cities
        ],
    }
    r = Response(
        json.dumps(geojson, ensure_ascii=False),
        mimetype="text/json",
        headers={"Access-Control-Allow-Origin": "*"}
    )
    print("--- %s seconds ---" % (time.time() - start_time))
    return r


@app.route("/city/<id>")
def city_by_id(id):
    start_time = time.time()
    db = sqlite3.connect(DB_LOCATION)
    db.row_factory = sqlite3.Row
    cursor = db.execute("SELECT * FROM cities WHERE id = ?", (id,))
    city = cursor.fetchone()
    cursor.close()
    db.close()
    r = Response(
        json.dumps(dict(city), ensure_ascii=False),
        mimetype="text/json",
        headers={"Access-Control-Allow-Origin": "*"}
    )
    print("--- %s seconds ---" % (time.time() - start_time))
    return r
