# -*- coding:utf-8 -*-
import re
import json

import tornado.web

from utils import jwt_auth


# 白名单
WHITE_LIST = ["/login","/"]

# 进行预设 继承tornado的RequestHandler
class BaseHandler(tornado.web.RequestHandler):

    def prepare(self):
        super(BaseHandler, self).prepare()

    def set_default_headers(self):
        super().set_default_headers()


# 进行token校验，继承上面的BaseHandler
class TokenHandler(BaseHandler):

    def prepare(self):
        ### 通过url传递token ###
        """
        # print(self.request.uri)
        # print(self.request.uri.get("token"))# /order?token=666
        # print(self.request.arguments)# {'token': [b'666']}
        ret = self.request.arguments.get("token","")
        # print(ret,type(ret[0])) # b'666' bytes
        # 最终结果
        # print(ret[0].decode("utf-8"))
        token = ret[0].decode("utf-8")
        result = (jwt_auth.parse_payload(token))
        if not result["status"]:
            self.token_passed = False
        else:
            self.token_passed = True
        self.token_msg = json.dumps(result, ensure_ascii=False)
        """
        ### 通过Authorization请求头传递token ###
        head = self.request.headers
        authorization = head.get("Authorization","")
        auth = authorization.split()
        if not auth:
            self.token_passed = False
            result = {'error': '未获取到Authorization请求头', 'status': False}
            self.token_msg = json.dumps(result, ensure_ascii=False)
            return
        if auth[0].lower() != 'jwt':
            self.token_passed = False
            result = {'error': 'Authorization请求头中认证方式错误', 'status': False}
            self.token_msg = json.dumps(result, ensure_ascii=False)
            return
        if len(auth) == 1:
            self.token_passed = False
            result = {'error': "非法Authorization请求头", 'status': False}
            self.token_msg = json.dumps(result, ensure_ascii=False)
            return
        elif len(auth) > 2:
            self.token_passed = False
            result = {'error': "非法Authorization请求头", 'status': False}
            self.token_msg = json.dumps(result, ensure_ascii=False)
            return
        token = auth[1]
        result = jwt_auth.parse_payload(token)
        if not result["status"]:
            self.token_passed = False
        else:
            self.token_passed = True
        self.token_msg = json.dumps(result, ensure_ascii=False)
