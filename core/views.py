from rest_framework import viewsets
from .models import Card, Portfolio, PortfolioEntry, PricePoint
from .serializers import CardSerializer, PortfolioSerializer, PortfolioEntrySerializer, PricePointSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

class PortfolioEntryViewSet(viewsets.ModelViewSet):
    queryset = PortfolioEntry.objects.all()
    serializer_class = PortfolioEntrySerializer

class PricePointViewSet(viewsets.ModelViewSet):
    queryset = PricePoint.objects.all()
    serializer_class = PricePointSerializer