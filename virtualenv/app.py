from flask import Flask,render_template,send_from_directory,url_for,session,request,redirect

from flask_uploads import UploadSet,IMAGES,configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import SubmitField

import pyrebase
from forms import SignupForm, LoginForm

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
auth = firebase.auth()



app = Flask(__name__)
app.config['SECRET_KEY']='asldfkjlj'
app.config['UPLOADED_PHOTOS_DEST']='uploads'
app.config['RECAPTCHA_PUBLIC_KEY']= '6LdqBZAjAAAAAK91_r-2vo1Q4xHwljDgGhu44QiX'
app.config['RECAPTCHA_PRIVATE_KEY']='6LdqBZAjAAAAAH01brCl8Ciuddmt5t2avzhyzF--'

photos = UploadSet('photos',IMAGES)
configure_uploads(app,photos)

class UploadForm(FlaskForm):
    photo =FileField(
        validators =[
            FileAllowed(photos,'Only Images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('upload')



@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],filename)

@app.route('/')
def welcome():
    return render_template('main.html')

@app.route('/signup/',methods=['GET','POST'])
def signup():
    form = SignupForm()
    if request.method=='POST':
        form.validate_on_submit()
        name = request.form.get('first_name')#+request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.create_user_with_email_and_password(email,password)
            session['user']=user
            session['name']=name
            return redirect(url_for('upload_image'))
        except:
            return "invalid signup, please try again"
        
        
    elif request.method=="GET":
        return render_template('signup-flask.html',form = form)


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method =='POST':
        form.validate_on_submit()
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            # global person
            # person['user']=user
            # person['name']=email
            # name = person.get('name')
            # print
            redirect(url_for('upload_image',user =''))#, user = name.get('name'))
        except:
            return "invalid user or password try again"
    if request.method=='GET':
        if 'user' in session:
            return redirect(url_for('upload_image'))
            # return "Hi {}".format(session['user'])
        else:
            return render_template('login-flask.html')


@app.route('/logout')
def logout ():
    session.pop('user',None)
    session.pop('name',None)
    return redirect(url_for('login'))

@app.route('/home',methods=['GET','POST'])
def upload_image():
    if 'user' in session:
        user = session['user']
    else:
        user =''
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file',filename = filename)
    else:file_url = None
    return render_template('landing.html',form = form,file_url= file_url, user =user)

@app.route('/workbench')
def xray():
    return render_template('display.html')
