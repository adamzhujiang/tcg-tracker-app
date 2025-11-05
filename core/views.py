from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from django.conf import settings
import requests
import json
from .models import Portfolio, PortfolioEntry, Card
from django.views.decorators.csrf import csrf_exempt


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
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
def add_portfolio(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Portfolio.objects.create(name=name, user=request.user)
            messages.success(request, "Portfolio added successfully!")
            return redirect("portfolios")
        else:
            messages.error(request, "Portfolio name cannot be empty.")
    return render(request, "core/add_portfolio.html")


@login_required
def portfolio_detail(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk, user=request.user)
    entries = PortfolioEntry.objects.filter(portfolio=portfolio)
    context = {
        "portfolio": portfolio,
        "entries": entries,
        "JUSTTCG_API_KEY": settings.JUSTTCG_API_KEY,
    }
    return render(request, "core/portfolio_detail.html", context)


@login_required
@require_POST
def add_card_to_portfolio(request, portfolio_id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON."})

    tcg_id = data.get("card_id")
    name = data.get("name")
    set_name = data.get("set_name")
    game = data.get("game")
    last_price = data.get("last_price", 0)
    quantity = data.get("quantity", 1)

    if not tcg_id or not name:
        return JsonResponse({"success": False, "error": "Card ID and name are required."})

    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1

    portfolio = get_object_or_404(Portfolio, pk=portfolio_id, user=request.user)

    card, created = Card.objects.get_or_create(
        tcg_id=tcg_id,
        defaults={
            "name": name,
            "set_name": set_name,
            "game": game,
            "last_price": last_price,
        }
    )

    if not created:
        card.last_price = last_price
        card.save()

    entry, created = PortfolioEntry.objects.get_or_create(
        portfolio=portfolio,
        card=card,
        defaults={"quantity": quantity}
    )

    if not created:
        entry.quantity += quantity
        entry.save()

    return JsonResponse({"success": True, "card_name": card.name, "quantity": entry.quantity, "last_price": card.last_price})

@login_required
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


@login_required
@require_GET
def search_cards(request):
    query = request.GET.get("q", "")
    game = request.GET.get("game", "")

    if not query:
        return JsonResponse([], safe=False)

    params = {
        "q": query,
        "api_key": settings.JUSTTCG_API_KEY, 
    }
    if game:
        params["game"] = game

    try:
        response = requests.get("https://api.justtcg.com/v1/cards", params=params)
        response.raise_for_status()
        data = response.json()
        cards = data.get("data", [])
        return JsonResponse(cards, safe=False)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def delete_card_from_portfolio(request, portfolio_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            card_tcg_id = data.get("card_id")
            if not card_tcg_id:
                return JsonResponse({"success": False, "error": "Card ID is required."})

            portfolio = Portfolio.objects.get(id=portfolio_id)

            entry = portfolio.entries.filter(card__tcg_id=card_tcg_id).first()
            if entry:
                entry.delete()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Card not found in portfolio."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method."})