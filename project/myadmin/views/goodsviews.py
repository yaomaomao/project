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
    
    # 获取搜索条件
    type = request.GET.get('type',None)
    kwords = request.GET.get('keywords',None)

    if type:

        if type == 'all':
            from django.db.models import Q
            goodslist = Goods.objects.filter(
                Q(goods__contains=kwords)|
                Q(descr__contains=kwords)|
                Q(price__contains=kwords)|
                Q(store__contains=kwords)|
                Q(info__contains=kwords)   
            )
        elif type == "goods":
            goodslist = Goods.objects.filter(goods__contains=kwords)
        elif type == "descr":
            goodslist = Goods.objects.filter(descr__contains=kwords)
        elif type == "price":
            goodslist = Goods.objects.filter(price__contains=kwords)
        elif type == "store":
            goodslist = Goods.objects.filter(store__contains=kwords)
        elif type == "info":
            goodslist = Goods.objects.filter(info__contains=kwords)
    else:

        goodslist = Goods.objects.all()

    # 分页
    from django.core.paginator import Paginator
    # 实例化分页对象，参数1：数据集合，参数2：每页显示 的条数
    paginator = Paginator(goodslist,5)
    # 获取当前的页码
    page = request.GET.get('p',1)
    # 获取当前页的数据
    ulist = paginator.page(page)


    context = {"goodslist":ulist}

    return render(request,"myadmin/goods/list.html",context)


#  删除商品
def delete(request):
    try:
        # 获取id
        uid = request.GET.get('gid',None)
        # 获取对象
        goods = Goods.objects.get(id=uid)
        
        if goods.pics:
            # /static/pics/
            os.remove('.'+goods.pics)
        goods.delete()
        context = {"msg":"删除成功！","type":0}
        return JsonResponse(context)
    except:
        context = {"msg":"删除失败！","type":1}
        return JsonResponse(context)


# 修改
def edit(request):

    goods_id = request.GET.get("gid",None)

    goods = Goods.objects.get(id=goods_id)

    if request.method == "GET":

        return render(request,"myadmin/goods/edit.html",{"goods":goods})

    elif request.method == "POST":
        try:
            # 判断是否上传了新的图片
            if request.FILES.get('pics',None):
                if goods.pics:
                    os.remove('.'+goods.pics)
                goods.pics = uploads(request)

            goods.goods = request.POST['goods']
            goods.descr = request.POST['descr']
            goods.price = request.POST['price']
            goods.store = request.POST['store']
            goods.info = request.POST['info']
            
            print(goods)
            goods.save()
            
            return HttpResponse("<script>alert('修改成功！');location.href='"+reverse('myadmin_goods_list') +"'</script>")
        except:
            return HttpResponse("<script>alert('修改失败！');location.href='"+reverse('myadmin_goods_edit') +'?uid='+str(goods.id)+"'</script>")

        
