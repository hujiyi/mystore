from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Supplier
from .forms import EditForm


def index(request):
    # data_list = Customer.objects.all()      # 从 objects 开始没有提示
    page = request.GET.get('page')  # 当前页码, 缺少时为第1页
    results = Supplier.objects.all()
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
    return render(request, 'supplier/index.html', locals())  # 模板文件路径没有提示, 不检查路径


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
        return render(request, 'supplier/edit.html', locals())

    form = EditForm()
    return render(request, 'supplier/edit.html', locals())


def update(request, id):
    data = get_object_or_404(Supplier, pk=id)
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            data.name = cd['name']
            data.phone = cd['phone']
            data.city = cd['city']
            data.address = cd['address']
            data.desc = cd['desc']
            data.save()
            return redirect(index)

        error_msg = '修改数据出错，请检查输入的数据格式'
        return render(request, 'supplier/edit.html', locals())

    form = EditForm(initial={
        'name': data.name,
        'phone': data.phone,
        'city': data.city,
        'address': data.address,
        'desc': data.desc,
    })
    return render(request, 'supplier/edit.html', locals())


def delete(request, id):
    data = get_object_or_404(Supplier, pk=id)
    if request.method == 'POST':
        data.delete()
        return redirect(index)

    return render(request, 'supplier/delete.html', locals())


def detail(request, id):
    data = get_object_or_404(Supplier, pk=id)
    return render(request, 'supplier/detail.html', locals())
