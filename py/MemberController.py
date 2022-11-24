from .Member import Member
from flask import render_template
from .TopK import TopK

class InvalidMethod(Exception):
    pass

class MemberController():
    top10Points = []
    top10Times = []

    def __init__(self,request):
        self.request = request
        self.member = Member(request.args['phone'])

    def getPhone(self):
        return self.member.phone()
        
    def getName(self):
        return self.member.name()

    def getPoints(self):
        return self.member.points()

    def getTimes(self):
        return self.member.times()

    def getLastTime(self):
        return self.member.lastTime()

    @staticmethod
    def genTop10():
        MemberController.top10Points.clear()
        MemberController.top10Points.clear()
        for json_member in db:
            member=Member(json_member["phone"])
            MemberController.top10Points.update(member,Member.comparePoints)
            MemberController.top10Times.update(member,Member.compareTimes)

    @staticmethod
    def getTop10Points():
        return MemberController.top10Points.getList()

    @staticmethod
    def getTop10Times():
        return MemberController.top10Times.getList()
        
        
    def handle_request(self):
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            # new phone
            if self.member.phone() is None:
                self.member.setPhone(request.args['phone'])
            # compare & update name
            member_name = self.member.name()
            form_name = request.form['name']
            if member_name != form_name:
                member.setName(self, form_name)
            # add point
            point=int(request.form['point'])
            if 'minus' in request.form:
                point = -point
            self.member.addPoint(point)
            # update database & top 10
            self.member.updateDB()
            MemberController.genTop10()
        else:
            raise InvalidMethod('Only support method GET and POST')

        return render_template('member.html',memberController=self)
            
MemberController.genTop10()
