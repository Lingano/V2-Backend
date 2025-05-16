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
    COMPANY_CHOICES = [(i, f'Company {i}') for i in range(1, 51)]
    company = models.IntegerField(choices=COMPANY_CHOICES)
    price = models.DecimalField(max_digits=5, decimal_places=2)
