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
        options = "retryWrites=true&w=majority"
        connection_string = f"mongodb+srv://{user}:{password}@cluster0.djv4q.mongodb.net/{database}?{options}"
        connect(host=connection_string)

    @classmethod
    def connect_test_database(cls):
        connect("mongoenginetest", host="mongomock://localhost")

    @classmethod
    def disconnect_database(cls):
        disconnect()

    @classmethod
    def reconnect_prod_database(cls):
        cls.disconnect_database()
        cls.connect_prod_database()
