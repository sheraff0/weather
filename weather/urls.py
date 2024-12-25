from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from accounts.views import (
    LoginView, sign_up, verify_email,
    subscribe, unsubscribe,
)
from home.views import HomeView, CityView
from .sitemaps import HomeSitemap, CitySitemap

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path(r"cities/<int:pk>/", CityView.as_view(), name="city"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("auth/register/", sign_up, name="register"),
    path(r"auth/verify-email/<str:token>/", verify_email, name="verify_email"),
    path("accounts/subscribe", subscribe, name="subscribe"),
    path("accounts/unsubscribe", unsubscribe, name="unsubscribe"),
    path("sitemap.xml", sitemap, {"sitemaps": {
        "home": HomeSitemap(),
        "city": CitySitemap(),
    }}, name="django.contrib.sitemaps.views.sitemap",)
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
