import os
from urllib import parse
from dotenv import load_dotenv
from mongoengine import connect, disconnect


class Connector:
    @classmethod
    def load_database_creds(cls):
        load_dotenv()

    @classmethod
    def connect_prod_database(cls):
        user = parse.quote_plus(os.environ["DATABASE_USER"])
        password = parse.quote_plus(os.environ["DATABASE_PASSWORD"])
        database = "idb"
        connect(host=f"mongodb+srv://{user}:{password}@cluster0.djv4q.mongodb.net/{database}?retryWrites=true&w=majority")

    @classmethod
    def connect_test_database(cls):
        connect("mongoenginetest", host="mongomock://localhost")

    @classmethod
    def disconnect_database(cls):
        disconnect()
