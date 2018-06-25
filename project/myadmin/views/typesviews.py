from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
import os
from ..models import Types

# 获取typeslist
def gettypesorder(request):
    # 按条件来缩进并排序
    tlist = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')

    for x in tlist:
        if x.pid == 0:
            x.pname = '顶级分类'
        else:
            t = Types.objects.get(id=x.pid)
            x.pname = t.name
        num  = x.path.count(',')-1
        x.name = (num*'|----')+x.name


    return tlist

# 列表页面
def list(request):
    types = request.GET.get('type',None)
    keywords = request.GET.get('keywords',None)
    typeslist = gettypesorder(request)
    
    for type in typeslist:

        if type.pid == 0:
            type.pname = "顶级分类"
        else:
        
            type.pname =Types.objects.get(id=type.pid).name


    return render(request,"myadmin/types/list.html",{"typeslist":typeslist})

# 添加分类
def add(request):

    if request.method == "GET":

        typeslist = gettypesorder(request)
        context = {"typeslist":typeslist}
        return render(request,"myadmin/types/add.html",context)

    elif request.method == "POST":
        type = Types()
        type.name = request.POST['name']
        type.pid = request.POST.get('pid',None)
        # path的获取
        if type.pid == '0':
            type.path = "0,"
        else:
            t = Types.objects.get(id = type.pid )
            type.path = t.path+str(type.pid)+','

        type.save()

        return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_types_list')+'"</script>')

# 删除
def delete(request):

    tid = request.GET['tid']
    # 判断当前类下是否子类
    num =  Types.objects.filter(pid=tid).count()

    if num > 0 :
        data = {'msg':'当前类下有子类,不能删除','type':1}
    else:
        type = Types.objects.get(id= tid)
        type.delete()
        data = {'msg':'删除成功','type':0}   

    return JsonResponse(data)

# 修改
def edit(request):
    # 获取id 和分类
    id = request.GET.get('uid',None)
    type = Types.objects.get(id = id)
    
    if request.method == 'GET':
        if type.pid == 0:
            type.pname = "顶级分类"
        else:
            type.pname = Types.objects.get(id = type.pid).name
        return  render(request,"myadmin/types/edit.html",{"type":type})

    elif request.method == 'POST':
        try:
            type.name = request.POST['name']
            type.save()
            return HttpResponse("<script>alert('修改成功！');location.href='"+reverse("myadmin_types_list") +"'</script>")
         
        except:
            return HttpResponse("<script>alert('修改失败！');location.href='"+reverse("myadmin_types_edit")+"?uid="+str(type.id) +"'</script>")
            