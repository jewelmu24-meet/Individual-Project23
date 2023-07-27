from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  'apiKey': "AIzaSyBY5paVATi0w5JAZVo8B7Y_jUGu0zuKpeg",
  'authDomain': "cs-individual-project-408ed.firebaseapp.com",
  'projectId': "cs-individual-project-408ed",
  'storageBucket': "cs-individual-project-408ed.appspot.com",
  'messagingSenderId': "730281284401",
  'appId': "1:730281284401:web:aad1b0d23cd1a06bfe5610",
  'measurementId': "G-B4RD60WQWD" , 'databaseURL': "https://cs-individual-project-408ed-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase= pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database() 

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method=='GET':
        return render_template("signin.html")

    else:
        email = request.form['email']
        password = request.form['password']

        try:
            login_session['user']= auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('content'))

        except:
            error ="authentication failed"
            return render_template('signup.html', e=email, p=password)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')

    else:
        email = request.form['email']
        password = request.form['password']
        fullname=request.form['fullname']
        username =request.form['username']
        bio = request.form['bio']

        user={'fullname': fullname, 'username': username, 'bio': bio, 'email':email}
        
        try:
            login_session['user']= auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            db.child('Users').child(UID).set(user)
            return redirect(url_for('content'))

        except:
            error ="authentication failed"
            return render_template('signup.html', e=email, p=password)


@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method =='POST':
        recipe = request.form['recipe']
        text = request.form['text']
        UID = login_session['user']['localId']
        review = {'recipe': recipe, 'text': text, 'uid': UID}
        db.child("reviews").child(recipe).push(review)
        return redirect(url_for('content'))

    else:
        return render_template("review.html")

      

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/content', methods=['GET', 'POST'])
def content():
#if request.method=='POST':

    reviews = db.child('reviews').get().val()
    reviews_macarons = reviews['macarons']
    reviews_cremebrulee = reviews['cremebrulee']
    reviews_eclairs = reviews['eclairs']

    return render_template('content.html', m=reviews_macarons, c=reviews_cremebrulee, e=reviews_eclairs)


#Code goes above here


#@app.route('/')
#def home():
    #return render_template('home.html')

#app.route('/signup', methods=['GET','POST'])
#def signup():
    #if request.method=='GET'
    #return render_template('signup.html')

    #else:


#@app.route('signin', methods=['GET', 'POST']) 
#def signin():
    #if request.method=='GET'
    #return render_template('signin.html')   

   # else:


#def hello_name_route(name):
    #return render_template(
        #'hello.html', n = name)


if __name__ == '__main__':
    app.run(debug=True)