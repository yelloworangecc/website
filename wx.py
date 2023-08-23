import hashlib,os,requests,time
from xml.etree import ElementTree

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
            # print(request.args) ImmutableMultiDict([('signature', '1f8d060e9d62bba50f6c4aac90765cf67e7fe098'), ('timestamp', '1692767175'), ('nonce', '467465726'), ('openid', 'otFB85v-7XCAQwS1Cj7rEt8XXwsU')])
            print(data)
            # {'ToUserName': 'gh_f2cf37fb95e6', 'FromUserName': 'otFB85v-7XCAQwS1Cj7rEt8XXwsU', 'CreateTime': '1692767220', 'MsgType': 'event', 'Event': 'CLICK', 'EventKey': 'HUI_USER_POINTS'}
            # {'ToUserName': 'gh_f2cf37fb95e6', 'FromUserName': 'otFB85v-7XCAQwS1Cj7rEt8XXwsU', 'CreateTime': '1692772409', 'MsgType': 'text', 'Content': '18112682607', 'MsgId': '24234674440793207'}
            # TODO: 向用户推送消息
            if 'EventKey' in data and data['EventKey'] == 'HUI_USER_BONDING':
                return '''<xml>
<ToUserName><![CDATA[{0[FromUserName]}]]></ToUserName>
<FromUserName><![CDATA[{0[ToUserName]}]]></FromUserName>
<CreateTime>{1}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{2}]]></Content>
</xml>'''.format(data,int(time.time()),'请输入在本店注册会员时登记的手机号码')
            if 'EventKey' in data and data['EventKey'] == 'HUI_USER_POINTS':
                return '''<xml>
<ToUserName><![CDATA[{0[FromUserName]}]]></ToUserName>
<FromUserName><![CDATA[{0[ToUserName]}]]></FromUserName>
<CreateTime>{1}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{2}]]></Content>
</xml>'''.format(data,int(time.time()), 100)
            if 'Content' in data:
                return '''<xml>
<ToUserName><![CDATA[{0[FromUserName]}]]></ToUserName>
<FromUserName><![CDATA[{0[ToUserName]}]]></FromUserName>
<CreateTime>{1}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{2}]]></Content>
</xml>'''.format(data,int(time.time()), '绑定成功')
            return '''<xml>
 61<ToUserName><![CDATA[{0[FromUserName]}]]></ToUserName>
 62<FromUserName><![CDATA[{0[ToUserName]}]]></FromUserName>
 63<CreateTime>{1}</CreateTime>
 64<MsgType><![CDATA[text]]></MsgType>
 65<Content><![CDATA[{2}]]></Content>
 66</xml>'''.format(data,int(time.time()), '出错，此功能暂时不可用')
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
