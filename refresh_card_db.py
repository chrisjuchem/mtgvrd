#!/usr/bin/env python
import sys

import requests

from app.db.connection import ensure_session
from app.db.models import Card


def do_refresh():
    bulk_data = requests.get("https://api.scryfall.com/bulk-data").json()
    oracle_cards_uri = None
    for entry in bulk_data["data"]:
        if entry["type"] == "oracle_cards":
            oracle_cards_uri = entry["download_uri"]
            break

    if not oracle_cards_uri:
        print("No oracle cards uri")
        sys.exit(1)

    print("Downloading cards...")
    cards = requests.get(oracle_cards_uri).json()

    with ensure_session() as ses:
        existing_cards = {c.oracle_id: c for c in Card.query(ses)}
        for sf_card in cards:
            existing = existing_cards.get(sf_card["oracle_id"])
            if existing:
                existing.update_from_scryfall(sf_card)
            else:
                ses.add(Card.from_scryfall(sf_card))
        ses.commit()


if __name__ == "__main__":
    do_refresh()
