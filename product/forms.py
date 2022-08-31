from django import forms
from .models import Product


class EditForm(forms.ModelForm):
    class Meta:  # 此处 Meta 没有提示
        model = Product  # model 没有提示
        fields = '__all__'  # 整行没有提示

    def __init__(self, *args, **kwargs):  # 只有不正确 的提示
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['desc'].widget.attrs.update({'class': 'form-control'})
