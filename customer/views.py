from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Customer
from .forms import EditForm


def index(request):
    # 1. 没有分页时，直接返回结果到 data_list 变量
    # data_list = Customer.objects.all()

    # 接收搜索框输入的关键字 'kw' 为html 中 input 标签 name 属性的值
    kw = request.GET.get('kw')
    if kw:
        kw = kw.strip()  # 去前后空格
        # 2. 有搜索没有分页时，接收查询结果的变量名应该改为 data_list
        # name__contains: __ 左边的 name 为Customer中的字段名; __ 右边的contains 为包含;
        results = Customer.objects.filter(name__contains=kw)
    else:
        # 3. 使用分页功能时, 查询结果先保存到results, 当前页再通过data_list返回到模板
        results = Customer.objects.all()

    page = request.GET.get('page')  # 当前页码, 缺少时为第1页
    paginator = Paginator(results, 10)
    try:
        current_page = paginator.page(page)
        data_list = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        data_list = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        data_list = current_page.object_list
    return render(request, 'customer/index.html', locals())  # 模板文件路径没有提示, 不检查路径


def create(request):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            # cd = form.cleaned_data
            # Customer.objects.create(
            #     name=cd['name'],
            #     phone=cd['phone'],
            #     address=cd['address'],
            # )
            form.save()
            return redirect(index)

        error_msg = '添加数据出错，请检查输入的数据格式'
        return render(request, 'customer/edit.html', locals())

    form = EditForm()
    return render(request, 'customer/edit.html', locals())


def update(request, id):
    data = get_object_or_404(Customer, pk=id)
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            data.name = cd['name']
            data.phone = cd['phone']
            data.address = cd['address']
            data.save()
            return redirect(index)

        error_msg = '修改数据出错，请检查输入的数据格式'
        return render(request, 'customer/edit.html', locals())

    form = EditForm(initial={
        'name': data.name,
        'phone': data.phone,
        'address': data.address,
    })
    return render(request, 'customer/edit.html', locals())


def delete(request, id):
    data = get_object_or_404(Customer, pk=id)
    if request.method == 'POST':
        data.delete()
        return redirect(index)

    return render(request, 'customer/delete.html', locals())


def detail(request, id):
    data = get_object_or_404(Customer, pk=id)
    return render(request, 'customer/detail.html', locals())
