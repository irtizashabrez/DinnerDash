from django.forms import ModelForm
from items.models import Item, Category
from django import forms


class ItemForm(ModelForm):
    title = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-floating form-control'}))
    description = forms.CharField(max_length=250, widget=forms.TextInput(
        attrs={'class': 'form-floating form-control'}))
    Category

    class Meta:
        model = Item
        fields = '__all__'


class CateoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
