# -*- coding:utf-8 -*-
from django.conf.urls import re_path

from api import views

urlpatterns = [
    re_path(r"^login/$",views.LoginView.as_view(),name="login"),
    re_path(r"^order/$",views.OrderView.as_view(),name="order"),
]

