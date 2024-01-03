from django.views.generic import TemplateView

from app_base.nav_menu import menu1


class LandingPageView(TemplateView):
    template_name = "app_base/landing_page.html"
    extra_context = {  # Need to pass these 3 context variables to each inherited from base.html template
        'title': 'EDU APP',
        'menu': menu1,
        'menu_selected': 0,
    }
