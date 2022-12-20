import pyrebase

config = {
  'apiKey': "AIzaSyDc91r_zBHXBIRt19AdWonw4ScQ3sr9yDw",
  'authDomain': "cxr-authenticator.firebaseapp.com",
  'projectId': "cxr-authenticator",
  'storageBucket': "cxr-authenticator.appspot.com",
  'messagingSenderId': "889363758241",
  'appId': "1:889363758241:web:6dc3ddc2311e6de0fe04e0",
  'measurementId': "G-PYSQ88MF0D",
  'databaseURL':""
}

firebase = pyrebase.initialize_app(config)
auth  = firebase.auth()
email = "test@gmail.com"
password =123456

# user = auth.create_user_with_email_and_password(email,password)
# print(user)

user= auth.sign_in_with_email_and_password(email,password)

#get user account info
# info = auth.get_account_info(user['idToken'])
# print(info)

auth.send_email_verification(user['idToken'])

auth.send_password_reset_email(email)