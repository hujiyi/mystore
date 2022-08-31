from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Stock
from .forms import EditForm


def index(request):
    page = request.GET.get('page')  # 当前页码, 缺少时为第1页
    results = Stock.objects.all()
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
    return render(request, 'stock/index.html', locals())  # 模板文件路径没有提示, 不检查路径


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
        return render(request, 'stock/edit.html', locals())

    form = EditForm()
    return render(request, 'stock/edit.html', locals())


def update(request, id):
    data = get_object_or_404(Stock, pk=id)
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            data.product = cd['product']
            data.supplier = cd['supplier']
            data.quantity_unit = cd['quantity_unit']
            data.unit_in_stock = cd['unit_in_stock']
            data.price_in_stock = cd['price_in_stock']
            data.unit_on_order = cd['unit_on_order']
            data.time_in_stock = cd['time_in_stock']
            data.save()
            return redirect(index)

        error_msg = '修改数据出错，请检查输入的数据格式'
        return render(request, 'stock/edit.html', locals())

    form = EditForm(initial={
        'product': data.product,
        'supplier': data.supplier,
        'quantity_unit':data.quantity_unit,
        'unit_in_stock': data.unit_in_stock,
        'price_in_stock': data.price_in_stock,
        'unit_on_order': data.unit_on_order,
    })
    return render(request, 'stock/edit.html', locals())


def delete(request, id):
    data = get_object_or_404(Stock, pk=id)
    if request.method == 'POST':
        data.delete()
        return redirect(index)

    return render(request, 'stock/delete.html', locals())


def detail(request, id):
    data = get_object_or_404(Stock, pk=id)
    return render(request, 'stock/detail.html', locals())
