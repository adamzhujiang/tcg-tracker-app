from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('portfolios/', views.portfolios, name='portfolios'),
    path('portfolio/add/', views.add_portfolio, name='add_portfolio'),  
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    path('portfolio/<int:portfolio_id>/add-card/', views.add_card_to_portfolio, name='add_card_to_portfolio'),
    path('portfolio/<int:portfolio_id>/delete-card/', views.delete_card_from_portfolio, name='delete_card_from_portfolio'),
    path('api/search-cards/', views.search_cards, name='search_cards'),
    path('portfolio/<int:pk>/delete/', views.delete_portfolio, name='delete_portfolio'),
    ]