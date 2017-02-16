from flask import Flask
from flask import render_template
from pymongo import MongoClient
import pandas as pd

app = Flask(__name__)

MONGODB_HOST = "mongodb://anshuman264:VJkCopXqbK5smqf0@cluster0-shard-00-00-ouybv.mongodb.net:27017,"
"cluster0-shard-00-01-ouybv.mongodb.net:27017,"
"cluster0-shard-00-02-ouybv.mongodb.net:27017/co_table?ssl=true&replicaSet=Cluster0-shard-0&authSource"
"=admin"
MONGODB_PORT = 27017
DBS_NAME = 'co_table'
COLLECTION_NAME = 'co_collection'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/co_table/analysis")
def co_table():
    connection = MongoClient(
        "mongodb://anshuman264:VJkCopXqbK5smqf0@cluster0-shard-00-00-ouybv.mongodb.net:27017,"
        "cluster0-shard-00-01-ouybv.mongodb.net:27017,"
        "cluster0-shard-00-02-ouybv.mongodb.net:27017/co_table?ssl=true&replicaSet=Cluster0-shard-0&authSource"
        "=admin")

    collection = connection[DBS_NAME][COLLECTION_NAME]
    co_occurrences = collection.find_one()
    # co_occurrences = json.dumps(co_occurrences, default=json_util.default)
    co_list = []
    for k, v in co_occurrences.items():
        co_list.append((k, v))
    print(co_list)
    # co_list = sorted(co_list, key=lambda x: x[1], reverse=True)
    labels = ['Word', 'Co-Occurrence']

    df = pd.DataFrame.from_records(co_list, columns=labels)
    connection.close()

    return render_template("analysis.html", tables=[df.to_html()], titles=['na', 'of Research Articles'])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)