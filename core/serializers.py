from rest_framework import serializers
from .models import Card, Portfolio, PortfolioEntry, PricePoint

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = "__all__"

class PortfolioEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioEntry
        fields = "__all__"

class PricePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePoint
        fields = "__all__"