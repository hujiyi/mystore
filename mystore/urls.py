"""mystore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import users.views, order.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),  # include() 内的应用名和url 模块名没有提示
    path('supplier/', include('supplier.urls')),
    path('order/', include('order.urls')),
    path('stock/', include('stock.urls')),
    # 'product.urls' 第一次使用, 匹配127.0.0.1:8000/product,
    # 用于文件复制应用后 views 和 模板文件中的 路径匹配(不用考虑哪个应用缺少前缀)
    path('product/', include('product.urls')),

    # 'product.urls' 第二次使用,匹配 127.0.0.1:8000, 可以改为其他希望显示在首页的应用
    # path('', include('product.urls')),

    path('login/', users.views.user_login),
    path('signup/', users.views.create_user),
    path('logout/', users.views.log_out),
    # 首页显示报表图形
    path('', order.views.report),
]
