from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path("users/", include(("users.urls", "users"), namespace="users")),
    path("subscriptions/", include(("subscriptions.urls", "subscriptions"), namespace="subscriptions")),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
    path('notifications/', include('notifications.urls')),
    path('users/', include('users.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('notifications/', include('notifications.urls')),
    path(
        'favicon.ico',
        RedirectView.as_view(
            url='/static/images/favicon.ico',
            permanent=True
        )
    ),
    path("admin/", admin.site.urls),
    path("", lambda request: redirect("users:login")),

]
