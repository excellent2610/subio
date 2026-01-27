from django.urls import path
from . import views
from .views import update_username
from .views import delete_account
from .views import register_view

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path('update-username/', update_username, name='update_username'),
    path("logout/confirm/", views.logout_confirm_view, name="logout_confirm"),
    path("delete/confirm/", views.delete_account_confirm_view, name="delete_account_confirm"),
    path("delete/", views.delete_account_view, name="delete_account"),
]
