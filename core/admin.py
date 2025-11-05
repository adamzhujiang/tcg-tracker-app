from django.contrib import admin
from .models import Card, Portfolio, PortfolioEntry, PricePoint

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("name", "set_name", "game", "price_at_addition", "volatility", "last_updated")
    search_fields = ("name", "set_name", "game")
    list_filter = ("game",)

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    search_fields = ("name", "user__username")
    list_filter = ("created_at",)

@admin.register(PortfolioEntry)
class PortfolioEntryAdmin(admin.ModelAdmin):
    list_display = ("portfolio", "card", "quantity", "purchase_price")
    search_fields = ("portfolio__name", "card__name")
    list_filter = ("portfolio",)

@admin.register(PricePoint)
class PricePointAdmin(admin.ModelAdmin):
    list_display = ("card", "date", "price")
    search_fields = ("card__name",)
    list_filter = ("date",)