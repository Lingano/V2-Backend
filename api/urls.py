from django.urls import path
from .views import (
    CurrentTimeAPI,
    HelloWorldAPI,
    CompanyListCreateAPI,
    CompanyDetailAPI,
    CompanyStatsAPI,
    CompanySearchAPI,
)

urlpatterns = [
    path("hello/", HelloWorldAPI.as_view(), name="hello_api"),
    path("current-time/", CurrentTimeAPI.as_view(), name="current_time_api"),
    path("companies/", CompanyListCreateAPI.as_view(), name="company_list_create"),
    path("companies/<int:pk>/", CompanyDetailAPI.as_view(), name="company_detail"),
    path("companies/stats/", CompanyStatsAPI.as_view(), name="company_stats"),
    path("companies/search/", CompanySearchAPI.as_view(), name="company_search"),
]
