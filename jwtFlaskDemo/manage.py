# -*- coding:utf-8 -*-
from flask import Flask, request, jsonify, render_template, g

from utils.jwt_auth import create_token, parse_payload

app = Flask(__name__)


# 通过url传递token
@app.before_request
def jwt_query_params_auth():
    if request.path == '/login/':
        return
    token = request.args.get('token')
    result = parse_payload(token)
    if not result['status']:
        return jsonify(result)
    g.user_info = result['data']

# 通过Authorization请求头传递token
"""
@app.before_request
def jwt_authorization_auth():
    if request.path == '/login/':
        return
    authorization = request.headers.get('Authorization', '')
    auth = authorization.split()
    if not auth:
        return jsonify({'error': '未获取到Authorization请求头', 'status': False})
    if auth[0].lower() != 'jwt':
        return jsonify({'error': 'Authorization请求头中认证方式错误', 'status': False})

    if len(auth) == 1:
        return jsonify({'error': "非法Authorization请求头", 'status': False})
    elif len(auth) > 2:
        return jsonify({'error': "非法Authorization请求头", 'status': False})

    token = auth[1]
    result = parse_payload(token)
    if not result['status']:
        return jsonify(result)
    g.user_info = result['data']
"""

@app.route('/login/', methods=['GET','POST'])
def login():
    # GET请求返回登陆页面
    if request.method == "GET":
        return render_template("login.html")
    # POST 方法 认证
    user = request.form.get('username')
    pwd = request.form.get('password')
    # 检测用户和密码是否正确，此处可以在数据进行校验。
    if user == 'whw' and pwd == '666':
        # 用户名和密码正确，给用户生成token并返回
        token = create_token({'username': 'wupeiqi'})
        return jsonify({'status': True, 'token': token})
    return jsonify({'status': False, 'error': '用户名或密码错误'})


@app.route('/order/', methods=['GET', "POST", "PUT", "DELETE"])
def order():
    print(g.user_info)
    if request.method == 'GET':
        return "订单列表"
    return "订单信息"


if __name__ == '__main__':
    app.run()
