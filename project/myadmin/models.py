from django.db import models

# Create your models here.
class Users(models.Model):

    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=80)
    email = models.CharField(max_length = 50)
    sex = models.CharField(max_length = 50,null=True)
    age = models.IntegerField(null = True)
    phone = models.CharField(max_length = 50,null=True)

    # 0 正常  1禁用 
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)


    pic = models.CharField(max_length = 200,default = "/static/pics/user.jpg")
    
class Types(models.Model):

    name = models.CharField(max_length = 50) 
    pid = models.IntegerField() 

    path = models.CharField(max_length = 255)

class Goods(models.Model):

    typeid =  models.ForeignKey(to="Types", to_field="id")
    goods = models.CharField(max_length = 50)
    descr = models.TextField(null=True)
    price = models.FloatField(null=True)
    
    info = models.TextField(null=True)
    pics = models.CharField(max_length = 255)
    # 状态
    state = models.IntegerField(default=0,null=True)
    # 库存
    store = models.IntegerField(default=0)
    # 被点击的次数
    clicknum = models.IntegerField(default=0)
    num = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)
