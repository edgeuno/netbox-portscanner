from django.urls import path

from .views import (
    HomeView,
)

urlpatterns = [
    # Home View
    path('', HomeView.as_view(), name='home'),
]
