from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product
from .forms import EditForm


def index(request):
    # data_list = Customer.objects.all()      # 从 objects 开始没有提示
    page = request.GET.get('page')  # 当前页码, 缺少时为第1页
    results = Product.objects.all()
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
    return render(request, 'product/index.html', locals())  # 模板文件路径没有提示, 不检查路径


def create(request):
    if request.method == 'POST':
        # request.FILES : 使用模型上传文件
        form = EditForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            # Product.objects.create(
            #     name=cd['name'],
            #     image=cd['image'],
            #     desc=cd['desc'],
            # )
            form.save()   # 添加数据时, 可以直接保存表单
            return redirect(index)

        error_msg = '添加数据出错，请检查输入的数据格式'
        return render(request, 'product/edit.html', locals())

    form = EditForm()
    return render(request, 'product/edit.html', locals())


def update(request, id):
    data = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            data.name = cd['name']
            # 有选择新图片时才进行保存，否则原有图片会被清空
            if request.FILES:
                data.image = cd['image']
            data.desc = cd['desc']
            data.save()
            return redirect(index)

        error_msg = '修改数据出错，请检查输入的数据格式'
        return render(request, 'product/edit.html', locals())

    form = EditForm(initial={
        'name': data.name,
        'image': data.image,
        'desc': data.desc,
    })
    return render(request, 'product/edit.html', locals())


def delete(request, id):
    data = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        data.delete()
        return redirect(index)

    return render(request, 'product/delete.html', locals())


def detail(request, id):
    data = get_object_or_404(Product, pk=id)
    return render(request, 'product/detail.html', locals())



