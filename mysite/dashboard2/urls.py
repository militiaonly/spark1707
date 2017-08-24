from django.conf.urls import url
from . import views

app_name = 'dashboard2'
urlpatterns = [
    # ex: /dashboard2/
    url(r'^$', views.index, name='index'),
    url(r'^(?P<stock_code>[0-9]+)/$', views.detail, name='detail'),
    url(r'^stock-info-api$', views.stock_info_api, name='stock_info_api')
]
