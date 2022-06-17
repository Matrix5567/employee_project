from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['address'].required = True
        self.fields['phone'].required = True

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        exclude = ('username',)
        fields = ('first_name', 'last_name', 'email', 'phone', 'address')
