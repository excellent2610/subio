from django.urls import path
from . import views

app_name = 'dashboard'  # важливо для namespace

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('ajax/', views.dashboard_ajax, name='dashboard_ajax'),
    path("", views.dashboard_view, name="index"),
]
