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

from .views import views,userviews,typesviews,goodsviews
urlpatterns = [
    url(r'^$', views.index,name='myadmin_index'),  
    url(r'^useradd$', userviews.add,name='myadmin_user_add'),  
    url(r'^userlist$', userviews.list,name='myadmin_user_list'),  
    url(r'^userdelete$', userviews.delete,name='myadmin_user_delete'),  
    url(r'^useredit$', userviews.edit,name='myadmin_user_edit'),  
    # 分类操作
    url(r'^typesadd$', typesviews.add,name='myadmin_types_add'),  
    url(r'^typeslist$', typesviews.list,name='myadmin_types_list'),  
    url(r'^typesdelete$', typesviews.delete,name='myadmin_types_delete'),  
    url(r'^typesedit$', typesviews.edit,name='myadmin_types_edit'), 
    # 商品操作
    url(r'^goods/add$', goodsviews.add,name='myadmin_goods_add'),  
    url(r'^goods/list$', goodsviews.list,name='myadmin_goods_list'),  
    url(r'^goods/delete$', goodsviews.delete,name='myadmin_goods_delete'),  
    url(r'^goods/edit$', goodsviews.edit,name='myadmin_goods_edit'), 
]
