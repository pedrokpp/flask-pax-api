from pymongo import MongoClient
from dotenv import load_dotenv
from os import environ
import random, json, string

load_dotenv('.env')

DBS_URL = environ['DATABASE-URL']

client = MongoClient(DBS_URL)
db = client.PAX
collection = db["pax"]

def addLicense(username: str, license: str) -> str:
    randomID: str = ''.join(random.choice(string.ascii_letters) for _ in range(30))
    newLicense: dict = {
        "_id" : randomID,
        "username" : username,
        "license" : license
    }
    try:
        collection.insert_one(newLicense)
        return json.dumps(newLicense)
    except:
        return json.dumps({ "error": True })

def checkLicense(license: str) -> dict:
    x = collection.find_one({ "license": license })
    return { "error": True } if x == None else x

def revokeLicense(license: str) -> None:
    collection.delete_many({ "license": license })