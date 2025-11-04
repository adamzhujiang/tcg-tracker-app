from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Portfolio


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "core/login.html")


@login_required
def home(request):
    portfolios = Portfolio.objects.filter(user=request.user)
    return render(request, "core/home.html", {"portfolios": portfolios})

@login_required
def portfolios(request):
    user_portfolios = Portfolio.objects.filter(user=request.user)
    return render(request, "core/portfolios.html", {"portfolios": user_portfolios})

@login_required
def portfolio_detail(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk, user=request.user)
    return render(request, "core/portfolio_detail.html", {"portfolio": portfolio})


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        if password != password_confirm:
            messages.error(request, "Passwords do not match")
            return render(request, "core/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, "core/register.html")

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")

    return render(request, "core/register.html")