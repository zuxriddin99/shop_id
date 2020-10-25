from django.urls import path
from .views import blog

app_name = 'blog'

urlpatterns = [
    path('blog/', blog, name='blog')
]