from flask import Flask, redirect, url_for, render_template, request, session
from forms import LoginForm,QAForm
from tabledef import *
import helpers
import json
import os
from werkzeug.utils import secure_filename
from collections import Counter
from numpy.random import choice

UPLOAD_FOLDER = '/home/manoj/Desktop/Flaskex-master/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

engine = db_connect()
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    global file_in_use
    if not session.get('logged_in'):
        form = LoginForm(request.form)
        if request.method == 'POST':
          username = request.form['username'].lower()
          password = request.form['password']
          if form.validate():
            if helpers.credentials_valid(username, password):
              session['logged_in'] = True
              session['username'] = username
              return json.dumps({'status': 'Login successful'})
            return json.dumps({'status': 'Invalid user/pass'})
          return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    
    
    file_in_use = request.args.get('fname')
    if file_in_use is None:
        file_in_use = 'coco.png'        
        filens = helpers.get_fnames()
        allfiles = [row.filename for row in filens]
        count = Counter(allfiles)
        uniqef = list(count.keys())
        p = list(count.values())
        MAX_ANNOT = 6 # max no of annottaion for an image
        p = [ max( MAX_ANNOT - ii , 0)  for ii in p]
        if sum(p) !=0 :
            p = [ i/sum(p) for i in p]
            idx = choice(range(0,len(p)),p=p)
        else:
            idx = choice(range(0,len(p)))
        
        file_in_use = uniqef[idx]
        
        
    print("....",file_in_use)
    imgs_dict = []
    imgq = {}
    #show file in random but haing many questions
    #filename = 'coco.png'
    filename = file_in_use    
    qas = helpers.get_qa(filename)
    #print (qas)
    imgq['img'] = filename
    imgq['que'] = qas
    imgq['ans'] = "1"
    imgq['qid'] = "1"
    imgs_dict.append(imgq)
    return render_template('home.html', pair = imgq)


@app.route('/addqa', methods=['POST'])
def addqa():
    form = QAForm(request.form)
    if request.method == 'POST':
        question = request.form['question'].lower()
        answer = request.form['answer'].lower()
        filename = request.form['filename']
        if form.validate():
            #if upload new file get newfilename
            helpers.add_qa(filename,question, answer)
            return json.dumps({'status': 'QA successful'})
        return json.dumps({'status': 'Both fields required'})



@app.route('/upload', methods=['POST'])
def upload():
    global file_in_use
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = 'uploads/' + filename
            file_in_use = filename
            return redirect(url_for('login',fname=filename))




@app.route('/next', methods=['POST'])
def nextfile():
    return redirect(url_for('login'))



@app.route("/logout")
def logout():
  session['logged_in'] = False
  return redirect(url_for('login'))

# -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if not session.get('logged_in'):
    form = LoginForm(request.form)
    if request.method == 'POST':
      username = request.form['username'].lower()
      password = helpers.hash_password(request.form['password'])
      email = request.form['email']
      if form.validate():
        if not helpers.username_taken(username):
          helpers.add_user(username, password, email)
          session['logged_in'] = True
          session['username'] = username
          return json.dumps({'status': 'Signup successful'})
        return json.dumps({'status': 'Username taken'})
      return json.dumps({'status': 'User/Pass required'})
    return render_template('login.html', form=form)
  return redirect(url_for('login'))

# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
  if session.get('logged_in'):
    if request.method == 'POST':
      password = request.form['password']
      if password != "":
        password = helpers.hash_password(password)
      email = request.form['email']
      helpers.change_user(password=password, email=email)
      return json.dumps({'status': 'Saved'})
    user = helpers.get_user()
    return render_template('settings.html', user=user)
  return redirect(url_for('login'))

# ======== Main ============================================================== #
if __name__ == "__main__":
  app.secret_key = os.urandom(12) # Generic key for dev purposes only
  app.run(host='0.0.0.0', port=5000,debug=True, use_reloader=True,threaded=True)
