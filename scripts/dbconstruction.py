######################################################
#
# dbconstruction - upload processed data to noSQL MongoDB
# written by Anshuman Sahoo (anshuman264@gmail.com)
#
######################################################

import json
import pymongo
import pprint


def dbconstruction():
    client = pymongo.MongoClient(
        "mongodb://anshuman264:VJkCopXqbK5smqf0@cluster0-shard-00-00-ouybv.mongodb.net:27017,"
        "cluster0-shard-00-01-ouybv.mongodb.net:27017,"
        "cluster0-shard-00-02-ouybv.mongodb.net:27017/co_table?ssl=true&replicaSet=Cluster0-shard-0&authSource"
        "=admin")
    db = client['co_table']

    collection = db['co_collection']

    source_file = open("../output/co_occurrence.json", 'r')

    # pprint.pprint(collection.find_one())

    parsed = json.loads(source_file.read())

    print(parsed)

    collection.insert(parsed)


if __name__ == '__main__':
    dbconstruction()
