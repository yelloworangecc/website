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
from py.MemberManager import Member
from py.ArticleManager import Article

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') # must
app.config['LIVE_FOLD'] = 'live/'
app.config['IP'] = 'None'
app.config['TS_NUMBER'] = 1000
app.config['BLOG_PER_PAGE'] = 5

login_manager = LoginManager()
login_manager.init_app(app)

emailMe = EmailMe('smtp.qq.com',465)

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
@app.route('/member', methods=['GET', 'POST'])
def member():
    # load all members first
    if not Member.load():
        return '<h1>query member failed, members not loaded</h1>'

    if request.method == 'GET':
        # get member by phone
        member = None
        print(request.args)
        if len(request.args) > 0:
            member = Member.get(request.args['phone'])
            
        Member.genTop10()
        members_p=Member.getTop10Points()
        members_t=Member.getTop10Times()
        return render_template('member.html',member=member,members_p=members_p,members_t=members_t)

    else:
        member = Member.get(request.args['phone'])
        member.modifyPoints(float(request.form['point']))
        members_p=Member.getTop10Points()
        members_t=Member.getTop10Times()
        return render_template('member.html',member=member,members_p=members_p,members_t=members_t)

# blog list
@app.route('/blog')
def blog():
    # load all articles first
    if not Article.load():
        return '<h1>load articles failed</h1>'

    articles = Article.getPageList(0, app.config['BLOG_PER_PAGE'])
    print(len(articles))
    return render_template('blog.html',articles=articles)

# single article
@app.route('/blog/<filename>')
def post(filename):    
    return render_template(f'posts/{filename}')


@app.route('/upload/post/<filename>', methods=['PUT'])
def upload_post(filename):
    print(request.data)
    return "None"

# play video
@app.route('/live')
@flask_login.login_required
def live():
    return render_template('live.html')

# access playlist and segment files
@app.route('/live/<filename>', methods=['GET','PUT'])
def uploaded_file(filename):
    if request.method == 'PUT':
        # Record IP
        app.config['IP'] = request.remote_addr
        # Delete file
        dot_index = filename.find('.')
        postfix = filename[dot_index+1:]
        if postfix == 'ts':
            number = int(filename[8:dot_index])
            if number >= app.config['TS_NUMBER']:
                deletefile = 'playlist'+str(number - app.config['TS_NUMBER'])+'.ts'
                deletepath = os.path.join(app.config['LIVE_FOLD'],deletefile)
                os.remove(deletepath)
				
        filepath = os.path.join(app.config['LIVE_FOLD'],filename)
        with open(filepath,mode='wb') as file:
            file.write(request.data)
        return 'success'
    else:
        return send_from_directory(app.config['LIVE_FOLD'],filename)


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

@app.route('/controller/')
@app.route('/controller/<command>')
def controller(command=None):
    if command is None:
        return render_template('controller.html')
    else:
        app.logger.info(command)
        return render_template('controller.html')

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
    app.run(debug=True,host='0.0.0.0',port=8080)
