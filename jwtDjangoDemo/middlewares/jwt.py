# -*- coding:utf-8 -*-
import re

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

from utils.jwt_auth import parse_payload

#   白名单
WHITE_LIST = ["/admin/.*","/login/","/"]


class JwtQueryParamMiddleware(MiddlewareMixin):
    """
    用户需要在url中通过参数进行传输token，例如：
    127.0.0.1:8001/order?token=eyJ0eXAiOiJqd3QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IndodyIsImV4cCI6MTU3NDQ5MTQ0MX0.K-k40u6XCvjDiYjhyfIqKsbrN4DCYkytqmdPHmBl9k0
    """
    def process_request(self, request):
        print(request.path_info)
        # 白名单放行
        for i in WHITE_LIST:
            if re.search(request.path_info,i):
                return
        # 校验非登录页面的get请求
        token = request.GET.get('token')
        result = parse_payload(token)
        if not result['status']:
            return JsonResponse(result,json_dumps_params={'ensure_ascii':False})
        request.user_info = result['data']
        return

class JwtAuthorizationMiddleware(MiddlewareMixin):
    """
    用户需要通过请求头的方式来进行传输token，例如（注意必须写成下面这种格式）：
    Authorization:jwt eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzM1NTU1NzksInVzZXJuYW1lIjoid3VwZWlxaSIsInVzZXJfaWQiOjF9.xj-7qSts6Yg5Ui55-aUOHJS4KSaeLq5weXMui2IIEJU
    """
    def process_request(self, request):

        # 白名单放行
        for i in WHITE_LIST:
            if re.search(request.path_info, i):
                return

        # 非登录页面需要校验token
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        auth = authorization.split()
        if not auth:
            return JsonResponse({'error': '未获取到Authorization请求头', 'status': False})
        if auth[0].lower() != 'jwt':
            return JsonResponse({'error': 'Authorization请求头中认证方式错误', 'status': False})
        if len(auth) == 1:
            return JsonResponse({'error': "非法Authorization请求头", 'status': False})
        elif len(auth) > 2:
            return JsonResponse({'error': "非法Authorization请求头", 'status': False})

        token = auth[1]
        result = parse_payload(token)
        if not result['status']:
            return JsonResponse(result)
        request.user_info = result['data']
