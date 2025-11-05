from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('portfolios/', views.portfolios, name='portfolios'),
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    path('portfolio/<int:portfolio_id>/add-card/', views.add_card_to_portfolio, name='add_card_to_portfolio'),
    path('portfolio/<int:portfolio_id>/delete-card/', views.delete_card_from_portfolio, name='delete_card_from_portfolio'),
    path('api/search-cards/', views.search_cards, name='search_cards'),  
    ]