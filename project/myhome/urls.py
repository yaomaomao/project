"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views
urlpatterns = [
    # 首页
    url(r'^$', views.index,name="myhome_index"),
    # 注册
    url(r'^register$', views.register,name="myhome_register"),
    # 登录
    url(r'^login$', views.login,name="myhome_login"),
    # 列表
    url(r'^list$', views.userlist,name="myhome_list"),
    # 详情
    url(r'^info$', views.info,name="myhome_info"),
    # 验证码
    url(r'^vcode$', views.vcode,name="myhome_vcode"),
    # 验证码
    url(r'^code$', views.code,name="myhome_code"),
    # ajax用户名验证
    url(r'^username$', views.username,name="myhome_username"),
    # 用户登出
    url(r'^logout$', views.logout,name="myhome_logout"),


]
