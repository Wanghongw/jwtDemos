# -*- coding:utf-8 -*-
import os

import tornado.ioloop
import tornado.web

from handlers import views


SETTINGS = {
    "debug":True,
    "template_path":os.path.join(os.path.dirname(__file__),"templates"),
}


def make_app():
    return tornado.web.Application(
        [
            (r"/v1", views.MainHandler),
            (r"/v1/order", views.OrderHandler),
        ],
        # 配置
        **SETTINGS,
    )


if __name__ == '__main__':
    # print(os.path.dirname(__file__))
    app = make_app()
    app.listen(9898)
    tornado.ioloop.IOLoop.current().start()
