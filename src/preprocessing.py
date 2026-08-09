import csv
import json
from typing import List, Dict


def load_items(path: str) -> List[Dict]:
    items = []
    with open(path, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tags = [tag.strip() for tag in row.get("tags", "").split(",") if tag.strip()]
            item = {
                "id": row.get("id", ""),
                "title": row.get("title", ""),
                "category": row.get("category", ""),
                "description": row.get("description", ""),
                "tags": tags,
                "rating": float(row.get("rating", "0")) if row.get("rating") else 0.0,
            }
            items.append(item)
    return items


def load_users(path: str) -> List[Dict]:
    users = []
    with open(path, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append({
                "id": row.get("id", ""),
                "name": row.get("name", ""),
                "favorite_category": row.get("favorite_category", ""),
            })
    return users


def load_preferences(path: str) -> List[Dict]:
    preferences = []
    try:
        with open(path, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                preferences.append({
                    "user_id": row.get("user_id", ""),
                    "item_id": row.get("item_id", ""),
                    "preference": row.get("preference", ""),
                })
    except FileNotFoundError:
        pass
    return preferences


def add_item(path: str, item: Dict) -> None:
    # Ensure items file has headers, write header if empty
    import os
    file_exists = os.path.exists(path) and os.path.getsize(path) > 0
    with open(path, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["id", "title", "category", "description", "tags", "rating"])
        writer.writerow([
            item["id"],
            item["title"],
            item["category"],
            item["description"],
            ",".join(item["tags"]),
            item["rating"]
        ])


def add_user(path: str, user: Dict) -> None:
    import os
    file_exists = os.path.exists(path) and os.path.getsize(path) > 0
    with open(path, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["id", "name", "favorite_category"])
        writer.writerow([
            user["id"],
            user["name"],
            user["favorite_category"]
        ])


def add_preference(path: str, pref: Dict) -> None:
    prefs = load_preferences(path)
    updated = False
    for p in prefs:
        if str(p["user_id"]) == str(pref["user_id"]) and str(p["item_id"]) == str(pref["item_id"]):
            p["preference"] = pref["preference"]
            updated = True
            break
    if not updated:
        prefs.append(pref)
        
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["user_id", "item_id", "preference"])
        writer.writeheader()
        writer.writerows(prefs)

