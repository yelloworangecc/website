from flask import Flask
from flask import render_template
from flask import send_file
from flask import url_for
from flask import request
from flask import logging
from py.EmailMe import EmailMe
import os,time

app = Flask(__name__)
emailMe = EmailMe('smtp.qq.com',465)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

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
