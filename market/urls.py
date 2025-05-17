from django.urls import path
from .views import CompanyListCreateView, ProductListCreateView, StockListCreateView, TradeListCreateView, StockTransactionListCreateView

urlpatterns = [
    path('companies/', CompanyListCreateView.as_view(), name='companies'),
    path('products/', ProductListCreateView.as_view(), name='products'),
    path('stocks/', StockListCreateView.as_view(), name='stocks'),
    path('trades/', TradeListCreateView.as_view(), name='trades'),
    path('stock-transactions/', StockTransactionListCreateView.as_view(), name='stock-transactions'),
]