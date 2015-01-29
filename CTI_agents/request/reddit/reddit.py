import urllib2
import json
import time
import datetime
import yaml
from pymongo import MongoClient as MC


def setup():
    setup_file = open("./request/reddit/setup.yaml", "r")
    setup_docs = yaml.load_all(setup_file)

    for doc in setup_docs:
        base_url = doc['base_url']
        limit = doc['default_limit']
        subreddits_list = doc['subreddits']

    urls = []

    for sub in subreddits_list:
        u = base_url % (sub, limit)
        urls.append(u)

    return urls


def mongo_connect():

    client = MC()
    db = client.DeloitteDemo
    collection = db.reddit

    return client, collection


def mongo_insert(collection, entries):

    for entry in entries:
        collection.insert(entry)


def mongo_disconnect(client):

    client.close()


def download(url):
    worked = True
    response = ""
    try:
        connection = urllib2.urlopen(url)
        response = connection.read()
        connection.close()
    except:
        worked = False

    return worked, response


def parse_json(response):

    jinput = json.loads(response)
    entries = []

    for i in jinput["data"]["children"]:
        url = i["data"]["url"]
        title = i["data"]["title"]
        score = i["data"]["score"]
        num_comments = i["data"]["num_comments"]
        ups = i["data"]["ups"]

        entry = {"u": url, "t": title, "sc": score, "nc": num_comments, "up": ups}
        entries.append(entry)

    return entries


def run():

    urls = setup()
    client, collection = mongo_connect()

    responses = []

    for url in urls:
        worked, response = download(url)
        if worked:
            responses.append(response)
            for response in responses:
                entries = parse_json(response)
                mongo_insert(collection, entries)
        else:
            print "Could not retrieve resourse"

    mongo_disconnect(client)
    print "Reddit scraping has finished"

def iterate(interval):
    while True:
        run()
        print "Iteration: " + str(datetime.datetime.now())
        time.sleep(interval)
