from allauth.account.forms import LoginForm
from django import forms
from django.utils.translation import gettext_lazy as _


class CustomLoginForm(LoginForm):
    remember = forms.BooleanField(label=_("Remember Me"), required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['remember'].initial = True  # changed initial from False to True
