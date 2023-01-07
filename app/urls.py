from app.views import *
from django.urls import path

urlpatterns = [
    path('get_euro_exchange_rates/', get_euro_exchange_rates, name="exchange_rate"),
]
