from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Card(models.Model):
    tcg_id = models.CharField(max_length=100, unique=True)  
    name = models.CharField(max_length=255)
    set_name = models.CharField(max_length=255, blank=True, null=True)
    game = models.CharField(max_length=50, db_index=True)
    price_at_addition = models.FloatField(default=0)  
    volatility = models.FloatField(default=0.0)   
    last_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.set_name})"


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="portfolios")
    name = models.CharField(max_length=200, default="My Portfolio")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class PortfolioEntry(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="entries")
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ("portfolio", "card")

    def total_value(self):
        if self.card.last_price:
            return self.quantity * self.card.last_price
        return None


class PricePoint(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="price_points")
    date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)