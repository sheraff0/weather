from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views.generic import TemplateView

from .models import City


class HomeView(TemplateView):
    template_name = "home.html"

    def get_cities(self):
        qs = City.objects.list_with_related()
        return [*qs]

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "cities": self.get_cities(),
        }


class CityView(LoginRequiredMixin, TemplateView):
    template_name = "city.html"
    login_url = "/auth/login/"

    def get_city(self):
        pk = self.kwargs.get("pk")
        return City.objects.item_with_related(pk)

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "city": self.get_city(),
        }
