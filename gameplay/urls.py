from django.conf.urls import url
#from django.contrib.auth.views import LoginView, LogoutView

from .views import game_detail, zrob_move

urlpatterns = [
    url(r'detale/(?P<id>\d+)/$', game_detail, name='gameplay_detale'),
    url(r'zrob_ruch/(?P<id>\d+)/$', zrob_move, name='gameplay_zrob_move')
]