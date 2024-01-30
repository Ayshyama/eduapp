from allauth.account.views import LoginView, SignupView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView
from app_accounts.models import CustomUser
from app_base.nav_menu import menu2
from app_accounts.Forms import CustomLoginForm


class UserLoginView(LoginView):
    template_name = 'account/login_signup.html'
    success_url = reverse_lazy('user_dashboard')

    def get_form_class(self):
        return CustomLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_login'] = True
        context['form_login'] = context.pop('form')
        context['form_signup'] = SignupView.form_class()
        return context


class UserSignupView(SignupView):
    template_name = 'account/login_signup.html'
    success_url = reverse_lazy('user_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_login'] = False
        context['form_signup'] = context.pop('form')
        context['form_login'] = LoginView.form_class()
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ('username', 'first_name', 'last_name', 'image', 'bio')
    template_name = 'app_accounts/profile.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_slug = self.request.user.username

        extra_context = {
            'title': 'User Profile',
            'menu': menu2,
            'menu_selected': 2,
            'user_slug': user_slug,
        }

        context.update(extra_context)

        return context

