from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('login/', views.login_view, name='login'),  
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    path('register/', views.register_view, name='register'),
    path('portfolios/', views.portfolios, name='portfolios'),
]