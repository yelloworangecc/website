import os,time

from flask import Flask
from flask import render_template
from flask import send_file
from flask import url_for
from flask import request
from flask import logging
from flask import session
from flask import redirect
from flask import send_from_directory

from werkzeug.utils import secure_filename

import flask_login
from flask_login import LoginManager
from flask_login import logout_user
from flask_login import login_user
from flask_login import current_user

from py.EmailMe import EmailMe
from py.LoginUser import User
# from py.MemberController import *

# initialize app
app = Flask(__name__)
app.app_context().push()
app.secret_key = os.getenv('SECRET_KEY') # must
app.config['LIVE_FOLD'] = 'live/'
app.config['IP'] = 'None'
app.config['TS_NUMBER'] = 1000

# regist blueprint
from wx import module_wx
app.register_blueprint(module_wx)
from blog import module_blog
app.register_blueprint(module_blog)
from video import module_video
app.register_blueprint(module_video)

login_manager = LoginManager()
login_manager.init_app(app)

emailMe = EmailMe('smtp.qq.com',465)

@app.teardown_request
def teardown_request(exception=None):
    pass

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return app.config['IP']

# login_user
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        print(phone + " " + password)
        user = User.get(phone)
        if user.verify_password(password):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('signin.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('signin'))#'Unauthorized', 401

# signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
    return render_template('signup.html')


# member management
# @app.route('/member', methods=['GET', 'POST'])
# def member():
#     member_controller=MemberController(request)
#     try:
#         html = member_controller.handle_request()
#     except InvalidMethod as e:
#         return str(e.args)
#     else:
#         return html


# This callback is used to reload the user object from the user ID stored in the session.
@login_manager.user_loader
def load_user(phone):
    print(phone)
    return User.get(phone)

@app.route('/album/')
@app.route('/album/<name>')
def album(name=None):
    if name is None:
        return render_template('album.html')
    else:
        return send_file('album/'+name)

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/messageme',methods=['GET','POST'])
def messageme():
    ''' {'who': 'tester', 'msg': 'hello' } '''
    if request.method == 'POST':
        data = request.form
        who = data['who']
        msg = data['msg']
        code = os.getenv('QQMAILCODE')
        if who is None or msg is None or code is None:
            return 'Send message FAIL'
        else:
            append_file_cmd = 'echo ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ', ' + who +', ' + msg + ' >> msg.txt'
            os.system(append_file_cmd)
            emailMe.login('1040617473@qq.com',code)
            emailMe.send('yelloworangecc@qq.com',who,msg)
            emailMe.quit()
            return 'Send message OK'
        
    if request.method == 'GET':
        return render_template('msgform.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)
