from django.shortcuts import render
#import pyrebase

# Create your views here.

# NOTE THIS IS FOR OLD FIREBASE CREDENTIALS WHICH ARE NO LONGER IN USE

# firebaseConfig = {
#   'apiKey': "AIzaSyCVyDzI_-Pb_y4zvOerNhN-ucHbt7IvLRc",
#   'authDomain': "makeup-matchr.firebaseapp.com",
#   'databaseURL': "https://makeup-matchr-default-rtdb.firebaseio.com",
#   'projectId': "makeup-matchr",
#   'storageBucket': "makeup-matchr.appspot.com",
#   'messagingSenderId': "1006679463606",
#   'appId': "1:1006679463606:web:245af1e8d9377edbb2f817"
# }

# firebase=pyrebase.initialize_app(firebaseConfig)
# authe = firebase.auth()
# database=firebase.database()

def index(request):
        # #accessing our firebase data and storing it in a variable
        # name = database.child('Data').child('Name').get().val()
        # stack = database.child('Data').child('Stack').get().val()
        # framework = database.child('Data').child('Framework').get().val()
    
        # context = {
        #     'name':name,
        #     'stack':stack,
        #     'framework':framework
        # }
        # return render(request, 'index.html', context)
        pass


