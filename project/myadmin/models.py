from django.db import models

# Create your models here.
class Users(models.Model):

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=80)
    email = models.CharField(max_length = 50)
    sex = models.CharField(max_length = 50)
    age = models.IntegerField(null = True)
    phone = models.CharField(max_length = 50)

    # 0 正常  1禁用 
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)


    pic = models.CharField(max_length = 200,default = "/static/pics/user.jpg")
    
    
