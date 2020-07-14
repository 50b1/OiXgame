from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

from .views import home, nowe_zaproszenie, akceptuj_zaproszenie

urlpatterns = [
    url(r'home$', home, name='player_home'),
    url(r'login$', LoginView.as_view(template_name='player/login_form.html'), name='player_login'),
    url(r'logout$', LogoutView.as_view(), name='player_logout'),
    url(r'nowe_zaproszenie$', nowe_zaproszenie, name='player_nowe_zaproszenie'),
    url(r'akceptuj_zaproszenie/(?P<id>\d+)$', akceptuj_zaproszenie, name='player_akceptuj_zaproszenie')
]