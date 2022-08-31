from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreateForm


def create_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            login(request, user)
            return HttpResponseRedirect('/')

        error_msg = '注册新用户失败'
        return render(request, 'users/signup.html', locals())

    form = UserCreateForm()
    return render(request, 'users/signup.html', locals())


# login 是 django.contrib.auth 定义好的函数，不能使用
def user_login(request):
    if request.method == 'POST':
        # 登录界面不使用表单类(如果使用表单还要同时多建一个Model)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')

        error_msg = '用户名或密码错误'

    return render(request, 'users/login.html', locals())


# 函数名不能与 导入的 logout同名, 所以命名为log_out
def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')
