import json
import urllib2
import time
import datetime
import yaml
from pymongo import MongoClient as MC


def setup():
    setup_file = open("./request/phishtank/setup.yaml", "r")
    setup_docs = yaml.load_all(setup_file)

    for doc in setup_docs:
        key = doc['key']
        db_url = doc['url'] % key

    return db_url


def download(url):
    try:
        response = urllib2.urlopen(url)
    except:
        response = "Could not retrieve resourse"

    return response


def mongo_connect():

    client = MC()
    db = client.DeloitteDemo
    collection = db.phishtank

    return client, collection


def mongo_remove(collection):

    collection.remove({})


def mongo_insert(collection, entries):

    for entry in entries:
        collection.insert(entry)


def mongo_disconnect(client):

    client.close()


def parse_json(response):

    jinput = json.loads(response.read())
    entries = []
    # for each entry in file:
    for j in jinput:
        # parse specific values
        try:
            url = j['url'] #url
            phish_id = j['phish_id'] #phish_id
            ip_address = j['details'][0]['ip_address']  # ip_address
            cidr_block = j['details'][0]['cidr_block']  # cidr_block
            announcing_network = j['details'][0]['announcing_network']  # announcing_network
            submission_time = j['submission_time']  # submission_time
            verification_time = j['verification_time']  # verification_time
            target = j['target']  # target

        except:
            pass

        entry = {"u": url, "id": phish_id, "ip": ip_address, "cb": cidr_block, "an": announcing_network, "st": submission_time, "vt": verification_time, "t": target}
        entries.append(entry)

    return entries


def run():

    db_url = setup()
    response = download(db_url)
    if type(response) != str:
        client, collection = mongo_connect()
        mongo_remove(collection)  # delete all data
        to_mongo = parse_json(response)
        mongo_insert(collection, to_mongo)
        mongo_disconnect(client)
        print "Phishtank scraping has finished"
    else:
        print response




def iterate(interval):
    while True:
        run()
        print "Iteration: " + str(datetime.datetime.now())
        time.sleep(interval)
