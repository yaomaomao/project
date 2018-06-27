from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from myadmin.models import Users,Goods,Types

from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
# 首页
def index(request):

    '''

    '''
    # 获取顶级的分类
    typeslist = Types.objects.filter(pid=0)

    typegoods = []
    for type in typeslist:
        # 获取一级分类
        type.sub = Types.objects.filter(pid = type.id)
        
        for t in type.sub:
            # 获取商品信息
            t.goodslist = Goods.objects.filter(typeid = t.id)
            typegoods.append(t)
    
    context = {"typeslist":typeslist,"typegoods":typegoods}     

    return render(request,"myhome/index.html",context)

# 注册
def register(request):
    if request.method == "GET":

        return render(request,"myhome/register.html")
    
    elif request.method == "POST":

        data = request.POST.copy().dict()

        del data['csrfmiddlewaretoken']
        try:
            # 加密
            data['password']= make_password(data['password'], None, 'pbkdf2_sha256')
            user = Users.objects.create(**data)
            # 写入session
            request.session['User'] = {'uid':user.id,'username':user.username}

            return HttpResponse("<script>alert('注册成功，跳转到首页！');location.href=('/')</script>")
        except:
            return HttpResponse('<script>alert("注册失败");history.back(-1)</script>')
            # return HttpResponse('<script>alert("添加失败");location.href="'+reverse('myadmin_goods_add')+'"</script>')
            # return HttpResponse("<script>alert('注册失败！');location.href='"+reverse('myhome_register')+"'</script>")

# 列表
def userlist(request,tid):

    goodslist = Goods.objects.filter(typeid = tid)

    return render(request,"myhome/list.html",{"goodslist":goodslist})

# 登录
def login(request):
    if request.method == 'GET':

        return render(request,"myhome/login.html")

    elif request.method == 'POST':

        name = request.POST.get('username',None)
        pwd = request.POST.get('password',None)
        if name == '' or pwd == '':
            return HttpResponse('<script>alert("用户名或密码不能为空！");history.back(-1)</script>') 
        user  = Users.objects.filter(username = name)
        print(user)
        if user:
            # 验证密码
            res = check_password(pwd,user.password)

            if res:
                 # 密码正确
                request.session['User'] = {'uid':user.id,'username':user.username}
                return HttpResponse("<script>alert('登录成功，跳转到首页！');location.href=('/')</script>")
            else:
                pass
        return HttpResponse('<script>alert("用户名或密码错误！");history.back(-1)</script>') 

# 登出
def logout(request):

    request.session['User'] = {}
    
    return HttpResponse('<script>alert("登出成功");location.href="/"</script>')

# 详情
def info(request,goodsid):

    goods = Goods.objects.get(id = goodsid)

    return render(request,"myhome/info.html",{"goods":goods})

# ajax验证验证码
def code(request):

    vcode = request.GET['code'].upper()
    if request.session['verifycode'].upper() == vcode:
        context = {"msg":"验证码正确！","type":0}
        return JsonResponse(context)
    else:
        context = {"msg":"验证码输入有误，请重新输入","type":1}
        return JsonResponse(context)

# ajax验证用户名
def username(request):

    username = request.GET.get('username',None)

    num = Users.objects.filter(username = username).count()

    if num == 0:
        context = {"msg":"用户名可用！","type":0}
        return JsonResponse(context)
    else:
        context = {"msg":"用户名已存在！","type":1}
        return JsonResponse(context)
    
# 验证码
def vcode(request):
    
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
