from django.shortcuts import render
import firebase_admin
from firebase_admin import db

# Grab crednetials from the provided private key
cred_obj = firebase_admin.credentials.Certificate('./makeupApp/credentials.json')

# Connect
firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://makeup-matchr-default-rtdb.firebaseio.com'
	})

def index(request):
        #accessing our firebase data and storing it in a variable
        ref = db.reference('Products')

        test = ref.child('Template').get()
    
        context = {
            'URL':test['URL']
        }
        return render(request, 'index.html', context)


