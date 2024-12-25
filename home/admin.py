from django.contrib import admin

from .models import Country, City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("title", "country_title", "population_mln", "image_preview")

    def country_title(self, instance):
        return instance.country.title
    country_title.short_description = "Страна"

    def get_queryset(self, request):
        return self.model.objects.select_related("country")


class CityInline(admin.TabularInline):
    model = City
    extra = 0


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    inlines = [CityInline]
