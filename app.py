from flask import Flask, render_template, request, url_for, redirect, jsonify, Response, flash
import io
import csv
import json
from src.recommendation import RecommendationSystem
from src.preprocessing import load_items, load_users, load_preferences, add_item, add_user, add_preference
from src.history_manager import load_history, add_history

app = Flask(__name__)
app.secret_key = "ai_rec_system_secret_key"

def get_data():
    items = load_items("dataset/items.csv")
    users = load_users("dataset/users.csv")
    preferences = load_preferences("dataset/preferences.csv")
    recsys = RecommendationSystem(items)
    return items, users, preferences, recsys

@app.route("/", methods=["GET", "POST"])
def index():
    items, users, preferences, recsys = get_data()
    categories = sorted({item["category"] for item in items})
    topics = sorted({topic for item in items for topic in item["tags"]})
    
    selected_user = request.args.get("user_id", "")
    
    if request.method == "POST":
        selected_categories = request.form.getlist("category")
        selected_topics = request.form.getlist("topic")
        algorithm = request.form.get("algorithm", "cosine")
        top_n = int(request.form.get("top_n", 5))
        user_id = request.form.get("user_id", "Guest")
        
        user_profile = {
            "categories": selected_categories,
            "topics": selected_topics,
        }
        
        recommended = recsys.recommend(user_profile, algorithm=algorithm, top_n=top_n)
        
        # Log to history
        hist_entry = {
            "user_id": user_id,
            "selected_categories": selected_categories,
            "selected_topics": selected_topics,
            "algorithm": algorithm,
            "top_n": top_n,
            "results": [{"item_id": rec["item"]["id"], "title": rec["item"]["title"], "score": rec["score"]} for rec in recommended]
        }
        add_history("dataset/history.json", hist_entry)
        
        return render_template(
            "recommendations.html",
            recommendations=recommended,
            selected_categories=selected_categories,
            selected_topics=selected_topics,
            algorithm=algorithm,
            top_n=top_n,
            user_id=user_id,
            users=users
        )

    return render_template("index.html", categories=categories, topics=topics, users=users, selected_user=selected_user)

@app.route("/dashboard")
def dashboard():
    items, users, preferences, _ = get_data()
    history = load_history("dataset/history.json")
    return render_template("dashboard.html", items=items, users=users, preferences=preferences, history=history)

@app.route("/manager", methods=["GET", "POST"])
def manager():
    items, users, preferences, _ = get_data()
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "add_item":
            title = request.form.get("title", "").strip()
            category = request.form.get("category", "").strip()
            description = request.form.get("description", "").strip()
            tags_str = request.form.get("tags", "").strip()
            rating = request.form.get("rating", "0.0")
            
            if not title or not category:
                flash("Title and Category are required!", "danger")
                return redirect(url_for("manager"))
                
            tags = [t.strip() for t in tags_str.split(",") if t.strip()]
            new_id = str(max([int(item["id"]) for item in items]) + 1) if items else "1"
            
            item_data = {
                "id": new_id,
                "title": title,
                "category": category,
                "description": description,
                "tags": tags,
                "rating": float(rating) if rating else 0.0
            }
            add_item("dataset/items.csv", item_data)
            flash(f"Item '{title}' successfully added!", "success")
            
        elif action == "add_user":
            name = request.form.get("name", "").strip()
            fav_cat = request.form.get("favorite_category", "").strip()
            
            if not name:
                flash("User Name is required!", "danger")
                return redirect(url_for("manager"))
                
            new_id = str(max([int(user["id"]) for user in users]) + 1) if users else "1"
            user_data = {
                "id": new_id,
                "name": name,
                "favorite_category": fav_cat
            }
            add_user("dataset/users.csv", user_data)
            flash(f"User '{name}' successfully created!", "success")
            
        elif action == "add_preference":
            user_id = request.form.get("user_id")
            item_id = request.form.get("item_id")
            preference_val = request.form.get("preference", "like")
            
            if not user_id or not item_id:
                flash("User and Item must be selected!", "danger")
                return redirect(url_for("manager"))
                
            pref_data = {
                "user_id": user_id,
                "item_id": item_id,
                "preference": preference_val
            }
            add_preference("dataset/preferences.csv", pref_data)
            flash("Preference mapping successfully saved!", "success")
            
        return redirect(url_for("manager"))
        
    return render_template("manager.html", items=items, users=users, preferences=preferences)

@app.route("/api/user-profile/<user_id>")
def user_profile_api(user_id):
    items, users, preferences, _ = get_data()
    user_prefs = [p for p in preferences if str(p["user_id"]) == str(user_id)]
    liked_item_ids = [str(p["item_id"]) for p in user_prefs if p["preference"] == "like"]
    liked_items = [item for item in items if str(item["id"]) in liked_item_ids]
    
    categories = list({item["category"] for item in liked_items})
    tags = list({tag for item in liked_items for tag in item["tags"]})
    
    user_obj = next((u for u in users if str(u["id"]) == str(user_id)), None)
    fav_cat = user_obj["favorite_category"] if user_obj else ""
    if fav_cat and fav_cat not in categories:
        categories.append(fav_cat)
        
    return jsonify({
        "categories": categories,
        "tags": tags,
        "favorite_category": fav_cat
    })

@app.route("/api/preference", methods=["POST"])
def api_preference():
    user_id = request.form.get("user_id")
    item_id = request.form.get("item_id")
    preference_val = request.form.get("preference", "like")
    
    if not user_id or not item_id:
        return jsonify({"success": False, "error": "Missing parameters"}), 400
        
    pref_data = {
        "user_id": user_id,
        "item_id": item_id,
        "preference": preference_val
    }
    add_preference("dataset/preferences.csv", pref_data)
    return jsonify({"success": True})

@app.route("/api/analytics")
def api_analytics():
    items, users, preferences, _ = get_data()
    history = load_history("dataset/history.json")
    
    # 1. Category counts
    cat_counts = {}
    for item in items:
        cat = item["category"]
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        
    # 2. Preferences by category
    pref_cat_counts = {}
    liked_item_ids = [str(p["item_id"]) for p in preferences if p["preference"] == "like"]
    for item in items:
        if str(item["id"]) in liked_item_ids:
            cat = item["category"]
            pref_cat_counts[cat] = pref_cat_counts.get(cat, 0) + 1
            
    # 3. Average ratings by category
    cat_ratings = {}
    cat_total_ratings = {}
    for item in items:
        cat = item["category"]
        cat_ratings[cat] = cat_ratings.get(cat, 0.0) + item.get("rating", 0.0)
        cat_total_ratings[cat] = cat_total_ratings.get(cat, 0) + 1
        
    avg_ratings = {}
    for cat in cat_ratings:
        avg_ratings[cat] = round(cat_ratings[cat] / cat_total_ratings[cat], 2)
        
    # 4. Algorithm history counts
    algo_counts = {}
    for h in history:
        algo = h.get("algorithm", "cosine")
        algo_counts[algo] = algo_counts.get(algo, 0) + 1
        
    # 5. Top recommended items
    rec_item_counts = {}
    for h in history:
        for res in h.get("results", []):
            title = res.get("title", "")
            if title:
                rec_item_counts[title] = rec_item_counts.get(title, 0) + 1
                
    # Sort top items
    top_items = sorted(rec_item_counts.items(), key=lambda x: x[1], reverse=True)[:6]
    top_items_dict = {k: v for k, v in top_items}
    
    return jsonify({
        "category_counts": cat_counts,
        "preference_category_counts": pref_cat_counts,
        "average_ratings": avg_ratings,
        "algorithm_counts": algo_counts,
        "top_items": top_items_dict
    })

@app.route("/export")
def export():
    items, users, preferences, recsys = get_data()
    categories_str = request.args.get("categories", "")
    topics_str = request.args.get("topics", "")
    algorithm = request.args.get("algorithm", "cosine")
    top_n = int(request.args.get("top_n", 5))
    format_type = request.args.get("format", "json")
    
    selected_categories = [c.strip() for c in categories_str.split(",") if c.strip()]
    selected_topics = [t.strip() for t in topics_str.split(",") if t.strip()]
    
    user_profile = {
        "categories": selected_categories,
        "topics": selected_topics,
    }
    
    recommended = recsys.recommend(user_profile, algorithm=algorithm, top_n=top_n)
    
    if format_type == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Rank", "Item ID", "Title", "Category", "Rating", "Similarity Score", "Explanation"])
        for i, rec in enumerate(recommended, 1):
            writer.writerow([
                i,
                rec["item"]["id"],
                rec["item"]["title"],
                rec["item"]["category"],
                rec["item"]["rating"],
                rec["score"],
                rec["explanation"]
            ])
        csv_data = output.getvalue()
        output.close()
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=recommendations.csv"}
        )
    else:
        json_data = json.dumps([{
            "rank": i,
            "item_id": rec["item"]["id"],
            "title": rec["item"]["title"],
            "category": rec["item"]["category"],
            "rating": rec["item"]["rating"],
            "score": rec["score"],
            "explanation": rec["explanation"]
        } for i, rec in enumerate(recommended, 1)], indent=2)
        return Response(
            json_data,
            mimetype="application/json",
            headers={"Content-disposition": "attachment; filename=recommendations.json"}
        )

if __name__ == "__main__":
    app.run(debug=True)

