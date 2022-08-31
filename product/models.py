from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=60, verbose_name='名称')
    # 图片的类型可以先设置为 models.ImageField 需要配合 pillow 库使用; FileField 不需要
    image = models.FileField(
        upload_to='static/images/',  # 指定文件上传相对路径
        max_length=300, blank=True,
        null=True, verbose_name='图片')
    desc = models.CharField(
        max_length=200, blank=True,
        null=True, verbose_name='描述')

    class Meta:  # 此处 Meta 没有提示
        verbose_name = '商品'  # 此处的 verbose_name  没有提示
        verbose_name_plural = verbose_name  # verbose_name_plural 没有提示

    def __str__(self):
        return self.name
