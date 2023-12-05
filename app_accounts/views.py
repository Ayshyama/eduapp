from django.shortcuts import render
from allauth.account.views import LoginView, SignupView


class UserLoginView(LoginView):
    template_name = 'account/login_signup.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_login'] = True
        context['form_login'] = context.pop('form')
        context['form_signup'] = SignupView.form_class()
        return context


class UserSignupView(SignupView):
    template_name = 'account/login_signup.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_login'] = False
        context['form_login'] = LoginView.form_class()
        context['form_signup'] = context.pop('form')
        return context

