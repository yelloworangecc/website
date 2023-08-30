import json,time,os,socket

wx_gz_id = os.getenv('WX_GZ_ID')
reply_text_template = '''<xml>
<ToUserName><![CDATA[{0}]]></ToUserName>
<FromUserName><![CDATA[{1}]]></FromUserName>
<CreateTime>{2}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{3}]]></Content>
</xml>'''

def DBProxy_exec(json_data):
    data = json.dumps(json_data)
    print(data)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(data.encode(),("127.0.0.1", 9999))
        data, from_addr = sock.recvfrom(1024)
        print(data)
        return json.loads(data.decode())
    return None

class WXStateInit:
    def __init__(self, WX_Manager):
        self.wx_manager = WX_Manager

    def handle(self,data):
        # data example
        # {'ToUserName': 'gh_f2cf37fb95e6', 'FromUserName': 'otFB85v-7XCAQwS1Cj7rEt8XXwsU',  'CreateTime': '1692767220', 'MsgType': 'event', 'Event': 'CLICK', 'EventKey': 'HUI_USER_POINTS'}
        # {'ToUserName': 'gh_f2cf37fb95e6', 'FromUserName': 'otFB85v-7XCAQwS1Cj7rEt8XXwsU', 'CreateTime': '1692772409', 'MsgType': 'text', 'Content': '18112682607', 'MsgId': '24234674440793207'}
        if 'EventKey' in data and data['EventKey'] == 'HUI_USER_BONDING':
            self.wx_manager.state = WXStateBonding(self.wx_manager)
            return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), '请输入在本店注册会员时登记的手机号码')
        if 'EventKey' in data and data['EventKey'] == 'HUI_USER_POINTS':
            sql = "SELECT SYJF FROM BM_WLDW WHERE CZ='{0}'".format(self.wx_manager.wx_id)
            json_data={}
            json_data['SQL']=sql
            json_data = DBProxy_exec(json_data)
            if json_data and isinstance(json_data,list) and json_data[0] and isinstance(json_data[0],list):
                return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), json_data[0][0])
            else:
                return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), '查询失败,如果未绑定会员请先绑定会员')
            
class WXStateBonding:
    def __init__(self, WX_Manager):
        self.wx_manager = WX_Manager

    def handle(self, data):
        if 'Content' in data:
            sql = "UPDATE BM_WLDW SET CZ='{0}' WHERE DH = '{1}'".format(self.wx_manager.wx_id , data['Content'])
            json_data={}
            json_data['SQL']=sql
            json_data = DBProxy_exec(json_data)
            self.wx_manager.state = WXStateInit(self.wx_manager)
            if json_data and json_data[0] == 1:
                return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), '绑定成功')
            else:
                return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), '绑定失败')
        else:
            return None

class WXManager:
    cached_managers = {}

    def __init__(self, WX_ID):
        self.wx_id=WX_ID
        self.state=WXStateInit(self)
        self.time=int(time.time())

    def isExpired(self,cur_time):
        if cur_time - self.time > 1200:
            return True
        return False

    def handle(self,data):
        result = self.state.handle(data)
        
        # clean the cached managers
        if isinstance(self.state,WXStateInit):
            for wx_id in WXManager.cached_managers:
                wx_manager=WXManager.get(wx_id)
                if wx_manager.isExpired(int(time.time())):
                    WXManager.remove(wx_id)

        return result

    @staticmethod
    def get(WX_ID):
        if WX_ID not in WXManager.cached_managers:
            WXManager.cached_managers[WX_ID] = WXManager(WX_ID)
        return WXManager.cached_managers[WX_ID]

    @staticmethod
    def remove(WX_ID):
        if WX_ID in WXManager.cached_managers:
            WXManager.cached_managers.pop(WX_ID)
