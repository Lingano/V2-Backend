from django.core.management.base import BaseCommand
from market.models import Company, Product, Stock, Trade, StockTransaction
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Simulate the market: company trades and stock transactions.'

    def handle(self, *args, **options):
        companies = list(Company.objects.all())
        products = list(Product.objects.all())
        stocks = list(Stock.objects.all())
        if not companies or not products or not stocks:
            self.stdout.write(self.style.WARNING('Not enough data to simulate.'))
            return

        # Simulate company-to-company trades
        for _ in range(10):  # Simulate 10 trades per run
            seller, buyer = random.sample(companies, 2)
            product = random.choice(products)
            quantity = random.randint(1, 100)
            price_per_unit = float(product.price) * random.uniform(0.95, 1.05)
            Trade.objects.create(
                seller=seller,
                buyer=buyer,
                product=product,
                quantity=quantity,
                price_per_unit=price_per_unit,
                timestamp=timezone.now()
            )

        # Simulate stock transactions
        for _ in range(5):  # Simulate 5 stock trades per run
            stock = random.choice(stocks)
            buyer, seller = random.sample(companies, 2)
            shares = random.randint(1, 1000)
            price_per_share = float(stock.price) * random.uniform(0.98, 1.02)
            if stock.available_shares >= shares:
                StockTransaction.objects.create(
                    stock=stock,
                    buyer=buyer,
                    seller=seller,
                    shares=shares,
                    price_per_share=price_per_share,
                    timestamp=timezone.now()
                )
                stock.available_shares -= shares
                stock.price = price_per_share  # Update price to last transaction
                stock.save()

        self.stdout.write(self.style.SUCCESS('Market simulation step completed.'))
