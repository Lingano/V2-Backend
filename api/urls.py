from django.urls import path
from .views import (
    CurrentTimeAPI,
    HelloWorldAPI,
    CompanyListCreateAPI,
    CompanyDetailAPI,
    CompanyStatsAPI,
    CompanySearchAPI,
    CompanyScraperAPI,
    CompanyDataSourcesAPI,
)
from .database_views import (
    DatabaseBrowserView,
    DatabaseTablesAPI,
    DatabaseTableDataAPI,
    DatabaseQueryAPI,
)

urlpatterns = [
    path("hello/", HelloWorldAPI.as_view(), name="hello_api"),
    path("current-time/", CurrentTimeAPI.as_view(), name="current_time_api"),
    path("companies/", CompanyListCreateAPI.as_view(), name="company_list_create"),
    path("companies/<int:pk>/", CompanyDetailAPI.as_view(), name="company_detail"),
    path("companies/stats/", CompanyStatsAPI.as_view(), name="company_stats"),
    path("companies/search/", CompanySearchAPI.as_view(), name="company_search"),
    path("companies/scrape/", CompanyScraperAPI.as_view(), name="company_scraper"),
    path(
        "companies/data-sources/",
        CompanyDataSourcesAPI.as_view(),
        name="company_data_sources",
    ),
]
