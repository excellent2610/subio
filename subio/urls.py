from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    # Головна сторінка тепер веде на dashboard
    path("", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
    
    # Інші додатки
    path("users/", include(("users.urls", "users"), namespace="users")),
    path("subscriptions/", include(("subscriptions.urls", "subscriptions"), namespace="subscriptions")),
    path('notifications/', include('notifications.urls')),
    
    # Адмінка та фавікон
    path("admin/", admin.site.urls),
    path(
        'favicon.ico',
        RedirectView.as_view(
            url='/static/images/favicon.ico',
            permanent=True
        )
    ),
]

# Додаємо обслуговування статичних файлів, якщо це розробка
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)