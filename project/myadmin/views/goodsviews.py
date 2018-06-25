from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
import os
from ..models import Users,Goods,Types
 # Create your views here.
def add(request):
    # get请求 会转到添加页面
    if request.method == "GET":

        tlist = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')

        for x in tlist:
            if x.pid == 0:
                x.pname = '顶级分类'
            else:
                t = Types.objects.get(id=x.pid)
                x.pname = t.name
            num  = x.path.count(',')-1
            x.name = (num*'|----')+x.name


        return render(request,"myadmin/goods/add.html",{"typeslist":tlist})

    elif request.method == "POST":
        try:
            data = request.POST.copy().dict()

            del data['csrfmiddlewaretoken']

            #  图片处理
            if request.FILES.get('pics',None):

                data['pics'] = uploads(request)
                if  data['pics'] == 1:
                    return HttpResponse('<script>alert("上传的文件类型不符合要求");location.href="'+reverse('myadmin_goods_add')+'"</script>')
            print(data)
            data['typeid'] = Types.objects.get(id = data['typeid'])
        
            print(data)
            Goods.objects.create(**data)
            
            return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_goods_list')+'"</script>')
        
        except:
            return HttpResponse('<script>alert("添加失败");location.href="'+reverse('myadmin_goods_add')+'"</script>')
            
# 执行文件的上传
def uploads(request):
    
    # 获取请求中的 文件 File 
    myfile = request.FILES.get('pics',None)

    # 获取上传的文件后缀名 myfile.name.split('.').pop()
    p = myfile.name.split('.').pop()
    arr = ['jpg','png','jpeg','gif']
    if p not in arr:
        return 1

    import time,random
    # 生成新的文件名
    filename = str(time.time())+str(random.randint(1,99999))+'.'+p
    
    # 打开文件
    destination = open("./static/pics/"+filename,"wb+")

    # 分块写入文件  
    for chunk in myfile.chunks():      
       destination.write(chunk)  

    # # destination.write(myfile.read()) #不推荐

    # 关闭文件
    destination.close()
    
    # return HttpResponse(filename)

    return '/static/pics/'+filename

# 列表
def list(request):

    
    goodslist = Goods.objects.all()
    
    context = {"goodslist":goodslist}
    print(goodslist)
    for v in goodslist:
        print(v)
    return render(request,"myadmin/user/list.html",context)


#  删除会员
def delete(request):
    try:
        # 获取id
        uid = request.GET.get('uid',None)
        # 获取对象
        user = Users.objects.get(id=uid)
        if user.pic:
            # /static/pics/
            os.remove('.'+user.pic)
        user.delete()
        context = {"msg":"删除成功！","type":0}
        return JsonResponse(context)
    except:
        context = {"msg":"删除失败！","type":1}
        return JsonResponse(context)


# 修改
def edit(request):

    user_id = request.GET.get("uid",None)

    user = Users.objects.get(id=user_id)

    if request.method == "GET":

        return render(request,"myadmin/user/edit.html",{"user":user})

    elif request.method == "POST":
        try:
            # 判断是否上传了新的图片
            if request.FILES.get('pic',None):
                if user.pic:
                    os.remove('.'+user.pic)
                user.pic = uploads(request)

            user.username = request.POST['username']
            user.email = request.POST['email']
            user.age = request.POST['age']
            user.sex = request.POST['sex']
            user.phone = request.POST['phone']
            
            print(user)
            user.save()
            
            return HttpResponse("<script>alert('修改成功！');location.href='"+reverse('myadmin_user_list') +"'</script>")
        except:
            return HttpResponse("<script>alert('修改失败！');location.href='"+reverse('myadmin_user_edit') +'?uid='+str(user.id)+"'</script>")

        
