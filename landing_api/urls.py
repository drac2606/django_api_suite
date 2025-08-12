from django.urls import path
from . import views

app_name = 'landing_api'

urlpatterns = [
    path('index/', views.LandingAPI.as_view(), name='landing_api_index'),
]
