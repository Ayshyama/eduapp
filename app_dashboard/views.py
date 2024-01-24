from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncDay
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView

from app_accounts.models import CustomUser, UserProgress
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

        user_progress = UserProgress.objects \
            .filter(user=self.request.user) \
            .annotate(date=TruncDay('datetime')) \
            .values('date') \
            .annotate(progress_count=Count('id')) \
            .order_by('date')

        progress_data = {progress['date'].strftime('%Y-%m-%d'): progress['progress_count'] for progress in user_progress}

        context['progress_data'] = progress_data

        return context



@login_required
def user_progress_json(request):
    user_progress = UserProgress.objects \
        .filter(user=request.user) \
        .annotate(date=TruncDay('datetime')) \
        .values('date') \
        .annotate(progress_count=Count('id')) \
        .order_by('date')

    progress_data = [
        {
            "date": progress['date'].strftime('%Y-%m-%d'),
            "details": [
                {
                    "name": "Exercises done: ",
                    "date": progress['date'],
                    "value": progress['progress_count']
                }
            ]
        }
        for progress in user_progress
    ]

    return JsonResponse(progress_data, safe=False)

