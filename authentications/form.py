from django.forms import ModelForm, fields
from django.contrib.auth.forms import UserCreationForm
from django import forms
from authentications.models import MyUser


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-floating form-control', }))
    full_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-floating form-control'}))

    class Meta:
        model = MyUser
        fields = ['email', 'full_name',
                  'display_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-floating form-control'
        self.fields['display_name'].widget.attrs['class'] = 'form-floating form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-floating form-control'
