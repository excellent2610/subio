from django.urls import path
from . import views
from .views import plans
from .views import cancel_subscription

app_name = "subscriptions"

urlpatterns = [
    path("add/", views.add_subscription, name="add"),
    path("edit/<int:pk>/", views.subscription_edit, name="edit"),
    path("delete/<int:pk>/", views.subscription_delete, name="delete"),
    path('paid/<int:pk>/', views.mark_paid, name='mark_paid'),
    path('plans/', plans, name='plans'),
    path('cancel/', cancel_subscription, name='cancel_subscription'),

]
