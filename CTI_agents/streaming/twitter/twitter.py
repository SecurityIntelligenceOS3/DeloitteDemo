from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient as MC
import yaml
import json

#very bad code at the moment


def setup():

    auth_list = []
    setup_file = open("./streaming/twitter/setup.yaml", "r")
    setup_docs = yaml.load_all(setup_file)
    for doc in setup_docs:
        auth_list.append(doc['authentication']['access_token'])
        auth_list.append(doc['authentication']['access_token_secret'])
        auth_list.append(doc['authentication']['consumer_key'])
        auth_list.append(doc['authentication']['consumer_secret'])
        track_list = doc['tracks']

    return auth_list, track_list


class StdOutListener(StreamListener):

    def mongo_connect(self):
        client = MC()
        db = client.DeloitteDemo
        collection = db.twitter

        return collection

    def parse_json(self, response):

        j = json.loads(response)
        entry = {}

        created_at = j['created_at']
        text = j['text']
        id_str = j['id_str']
        u_id_str = j['user']['id_str']
        u_name = j['user']['name']
        u_screen_name = j['user']['screen_name']
        u_url = j['user']['url']
        u_description = j['user']['description']
        u_followers_count = j['user']['followers_count']
        u_friends_count = j['user']['friends_count']
        u_statuses_count = j['user']['statuses_count']
        u_time_zone = j['user']['time_zone']
        u_lang = j['user']['lang']
        geo = j['geo']
        coordinates = j['coordinates']
        place = j['place']
        contributors = j['contributors']
        e_hashtags = j['entities']['hashtags']
        e_trends = j['entities']['trends']
        e_urls = j['entities']['urls']
        lang = j['lang']

        try:
            entry = {"ca": created_at, "t": text, "id": id_str, "uid": u_id_str, "un": u_name,
                     "usn": u_screen_name, "uu": u_url, "ud": u_description, "ufc": u_followers_count,
                     "ufr": u_friends_count, "usc": u_statuses_count, "utz": u_time_zone,
                     "ul": u_lang, "g": geo, "co": coordinates, "p": place, "cb": contributors,
                     "eht": e_hashtags, "l": lang, "etr": e_trends, "eu": e_urls}
        except:
            pass

        return entry

    def on_data(self, data):
        entry = self.parse_json(data)
        collection = self.mongo_connect()
        try:
            collection.insert(entry)
        except:
            pass

        return True

    def on_error(self, status):
        print status


def fire():
    auth_list, track_list = setup()

    l = StdOutListener()
    auth = OAuthHandler(auth_list[2], auth_list[3])
    auth.set_access_token(auth_list[0], auth_list[1])
    stream = Stream(auth, l)

    stream.filter(track=track_list)


