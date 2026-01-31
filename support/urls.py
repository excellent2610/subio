from django.urls import path
from . import views

app_name = "support"

urlpatterns = [
    path("", views.support_page, name="page"),
    path("activate/", views.become_supporter, name="activate"),
]
