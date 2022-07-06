import json

class User():
    def __init__(self, name, phone, password):
        print("__init__")
        self.username = name
        self.phone = phone
        self.password = password
        self.isAuthenticated = False

    def verify_password(self, password):
        print("verify_password")
        if self.password == password:
            isAuthenticated = True
        return isAuthenticated

    def get_id(self):
        print("get_id")
        return self.phone

    def is_authenticated(self):
        print("is_authenticated")
        return isAuthenticated

    def is_active(self):
        print("is_active")
        return True

    def is_anonymous(self):
        print("is_anonymous")
        return True

    @staticmethod
    def get(phone):
        fp = open('json/Users.json','r',encoding='utf8')
        users = json.load(fp)
        for user in users:
            if user["phone"] == phone:
                print("user found")
                return User(user["name"],user["phone"],user["password"])
        print("user not found")
        return None

    @staticmethod
    def set(name,phone,password):
        fp = io.open('../json/Users.json','r',encoding='utf8')
        users = json.load(fp)
        isFind = False
        for user in users:
            if user["phone"] == phone:
                # modify
                user["name"] = name
                user["password"] = password
                isFind = True
                break
        if not isFind:
            user = json.loads('{}')
            user["phone"] = phone
            user["name"] = name
            user["password"] = password
            users.append(user)
        return None

