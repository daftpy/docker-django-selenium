from django.urls import include, path
from . import views

app_name = 'main'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('accounts/register/', views.registration, name='register')
]