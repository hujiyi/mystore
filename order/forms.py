from django import forms
from .models import Order
from stock.models import Stock


class EditForm(forms.ModelForm):
    # stock = forms.ModelChoiceField(
    #     label='商品',
    #     required=True,
    #     queryset=Stock.objects.all(),
    #     widget=forms.Select(attrs={'class': 'form-control'})
    # )

    class Meta:  # 此处 Meta 没有提示
        model = Order  # model 没有提示
        fields = '__all__'  # 整行没有提示

    def __init__(self, *args, **kwargs):  # 只有不正确 的提示
        super().__init__(*args, **kwargs)
        self.fields['stock'].widget.attrs.update({'class': 'form-control'})
        self.fields['customer'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity_unit'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['total_price'].widget.attrs.update({'class': 'form-control'})
        self.fields['time_on_order'].widget.attrs.update({'class': 'form-control'})
