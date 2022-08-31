from django.db import models
from product.models import Product
from customer.models import Customer
from stock.models import Stock
from datetime import datetime


class Order(models.Model):
    stock = models.ForeignKey(
        Stock, on_delete=models.DO_NOTHING, verbose_name="商品")
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, verbose_name="客户")
    quantity = models.IntegerField(blank=True, default=0, verbose_name="数量")
    quantity_unit = models.CharField(
        max_length=20, blank=True, default='千克', verbose_name='数量单位')
    price = models.DecimalField(
        decimal_places=2, max_digits=10,
        blank=True, default=0.0, verbose_name='单价')
    total_price = models.DecimalField(
        decimal_places=2, max_digits=10,
        blank=True, default=0.0, verbose_name='总价')
    time_on_order = models.DateTimeField(blank=True, default=datetime.now)

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.stock
