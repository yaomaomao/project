from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from .. models import Types
from django.contrib.auth.decorators import permission_required
# Create your views here.
def gettypesorder():
    # 获取所有的分类信息
    # tlist = Types.objects.all()

    # select *,concat(path,id) as paths from myadmin_types order by paths;
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



@permission_required('myadmin.insert_types',raise_exception = True)
def add(request):
    if request.method == 'GET':
        # 返回一个添加的页面

        tlist = gettypesorder()

        context = {'tlist':tlist}

        return render(request,'myadmin/types/add.html',context)

    elif request.method == 'POST':
        # 执行分类的添加
        ob = Types()
        ob.name = request.POST['name']
        ob.pid = request.POST['pid']
        if ob.pid == '0':
            ob.path = '0,'
        else:
            # 根据当前父级id获取path,在添加当前父级id
            t = Types.objects.get(id=ob.pid)
            ob.path = t.path+str(ob.pid)+','
        ob.save()
        return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_types_list')+'"</script>')


        
@permission_required('myadmin.show_types',raise_exception = True)
def index(request):

    tlist = gettypesorder()
     # 导入分页类
    from django.core.paginator import Paginator
    # 实例化分页对象,参数1,数据集合,参数2 每页显示条数
    paginator = Paginator(tlist, 10)
    # 获取当前页码数
    p = request.GET.get('p',1)
    # 获取当前页的数据
    tlist = paginator.page(p)

    context = {'tlist':tlist}

    return render(request,'myadmin/types/list.html',context)


@permission_required('myadmin.del_types',raise_exception = True)
def delete(request):

    tid = request.GET.get('uid',None)

    # 判断当前类下是否子类
    num = Types.objects.filter(pid=tid).count()

    if num != 0:
         data = {'msg':'当前类下有子类,不能删除','code':1}
    else:
        # 判断当前类下是否商品,
        ob = Types.objects.get(id=tid)
        ob.delete()

        data = {'msg':'删除成功','code':0}



    return JsonResponse(data)







@permission_required('myadmin.edit_types',raise_exception = True)
def edit(request):

    # 获取id 和分类
    id = int(request.GET.get('uid',None))
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