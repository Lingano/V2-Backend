from django.urls import path
from .views import CurrentTimeAPI, HelloWorldAPI

urlpatterns = [
    path('hello/', HelloWorldAPI.as_view(), name='hello_api'),
    path('current-time/', CurrentTimeAPI.as_view(), name='current_time_api'),
]