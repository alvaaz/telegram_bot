from dotenv import load_dotenv
import os
import pymongo

load_dotenv()

token: str = os.getenv("TELEGRAM_TOKEN")
mode: str = os.getenv("MODE")
client = pymongo.MongoClient("mongodb+srv://user:pwd@cluster0.te8ga.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db_name: str = "bot"
collection_name: str = "quotes"
cloud_name:str = "x"
api_key: str = "x",
api_secret = "x"
db = client[db_name][collection_name]
