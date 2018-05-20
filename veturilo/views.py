from django.views.generic import TemplateView
from scraper.models import Location


class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['locations'] = Location.objects.select_related()
        return context
