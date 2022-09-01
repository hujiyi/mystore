# mystore

a Django store app

使用办法：

1. 创建一个名称 `mystore` 的 `MySQL` 数据库

2. 修改 `mystore/settings.py` 中数据库连接字符

3. 执行命令迁移数据库

```bash
python manage.py makemigrations
python manage.py migrate
```

4. 执行命令运行程序

```bash
python manage.py runserver
```

详细教程见 https://hujiyi.github.io

