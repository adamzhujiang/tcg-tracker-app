import os
import django
import requests
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tcgsite.settings")
django.setup()

from core.models import Card, PricePoint

API_KEY = "tcg_99d32afb675849868a53ee46f1b92fa5"
BASE_URL = "https://api.justtcg.com/v1/cards"


def fetch_cards(game="One Piece Card Game", page=1, page_size=10):
    """Fetch card data from JustTCG API for a specific game."""
    headers = {"x-api-key": API_KEY}
    params = {
        "game": game,
        "page": page,
        "pageSize": page_size,
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def update_cards_from_api(game="One Piece Card Game"):
    """Sync cards from JustTCG API into our database."""
    print(f"Fetching {game} cards...")
    data = fetch_cards(game=game)

    for item in data.get("data", []):
        tcg_id = item["id"]
        name = item.get("name", "Unknown")

        set_info = item.get("set")
        set_name = set_info.get("name") if isinstance(set_info, dict) else set_info

        last_price = item.get("prices", {}).get("market", 0.0)
        last_updated = datetime.now()

        card, created = Card.objects.update_or_create(
            tcg_id=tcg_id,
            defaults={
                "name": name,
                "set_name": set_name,
                "game": game,
                "last_price": last_price,
                "last_updated": last_updated,
            },
        )

        PricePoint.objects.create(card=card, price=last_price)
        print(f"✅ {'Created' if created else 'Updated'}: {name} (${last_price})")

    print("Done syncing cards!")


def run():
    """Entry point for `python manage.py runscript fetch_cards`"""
    update_cards_from_api("One Piece Card Game")