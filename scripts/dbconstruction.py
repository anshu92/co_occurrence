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
    """
    Connect to remote MongoDB server and insert processed data as a document of key value pairs
    (JSON).

    Returns
    -------
    None
    """
    client = pymongo.MongoClient(
        "mongodb://anshuman264:VJkCopXqbK5smqf0@cluster0-shard-00-00-ouybv.mongodb.net:27017,"
        "cluster0-shard-00-01-ouybv.mongodb.net:27017,"
        "cluster0-shard-00-02-ouybv.mongodb.net:27017/co_table?ssl=true&replicaSet=Cluster0-shard-0&authSource"
        "=admin")
    db = client['co_table_per_article']

    collection = db['co_collection']

    source_file = open("../output/co_occurrence_per_article.json", 'r')

    # pprint.pprint(collection.find_one())

    parsed = json.loads(source_file.read())

    print(parsed)

    collection.insert(parsed)


if __name__ == '__main__':
    dbconstruction()
