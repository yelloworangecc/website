import hashlib,os,requests,time
from xml.etree import ElementTree
from py.WXManager import WXManager

from flask import Blueprint,abort,request,current_app

module_wx = Blueprint('module_wx', __name__, url_prefix='/wx')
current_app.config['WX_TOKEN'] = os.getenv('WX_TOKEN')
current_app.config['WX_ID'] = os.getenv('WX_ID')
current_app.config['WX_PWD'] = os.getenv('WX_PWD')
current_app.config['WX_ACCESS_TIME'] = 0
current_app.config['WX_ACCESS_EXPIRE'] = 7000
current_app.config['WX_USER_TOTAL'] = 0
current_app.config['WX_USER_COUNT'] = 0

@module_wx.route('MP_verify_4P6XPqWt5Gxg697V.txt')
def wx_verify():
    return '4P6XPqWt5Gxg697V'

@module_wx.route('/token', methods=['GET','POST'])
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
        if request.method == 'GET':
            return request.args['echostr']
        else:
            root=ElementTree.fromstring(request.data.decode())
            data={}
            for child in root:
                data[child.tag]=child.text
            print(data)
            wx_manager = WXManager.get(data['FromUserName'])
            return wx_manager.handle(data)
    else:
        return abort(403)

@module_wx.route('/access_token')
def access_token():
    access_time = current_app.config['WX_ACCESS_TIME']
    t = int(time.time())
    print(access_time,t)
    if access_time != 0 and t - access_time < current_app.config['WX_ACCESS_EXPIRE']:
        print(current_app.config['WX_ACCESS_TOKEN'])
        return 'OK'
    
    APPID = current_app.config['WX_ID']
    APPSECRET = current_app.config['WX_PWD']
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'
    print(url)
    r = requests.get(url)
    j = r.json()
    if 'access_token' in j:
        current_app.config['WX_ACCESS_TOKEN'] = j['access_token']
        current_app.config['WX_ACCESS_TIME'] = t
        print(current_app.config['WX_ACCESS_TOKEN'])
        return 'OK'
    else:
        about(500)
    
#https://api.weixin.qq.com/cgi-bin/user/get?access_token=ACCESS_TOKEN&next_openid=NEXT_OPENID
@module_wx.route('/user_list')
def user_list():
    access_token()
    
    ACCESS_TOKEN=current_app.config['WX_ACCESS_TOKEN']
    url = f'https://api.weixin.qq.com/cgi-bin/user/get?access_token={ACCESS_TOKEN}'
    print(url)
    r = requests.get(url)
    return r.text
    j = r.json()
    if 'total' in j and 'count' in j:
        current_app.config['WX_USER_TOTAL'] = j['total']
        current_app.config['WX_USER_COUNT'] = j['count']
        if j['count'] > 0:
            return j['data']
        else:
            return ''
    else:
      abort(500)       
