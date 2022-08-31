from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=60, verbose_name='客户')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='电话')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='地址')
    desc = models.CharField(max_length=200, blank=True, null=True, verbose_name='备注')

    class Meta:  # 此处 Meta 没有提示
        verbose_name = '客户'  # 此处的 verbose_name  没有提示
        verbose_name_plural = verbose_name  # verbose_name_plural 没有提示

    def __str__(self):
        return self.name
