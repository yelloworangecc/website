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
        data, from_addr = sock.recvfrom(10240)
        print(data)
        return json.loads(data.decode())
    return None

def DBProxy_getDrugs(drugName):
    sql = "SELECT SUM(SL), YPMC, SCCJ FROM XSD_MX WHERE YPMC like '%{0}%' group by YPMC, SCCJ".format(drugName)
    sale_data={}
    sale_data['SQL']=sql
    sale_data = DBProxy_exec(sale_data)
    if not sale_data and not isinstance(sale_data,list) and not sale_data[0] and not isinstance(sale_data[0],list):
        return None

    sql = "SELECT SUM(SL), YPMC, SCCJ FROM RKD_MX WHERE YPMC like '%{0}%' group by YPMC, SCCJ".format(drugName)
    receipt_data={}
    receipt_data['SQL']=sql
    receipt_data = DBProxy_exec(receipt_data)
    if not receipt_data and not isinstance(receipt_data,list) and not receipt_data[0] and not isinstance(receipt_data[0],list):
        return None

    for receipt_item in receipt_data:
        for sale_item in sale_data:
            if sale_item[1] == receipt_item[1] and sale_item[2] == receipt_item[2]:
                receipt_item[0] = float(receipt_item[0]) - float(sale_item[0])
    return receipt_data
    
class WXStateInit:
    def __init__(self, WX_Manager):
        self.wx_manager = WX_Manager

    def handle(self,data):
        
        if 'EventKey' in data and data['EventKey'] == 'HUI_USER_BONDING':
            phone = self.wx_manager.getPhone()
            if phone:
                return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), '您已绑定过会员号({0})，如需更改请留言“重新绑定会员号+手机号码”'.format(phone))

            self.wx_manager.state = WXStateBonding(self.wx_manager)
            return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), '请输入在本店注册会员时登记的手机号码')

        elif 'EventKey' in data and data['EventKey'] == 'HUI_USER_POINTS':
            sql = "SELECT SYJF FROM BM_WLDW WHERE CZ='{0}'".format(self.wx_manager.wx_id)
            json_data={}
            json_data['SQL']=sql
            json_data = DBProxy_exec(json_data)
            if json_data and isinstance(json_data,list) and json_data[0] and isinstance(json_data[0],list):
                points = json_data[0][0]
                if not points:
                    points = 0
                msg = '您的积分余额为: {0} (在门店每消费一元累积一个积分）'.format(points)
                return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), msg)
            else:
                return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), '查询失败,如果未绑定会员请先绑定会员')
        elif 'EventKey' in data and data['EventKey'] == 'HUI_USER_DRUGS':
            self.wx_manager.state = WXStateQueryDrugs(self.wx_manager)
            return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), '请输入药品名称')
        elif 'EventKey' in data and data['EventKey'] == 'HUI_USER_PURCHASE':
            return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), '该功能正在开发,敬请期待')
        elif 'EventKey' in data and data['EventKey'] == 'HUI_USER_MESSAGE':
            return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), '该功能正在开发,敬请期待')
        else:
            return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), '公众号暂时无法识别该指令')
            
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
        
class WXStateQueryDrugs:
    def __init__(self, WX_Manager):
        self.wx_manager = WX_Manager

    def handle(self, data):
        if 'Content' in data:
            data = DBProxy_getDrugs(data['Content'])
            
            if len(data) > 10:
                return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), '查询结果过多，请您提供更准确的药品名称')

            self.wx_manager.state = WXStateInit(self.wx_manager)
            result = "名称\t厂家\t数量\n--------------------"
            for item in data:
                if item[0] > 0:
                    result = "{0}\n{1}\t{2}\t{3}".format(result, item[1], item[2], item[0])
            result = result + "\n--------------------\n查询成功,数据可能存在误差，仅供参考"
            return reply_text_template.format(self.wx_manager.wx_id, wx_gz_id, int(time.time()), result)
        else:
            return None
        
class WXManager:
    cached_managers = {}

    def __init__(self, WX_ID):
        self.wx_id=WX_ID
        self.state=WXStateInit(self)
        self.time=int(time.time())

    def getPhone(self):
        sql = "SELECT TOP 1 DH FROM BM_WLDW WHERE CZ='{0}'".format(self.wx_id)
        json_data = {}
        json_data['SQL'] = sql
        json_data = DBProxy_exec(json_data)
        if json_data and isinstance(json_data,list) and json_data[0] and isinstance(json_data[0],list) and json_data[0][0]:
            return json_data[0][0]
        else:
            return None

    def isExpired(self,cur_time):
        if cur_time - self.time > 300:
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
