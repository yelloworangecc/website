import hashlib,os

from flask import Blueprint,abort,request,current_app

module_wx = Blueprint('module_wx', __name__, url_prefix='/wx')
current_app.config['WX_TOKEN'] = os.getenv('WX_TOKEN')
current_app.config['WX_ID'] = os.getenv('WX_ID')
current_app.config['WX_PWD'] = os.getenv('WX_PWD')

@module_wx.route('/token')
def token():
    if not request.args:
        abort(400)
    list = [current_app.config['WX_TOKEN'], request.args['timestamp'], request.args['nonce']]
    list.sort()
    str =  list[0]+list[1]+list[2]
    sha1 = hashlib.sha1()
    sha1.update(str.encode('utf-8'))
    hashcode = sha1.hexdigest()
    if hashcode == request.args['signature']:
        return request.args['echostr']
    else:
        return abort(403)

