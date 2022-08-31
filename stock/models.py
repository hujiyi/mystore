from django.db import models
from product.models import Product
from supplier.models import Supplier
from datetime import datetime


class Stock(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING,
        verbose_name='商品')
    supplier = models.ForeignKey(
        Supplier, on_delete=models.DO_NOTHING,
        verbose_name='供应商')
    quantity_unit = models.CharField(
        max_length=20, blank=True,
        default='千克', verbose_name='数量单位')
    unit_in_stock = models.IntegerField(blank=True, default=0, verbose_name="入库数量")
    price_in_stock = models.DecimalField(
        decimal_places=2, max_digits=10,
        blank=True, default=0.0, verbose_name='入库单价')
    unit_on_order = models.IntegerField(blank=True, default=0, verbose_name="已售数量")
    time_in_stock = models.DateTimeField(blank=True, default=datetime.now)

    class Meta:  # 此处 Meta 没有提示
        verbose_name = '库存'  # 此处的 verbose_name  没有提示
        verbose_name_plural = verbose_name  # verbose_name_plural 没有提示

    def __str__(self):
        return f'{self.supplier} - {self.product}'
