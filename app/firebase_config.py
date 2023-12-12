import firebase_admin
from firebase_admin import credentials, db


# Replace 'path/to/serviceAccountKey.json' with the path to your Firebase service account key
cred = credentials.Certificate("/home/devyashshah/Desktop/SE_FInal/auvisionx-firebase-adminsdk-dr852-1a950ab3b5.json")
firebase_app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://auvisionx-default-rtdb.firebaseio.com'})
