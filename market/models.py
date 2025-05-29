from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)


class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)


class Stock(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    total_shares = models.PositiveIntegerField(default=1000000)
    available_shares = models.PositiveIntegerField(default=1000000)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Trade(models.Model):
    seller = models.ForeignKey(Company, related_name='sales', on_delete=models.CASCADE)
    buyer = models.ForeignKey(Company, related_name='purchases', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


class StockTransaction(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Company, related_name='stock_buys', on_delete=models.CASCADE)
    seller = models.ForeignKey(Company, related_name='stock_sells', on_delete=models.CASCADE, null=True, blank=True)
    shares = models.PositiveIntegerField()
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
