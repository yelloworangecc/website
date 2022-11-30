from .Member import Member
from flask import render_template
from .TopK import TopK

class InvalidMethod(Exception):
    pass

class MemberController():
    top10Points = TopK(10)
    top10Times = TopK(10)

    def __init__(self,request):
        self.request = request
        self.phone_arg = None
        if 'phone' in request.args:
            self.phone_arg = request.args['phone']
            self.member = Member(self.phone_arg)
        else:
            self.member = Member(None)

    def getPhone(self):
        phone = self.member.phone()
        if phone is None:
            phone = self.phone_arg
        return phone
        
    def getName(self):
        return self.member.name()

    def getPoint(self):
        return self.member.point()

    def getTime(self):
        return self.member.time()

    def getLastTime(self):
        return self.member.lastTime()

    @staticmethod
    def genTop10():
        MemberController.top10Points.clear()
        MemberController.top10Times.clear()
        for json_member in Member.db.load():
            member=Member(json_member["phone"])
            MemberController.top10Points.update((member.point(),member))
            MemberController.top10Times.update((member.time(),member))

    @staticmethod
    def getTop10Points():
        return MemberController.top10Points.getList()

    @staticmethod
    def getTop10Times():
        return MemberController.top10Times.getList()
        
        
    def handle_request(self):
        if self.request.method == 'GET':
            pass
        elif self.request.method == 'POST':
            # new phone
            if self.member.phone() is None:
                print(self.phone_arg)
                self.member.setPhone(self.phone_arg)
            # compare & update name
            member_name = self.member.name()
            form_name = self.request.form['name']
            if member_name != form_name:
                self.member.setName(form_name)
            # add point
            point=int(self.request.form['point'])
            point=abs(point)
            if 'minus' in self.request.form:
                point = -point
            self.member.addPoint(point)
            # update database & top 10
            self.member.updateDB()
            MemberController.genTop10()
        else:
            raise InvalidMethod('Only support method GET and POST')

        return render_template('member.html',memberController=self)
            
MemberController.genTop10()
