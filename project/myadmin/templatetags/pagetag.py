from django import template
from django.utils.html import format_html

register = template.Library()
# 自定义页面优化标签
@register.simple_tag
def PageShow(count,request):
    # 获取当前页
    page = int(request.GET.get('p',1))

    begin = page-4
    end = page+5

    if page < 5:
        begin = 1
        end = 10

    if page > count-5:

        begin = count-9
        end = count

    if begin <= 0:
        begin = 1

    # u =''

    # for v in request.GET:

    s = ''
    s += '<li><a href="?p=1">首页</a></li>'
    if page - 1 <= 0:
        s += '<li class="am-disabled"><a href="?p=1">上一页</a></li>'
    else:
        s += '<li><a href="?p='+str(page-1)+'">上一页</a></li>'

    for x in range(begin,end+1):
        # 判断是否为当前页
        if page == x:
            s += '<li class="am-active"><a href="?p='+str(x)+'">'+str(x)+'</a></li>'
        else:
            s += '<li><a href="?p='+str(x)+'">'+str(x)+'</a></li>'


    if page+1 >= count:
        s += '<li class="am-disabled"><a href="?p='+str(count)+'">下一页</a></li>'
    else:
        s += '<li><a href="?p='+str(page+1)+'">下一页</a></li>'

    s += '<li><a href="?p='+str(count)+'">尾页</a></li>'



    return format_html(s)