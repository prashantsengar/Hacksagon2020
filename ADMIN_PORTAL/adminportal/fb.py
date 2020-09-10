import pyrebase
import configparser as cp

conf = cp.ConfigParser()
conf.read("conf.ini")

config = {
    "apiKey": conf["DEFAULT"]["apikey"],
    "authDomain": conf["DEFAULT"]["domain"],
    "databaseURL": conf["DEFAULT"]["dburl"],
    "projectId": conf["DEFAULT"]["projectid"],
    "storageBucket": conf["DEFAULT"]["storage"],
    "messagingSenderId": conf["DEFAULT"]["senderid"],
    "appId": conf["DEFAULT"]["appid"],
    "measurementId": conf["DEFAULT"]["measureid"],
}


firebase = pyrebase.initialize_app(config)

db = firebase.database()

# all_crime = db.child('crime').get()
# for crime in all_crime.each():
#     print(crime.val())

def insert(name):
    data = {"name": name}
    return db.child("users").push(data)

def main():
    return db
