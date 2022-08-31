from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import ExtractMonth
from django.db.models import Count, Sum
from pyecharts import options as opts
from pyecharts.charts import Page, Bar, Pie
from .models import Order
from stock.models import Stock
from .forms import EditForm


def index(request):
    page = request.GET.get('page')  # 当前页码, 缺少时为第1页
    results = Order.objects.all()
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
    return render(request, 'order/index.html', locals())  # 模板文件路径没有提示, 不检查路径


def create(request):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            stock = cd['stock']  # 当前选中的库存商品
            quantity = cd['quantity']  # 当前订购的数量

            # 剩余商品数量
            remaining = stock.unit_in_stock - stock.unit_on_order
            # 如果库存剩余商品数量 大于等于 订购数量
            if remaining >= quantity:
                order = form.save()
                # 忽略输入界面中的总价, 使用 单价 * 数量 进行计算
                order.total_price = order.price * order.quantity
                order.save()  # 保存计算后总价
                # 修改库存商品的已购数量
                stock.unit_on_order += order.quantity
                stock.save()  # 保存修改后库存信息
                return redirect(index)

            error_msg = f'库存数量不足, 还剩 {remaining} {stock.quantity_unit}'
            return render(request, 'order/edit.html', locals())

        error_msg = '添加数据出错，请检查输入的数据格式'
        return render(request, 'order/edit.html', locals())

    form = EditForm()
    return render(request, 'order/edit.html', locals())


def update(request, id):
    data = get_object_or_404(Order, pk=id)
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # 查找修改前的订单
            old_order = get_object_or_404(Order, pk=id)
            stock = cd['stock']
            data.stock = stock
            data.customer = cd['customer']
            data.quantity = cd['quantity']
            data.quantity_unit = cd['quantity_unit']
            data.price = cd['price']
            data.total_price = cd['total_price']
            data.time_on_order = cd['time_on_order']
            # 如果修改了订单中商品数量, 同时修改 库存中的已售数量
            stock.unit_on_order += (data.quantity - old_order.quantity)
            # 当修改商品订单数量时, 有足够的剩余才保存, 否则不保存(保存就是实现修改)
            if stock.unit_in_stock - stock.unit_on_order >= 0:
                data.save()
                stock.save()  # 保存
                return redirect(index)

            error_msg = '商品库存数量不足'
            return render(request, 'order/edit.html', locals())

        error_msg = '修改数据出错，请检查输入的数据格式'
        return render(request, 'order/edit.html', locals())

    form = EditForm(initial={
        'stock': data.stock,
        'customer': data.customer,
        'quantity': data.quantity,
        'quantity_unit': data.quantity_unit,
        'price': data.price,
        'total_price': data.total_price,
        'time_on_order': data.time_on_order,
    })
    return render(request, 'order/edit.html', locals())


def delete(request, id):
    data = get_object_or_404(Order, pk=id)
    if request.method == 'POST':
        data.delete()
        return redirect(index)

    return render(request, 'order/delete.html', locals())


def detail(request, id):
    data = get_object_or_404(Order, pk=id)
    return render(request, 'order/detail.html', locals())


def report(request):
    # .values("customer__name")  第一个 .values(), 进行分组的字段, 相同的会合并进行汇总
    data_customer = Order.objects.values("customer__name").annotate(
        # .annotate() 汇总的项目
        month=ExtractMonth('time_on_order'),  # ExtractMonth 用于按月获取数据
        total=Sum("total_price")).values(
        #  最后的 .values(), 分类汇总结果输出的字段
        "customer__name", "total", "month")
    # 使用 HttpResponse 在浏览器检查汇总的结果
    # return HttpResponse(data)

    # Bar为柱状图
    bar = Bar(init_opts=opts.InitOpts(width='800px', height='400px'))
    # x轴显示信息
    bar.add_xaxis([f"{i['month']}月 - {i['customer__name']}" for i in data_customer])
    # 添加一个Y轴信息
    bar.add_yaxis('消费总金额: ', [i['total'] for i in data_customer])
    bar.render('templates/bar.html')  # 生成图表时html文件的路径从 templates 开始

    data_products = Order.objects.values("stock__product__name").annotate(
        # .annotate() 汇总的项目
        month=ExtractMonth('time_on_order'),
        total=Sum("total_price")).values(
        "stock__product__name", "total", "month")
    # return HttpResponse(data_products)

    # Pie 用于生成饼图
    pie_product = Pie(init_opts=opts.InitOpts(width='400px', height='250px'))
    # 饼图的颜色列表
    pie_product.set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
    # 设置标题
    pie_product.set_global_opts(
        title_opts=opts.TitleOpts(title="每月商品销售额比例"),
        # 设置图例位置
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="70%", orient="vertical"), )
    # 添加饼图数据
    pie_product.add(
        "",
        [list(z) for z in zip(
            [f"{i['month']}月 - {i['stock__product__name']}" for i in data_products],  # 文字
            [i['total'] for i in data_products])],  # 数值
        radius=["30%", "75%"],  # 可选项
        center=["35%", "50%"],  # 可选项
        rosetype="radius",  # 可选项
    )
    # 生成到第二个文件
    pie_product.render('templates/pie_product.html')  # 生成图表时html文件的路径从 templates 开始

    data_supplier = Order.objects.values("stock__supplier__name").annotate(
        # .annotate() 汇总的项目
        # month=ExtractMonth('time_on_order'),
        total=Sum("total_price")).values(
        "stock__supplier__name", "total", )

    pie_supplier = Pie(init_opts=opts.InitOpts(width='400px', height='250px'))
    pie_supplier.set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
    # 设置标题
    pie_supplier.set_global_opts(
        title_opts=opts.TitleOpts(title="每月按供应商销售金额比例"),
        # 设置图例位置
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="70%", orient="vertical"), )
    # # pie_product.set_series_opts()
    pie_supplier.add(
        "",
        [list(z) for z in zip(
            [i['stock__supplier__name'] for i in data_supplier],
            [i['total'] for i in data_supplier])],
        radius=["30%", "75%"],
        center=["35%", "50%"],
        rosetype="radius",
    )
    # 生成到第三个文件
    pie_supplier.render('templates/pie_supplier.html')

    # 在 'order/report.html' 引用 以上生成的三个文件
    return render(request, 'order/report.html', locals())
