from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import DetailView

from app_accounts.models import CustomUser
from app_base.nav_menu import menu1


class UserDashboardView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'app_dashboard/dashboard_progress.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated:
            raise Http404
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['menu'] = menu1
        return context
