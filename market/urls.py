from django.urls import path
from .views import CompanyListView

urlpatterns = [
    path('companies/', CompanyListView.as_view(), name='companies'),
]