from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from  ..models import Orders
from django.contrib.auth.decorators import permission_required


@permission_required('myadmin.show_order',raise_exception = True)
def index(request):
    
    orderlist = Orders.objects.all()
     # 获取搜索条件
    type = request.GET.get('type',None)
    kwords = request.GET.get('keywords',None)

    if type:

        if type == 'all':
            from django.db.models import Q
            orderlist = Orders.objects.filter(
                Q(title__contains=kwords)|
                Q(descr__contains=kwords)|
                Q(price__contains=kwords)|
                Q(store__contains=kwords)|
                Q(info__contains=kwords)   
            )
        elif type == "status":
            orderlist = Orders.objects.filter(status__contains=kwords)
       
    else:

        orderlist = Orders.objects.all()
    # 导入分页类
    from django.core.paginator import Paginator
    # 实例化分页对象,参数1,数据集合,参数2 每页显示条数
    paginator = Paginator(orderlist, 10)
    # 获取当前页码数
    p = request.GET.get('p',1)
    # 获取当前页的数据
    orderlist = paginator.page(p)

    return render(request,'myadmin/order/list.html',{"orderlist":orderlist})

def edit(request):
    
    if request.method == "GET":

        orderid = request.GET.get("orderid",None)
        order = Orders.objects.get(id = orderid)

        return render(request,"myadmin/order/edit.html",{"order":order})
    elif request.method == "POST":
        pass