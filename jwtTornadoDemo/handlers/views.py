# -*- coding:utf-8 -*-
import json

import tornado.web
from tornado.escape import json_encode

from utils import jwt_auth
from . import base_handler


# 用于生成token的登陆逻辑继承BaseHandler！
class MainHandler(base_handler.BaseHandler):

    def get(self,*args,**kwargs):
        self.render("login.html")

    def post(self, *args, **kwargs):
        err_dic = {"status":False,"error":"用户名或密码错误"}

        name = self.get_argument("username")
        pwd = self.get_argument("password")
        if name == "whw" and pwd == "666":
            # 用户名密码正确 给用户生成token并返回
            token = jwt_auth.create_token({"username":"whw"})
            self.write(json_encode(token))
        else:
            ret = json.dumps(err_dic,ensure_ascii=False)
            self.write(ret)


# 其他需要jwt校验的继承TokenHandler！
class OrderHandler(base_handler.TokenHandler):

    def get(self):
        if self.token_passed:
            self.write("<h1>订单列表</h1>")
            self.write(self.token_msg)
        else:
            self.write(self.token_msg)

    def post(self, *args, **kwargs):
        if self.token_passed:
            self.write("添加订单")
            self.write(self.token_msg)
        else:
            self.write(self.token_msg)

    def put(self, *args, **kwargs):
        if self.token_passed:
            self.write("修改订单")
            self.write(self.token_msg)
        else:
            self.write(self.token_msg)

    def delete(self, *args, **kwargs):
        if self.token_passed:
            self.write("删除订单")
            self.write(self.token_msg)
        else:
            self.write(self.token_msg)

