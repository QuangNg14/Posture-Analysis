import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCDxKa-AEKeqm-nFyFDh3u9j00rS_tNzqE",
    "authDomain": "posture-analytics.firebaseapp.com",
    "projectId": "posture-analytics",
    "storageBucket": "posture-analytics.appspot.com",
    "messagingSenderId": "993803643647",
    "appId": "1:993803643647:web:9c6beaa9367a66f6c83aca",
    "databaseURL": "",
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

path_on_cloud = "videos/pose1_demo"
path_local = "./videos/pose1_demo.mp4"
storage.child(path_on_cloud).put(path_local)

# link = storage.child("images/test-shot").get_url(None)
# print(link)
# https://firebasestorage.googleapis.com/v0/b/storage-url.appspot.com/o/images%2Fexample.jpg?alt=media
