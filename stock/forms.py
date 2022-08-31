from django import forms
from .models import Stock


class EditForm(forms.ModelForm):
    class Meta:  # 此处 Meta 没有提示
        model = Stock  # model 没有提示
        fields = '__all__'  # 整行没有提示

    def __init__(self, *args, **kwargs):  # 只有不正确 的提示
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['supplier'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity_unit'].widget.attrs.update({'class': 'form-control'})
        self.fields['unit_in_stock'].widget.attrs.update({'class': 'form-control'})
        self.fields['price_in_stock'].widget.attrs.update({'class': 'form-control'})
        self.fields['unit_on_order'].widget.attrs.update({'class': 'form-control'})
        self.fields['time_in_stock'].widget.attrs.update({'class': 'form-control'})
