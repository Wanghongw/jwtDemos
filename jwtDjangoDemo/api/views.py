from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from utils.jwt_auth import create_token

@method_decorator(csrf_exempt,name="dispatch")
class LoginView(View):

    # 登陆页面
    def get(self,request,*args,**kwargs):
        return render(request,"login.html")

    # post方式提交表单就行用户名密码校验，通过的话生成token
    def post(self,request,*args,**kwargs):
        user = request.POST.get("username")
        pwd = request.POST.get("password")
        # print(user,pwd)
        # 这里进行用户名密码的校验
        if user == "whw" and pwd == "666":
            # 校验成功为用户生成token
            token = create_token({"username":"whw"})
            return JsonResponse(
                {"status":True,"token":token}
            )
        # 当然，这一步也可以将token的值存在本地缓存中，为了方便直接返回给浏览器
        # 用户下一次登陆时将之前生成的token值复制，当作是请求de参数即可
        return JsonResponse(
            # 防止中文显示ascii码
            {"status": False, "error":"用户名或密码错误"},json_dumps_params={'ensure_ascii':False}
        )

@method_decorator(csrf_exempt,name="dispatch")
class OrderView(View):

    def get(self, request, *args, **kwargs):
        print(request.user_info)
        return JsonResponse({'data': '订单列表'},json_dumps_params={'ensure_ascii':False})

    def post(self, request, *args, **kwargs):
        print(request.user_info)
        return JsonResponse({'data': '添加订单'},json_dumps_params={'ensure_ascii':False})

    def put(self, request, *args, **kwargs):
        print(request.user_info)
        return JsonResponse({'data': '修改订单'},json_dumps_params={'ensure_ascii':False})

    def delete(self, request, *args, **kwargs):
        print(request.user_info)
        return JsonResponse({'data': '删除订单'},json_dumps_params={'ensure_ascii':False})
