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
from django.contrib.auth import views as auth_views 



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
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        name = request.POST.get('name')
        set_name = request.POST.get('set_name')
        game = request.POST.get('game')
        last_price = request.POST.get('last_price') or 0
        quantity = request.POST.get('quantity') or 1

        if not card_id or not name:
            return JsonResponse({'success': False, 'error': 'Card ID and name are required.'})

        card, created = Card.objects.get_or_create(
            tcg_id=card_id,
            defaults={'name': name, 'set_name': set_name, 'game': game, 'last_price': last_price}
        )

        portfolio = Portfolio.objects.get(id=portfolio_id)
        entry, created = PortfolioEntry.objects.get_or_create(
            portfolio=portfolio,
            card=card,
            defaults={'quantity': quantity}
        )

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

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
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})

    try:
        data = json.loads(request.body)
        entry_id = data.get('entry_id')
        if not entry_id:
            return JsonResponse({'success': False, 'error': 'PortfolioEntry ID is required.'})

        entry = PortfolioEntry.objects.get(id=entry_id)
        entry.delete()
        return JsonResponse({'success': True})
    except PortfolioEntry.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Portfolio entry not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def delete_portfolio(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk, user=request.user)
    if request.method == "POST":
        portfolio.delete()
        return redirect('portfolios')
    return redirect('portfolios')