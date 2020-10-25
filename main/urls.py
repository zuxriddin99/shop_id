from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('', views.cart_detail, name='cart_detail'),

]
