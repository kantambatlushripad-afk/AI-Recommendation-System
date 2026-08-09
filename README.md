# 🤖 AI Recommendation System — Preference Matching

> A production-ready **AI Recommendation System** built with Flask and Python that recommends items based on user preferences using multiple similarity algorithms, including **Cosine Similarity, Jaccard Similarity, Euclidean Similarity, Pearson Correlation, and TF-IDF Content-Based Filtering**.

The project combines an intelligent recommendation engine with a modern **glassmorphic web interface**, interactive analytics dashboards, dataset management, recommendation history, favorites, and export functionality.

---

## ✨ Features

### 🧠 Multiple AI Recommendation Algorithms

Choose between multiple recommendation techniques in real time:

* 🔵 **Cosine Similarity**
* 🟣 **Jaccard Similarity**
* 🟢 **Euclidean Distance Similarity**
* 🟠 **Pearson Correlation**
* 🔴 **TF-IDF Content-Based Filtering**

Each algorithm provides a different approach to measuring the relationship between user preferences and item characteristics.

---

### 👤 User Preference Matching

Users can select an existing profile and receive personalized recommendations based on their preferences.

The system can analyze:

* Favorite categories
* Item tags
* Previously liked items
* Ratings
* User-item preferences
* Content descriptions

The recommendation engine automatically builds a user preference profile from the stored dataset.

---

### 🎯 Personalized Recommendations

The system generates ranked recommendations based on the selected algorithm.

Each recommendation can display:

* ⭐ Item rating
* 📊 Match percentage
* 🏷️ Matching tags
* 📂 Category match
* 🧮 Similarity score
* 💡 Explanation of why the item was recommended

This makes the recommendation process more transparent and understandable.

---

### 📊 Interactive Analytics Dashboard

A dedicated dashboard provides visual insights into the recommendation system using **Chart.js**.

Dashboard visualizations include:

1. 🍩 Category Distribution
2. 📊 Top Recommended Items
3. 🕸️ Average Rating by Category
4. 📈 Popular Tags / Category Preferences
5. 🕒 Recent Recommendation History

The dashboard helps analyze both the dataset and recommendation behavior.

---

### 💾 Dataset Management

A built-in Data Manager allows administrators to manage the recommendation dataset directly from the web interface.

You can:

* ➕ Add new items
* 👤 Create new users
* ❤️ Add user preferences
* ⭐ Add or update ratings
* 🏷️ Manage item categories and tags

Changes are persisted directly to:

```text
dataset/
├── items.csv
├── users.csv
├── preferences.csv
└── history.json
```

---

### ❤️ Favorites & Real-Time Preferences

Users can favorite recommended items directly from the recommendation page.

The system sends the preference to the Flask backend and updates the dataset in real time.

This allows the recommendation system to continuously learn from user interactions.

---

### 🔍 Search & Filtering

The application includes live search functionality for:

* Items
* Users
* Categories
* Topics
* Tags

Search results are retrieved through the Flask API.

---

### 📥 Export Recommendations

Recommendation results can be exported in:

* 📄 CSV
* 📋 JSON

This makes it easy to save, analyze, or reuse recommendation results.

---

### 🕒 Recommendation History

Every recommendation session can be stored in:

```text
dataset/history.json
```

History records can contain:

* User profile
* Selected algorithm
* Recommended items
* Similarity scores
* Timestamp

This data is also used for analytics and recommendation statistics.

---

## 🎨 Modern UI/UX

The frontend is designed with a modern glassmorphic aesthetic.

### UI Features

* 🌙 Dark / Light mode
* 🪟 Glassmorphism panels
* ✨ Glowing borders
* 🎨 HSL-based theme variables
* 🖱️ Smooth hover effects
* 💫 Micro animations
* 📱 Responsive layout
* 🔎 Search and filtering
* 🎛️ Interactive algorithm selector
* 📊 Interactive charts
* ❤️ Favorite interactions
* 📥 Export controls

The interface is designed to feel like a modern AI-powered recommendation platform rather than a traditional Flask application.

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │      Web Browser        │
                    │  HTML / CSS / JavaScript│
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       Flask App         │
                    │       app.py            │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
      ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
      │ Recommendation│  │  Preprocessing │  │    History    │
      │    Engine     │  │    Module      │  │    Manager    │
      └───────┬───────┘  └───────┬───────┘  └───────┬───────┘
              │                  │                  │
              ▼                  ▼                  ▼
      ┌────────────────────────────────────────────────────┐
      │                    Dataset Layer                   │
      │                                                    │
      │ items.csv │ users.csv │ preferences.csv │ history │
      └────────────────────────────────────────────────────┘
```

---

# 🧠 Recommendation Pipeline

```text
User Selection
      │
      ▼
Load User Preferences
      │
      ▼
Build User Profile
      │
      ▼
Select Recommendation Algorithm
      │
      ├── Cosine Similarity
      ├── Jaccard Similarity
      ├── Euclidean Similarity
      ├── Pearson Correlation
      └── TF-IDF
      │
      ▼
Calculate Similarity Scores
      │
      ▼
Rank Items
      │
      ▼
Select Top-N Recommendations
      │
      ▼
Generate Explanations
      │
      ▼
Display Recommendations
```

---

# 📐 Similarity Algorithms

## 1. Cosine Similarity

Measures the cosine of the angle between two vectors.

```text
Similarity(A,B) =
       A · B
──────────────────
   ||A|| ||B||
```

Useful for comparing preference and feature vectors.

---

## 2. Jaccard Similarity

Measures the overlap between two sets.

```text
Jaccard(A,B) = |A ∩ B|
               ─────────
               |A ∪ B|
```

Useful for comparing:

* Tags
* Categories
* User preferences
* Item features

---

## 3. Euclidean Similarity

The system converts Euclidean distance into a similarity score:

```text
Similarity = 1 / (1 + Distance)
```

A smaller distance therefore produces a higher similarity score.

---

## 4. Pearson Correlation

Measures the correlation between two feature vectors.

```text
Pearson =
    Covariance(A,B)
──────────────────────
  Std(A) × Std(B)
```

This can identify relationships between preference patterns.

---

## 5. TF-IDF Content-Based Filtering

The TF-IDF recommender combines item information such as:

```text
Title
Category
Description
Tags
```

The combined text is converted into TF-IDF vectors using `scikit-learn`.

The user's preference profile is then compared with item vectors using cosine similarity.

---

# 📁 Project Structure

```text
AI-Recommendation-System/
│
├── app.py
│
├── src/
│   ├── similarity.py
│   ├── recommendation.py
│   ├── preprocessing.py
│   └── history_manager.py
│
├── dataset/
│   ├── items.csv
│   ├── users.csv
│   ├── preferences.csv
│   └── history.json
│
├── templates/
│   ├── index.html
│   ├── recommendations.html
│   ├── dashboard.html
│   └── manager.html
│
├── static/
│   ├── styles.css
│   ├── script.js
│   └── ...
│
├── scratch/
│   └── verify_recommendation.py
│
├── requirements.txt
│
└── README.md
```

---

# 🔌 API Endpoints

| Method     | Endpoint          | Description                   |
| ---------- | ----------------- | ----------------------------- |
| `GET`      | `/`               | Main recommendation interface |
| `GET`      | `/dashboard`      | Analytics dashboard           |
| `GET/POST` | `/manager`        | Dataset management            |
| `GET`      | `/api/analytics`  | Analytics data                |
| `GET`      | `/api/search`     | Search users/items            |
| `POST`     | `/api/preference` | Add/update preference         |
| `GET`      | `/export`         | Export recommendations        |

---

# 📊 Analytics API

The `/api/analytics` endpoint provides data for the frontend charts.

Example data categories include:

```text
Items by Category
Liked Item Frequency
Average Rating by Category
Most Recommended Items
Popular Tags
Recommendation History
```

Chart.js is then used to convert this data into interactive visualizations.

---

# 💾 Dataset Format

## Items

`dataset/items.csv`

Example:

```csv
id,title,category,tags,rating,description
1,Python Programming,Programming,"python,code,development",4.8,"Learn Python programming fundamentals"
2,Machine Learning,AI,"ml,ai,data",4.9,"Introduction to machine learning"
```

---

## Users

`dataset/users.csv`

Example:

```csv
id,name,favorite_category
1,Alice,Programming
2,Bob,AI
3,Charlie,Data Science
```

---

## Preferences

`dataset/preferences.csv`

Example:

```csv
user_id,item_id,rating
1,1,5
1,2,4
2,2,5
```

---

## Recommendation History

`dataset/history.json`

Example:

```json
[
  {
    "user_id": 1,
    "algorithm": "cosine",
    "recommendations": [
      {
        "item_id": 2,
        "score": 0.91
      }
    ],
    "timestamp": "2026-08-09T18:30:00"
  }
]
```

---

# 🛠️ Technologies Used

### Backend

* 🐍 Python
* 🌶️ Flask
* 🧠 scikit-learn
* 🧮 NumPy
* 🐼 Pandas

### Frontend

* HTML5
* CSS3
* JavaScript
* Chart.js

### Data Storage

* CSV
* JSON

### Machine Learning

* TF-IDF Vectorization
* Cosine Similarity
* Jaccard Similarity
* Euclidean Distance
* Pearson Correlation

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AI-Recommendation-System.git
```

Navigate into the project:

```bash
cd AI-Recommendation-System
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist, install the core dependencies:

```bash
pip install flask pandas numpy scikit-learn
```

---

# ▶️ Running the Application

Start the Flask server:

```bash
python app.py
```

The application should be available at:

```text
http://127.0.0.1:5000
```

Open the URL in your browser.

---

# 🧪 Testing

The project includes a verification script for testing the recommendation engine and dataset operations.

Run:

```bash
python scratch/verify_recommendation.py
```

The verification process checks:

* Dataset loading
* Similarity calculations
* Recommendation ranking
* Recommendation scores
* User creation
* Item creation
* Preference persistence

---

# 🧪 Manual Testing Checklist

After starting the application:

### Recommendation System

* [ ] Select an existing user
* [ ] Verify user preferences load
* [ ] Select Cosine Similarity
* [ ] Select Jaccard Similarity
* [ ] Select Euclidean Similarity
* [ ] Select Pearson Correlation
* [ ] Select TF-IDF
* [ ] Change Top-N value
* [ ] Search/filter recommendations
* [ ] View recommendation explanations

### Favorites

* [ ] Favorite an item
* [ ] Verify preference is stored
* [ ] Refresh the page
* [ ] Confirm the preference persists

### Dashboard

* [ ] Open `/dashboard`
* [ ] Verify category chart
* [ ] Verify recommendation chart
* [ ] Verify rating chart
* [ ] Verify popular tags/category chart
* [ ] Check recommendation history

### Data Manager

* [ ] Add a new item
* [ ] Create a new user
* [ ] Add a user preference
* [ ] Verify CSV files are updated
* [ ] Verify the new data appears in recommendations

### Export

* [ ] Export recommendations as CSV
* [ ] Export recommendations as JSON
* [ ] Verify downloaded data

---

# 🔐 Data Persistence

The system intentionally uses lightweight CSV/JSON storage so the project can be easily understood, demonstrated, and modified.

Data is persisted in:

```text
dataset/items.csv
dataset/users.csv
dataset/preferences.csv
dataset/history.json
```

> For a large-scale production deployment, the CSV/JSON layer can later be replaced with PostgreSQL, MySQL, MongoDB, or another production database.

---

# 🚀 Future Improvements

The system can be extended with:

* 🔐 User authentication
* 🗄️ PostgreSQL/MySQL database
* 🤝 Collaborative filtering
* 🧠 Hybrid recommendation models
* 🤖 Deep-learning recommendation models
* 🔄 Real-time model updates
* 📈 Advanced recommendation analytics
* 🧪 Automated unit and integration testing
* ⚡ Recommendation caching
* 🌐 REST API documentation
* 📱 Mobile-responsive PWA
* ☁️ Cloud deployment
* 👥 Multi-user sessions
* 🧬 Neural recommendation models
* 🎯 A/B testing for recommendation algorithms
* 🔔 Personalized notifications

---

# 📈 Performance & Scalability

The architecture separates the application into independent components:

```text
Frontend
   ↓
Flask API
   ↓
Recommendation Engine
   ↓
Similarity Engine
   ↓
Data Layer
```

This makes it easier to replace individual components without rewriting the entire application.

For example:

```text
CSV/JSON
   ↓
PostgreSQL
```

or:

```text
Traditional Similarity
   ↓
Hybrid ML Model
```

can be introduced without fundamentally changing the frontend.

---

# 🧩 Recommendation Explainability

One of the main goals of this project is to make recommendations understandable.

Instead of simply displaying:

```text
Recommendation Score: 91%
```

the application can explain:

```text
Why this item?

✓ Category matches your preference
✓ 3 tags match your interests
✓ High item rating
✓ Strong content similarity

Overall Match: 91%
```

This provides a more transparent recommendation experience.

---

# 🌟 Project Highlights

| Feature                | Status |
| ---------------------- | ------ |
| Cosine Similarity      | ✅      |
| Jaccard Similarity     | ✅      |
| Euclidean Similarity   | ✅      |
| Pearson Correlation    | ✅      |
| TF-IDF Recommendation  | ✅      |
| User Profiles          | ✅      |
| Preference Management  | ✅      |
| Favorites              | ✅      |
| Recommendation History | ✅      |
| Analytics Dashboard    | ✅      |
| Chart.js Visualization | ✅      |
| Search & Filtering     | ✅      |
| CSV Export             | ✅      |
| JSON Export            | ✅      |
| Dark / Light Mode      | ✅      |
| Glassmorphism UI       | ✅      |
| Dataset Manager        | ✅      |
| Automated Verification | ✅      |

---

# 🎓 Project Purpose

This project demonstrates how traditional similarity algorithms and content-based machine learning can be combined to build an intelligent recommendation platform.

It is particularly useful for learning:

* Recommendation systems
* Similarity metrics
* Content-based filtering
* Natural Language Processing
* TF-IDF
* Flask API development
* Data preprocessing
* Data visualization
* REST API design
* Frontend/backend integration
* Explainable AI concepts

---

# 👨‍💻 Author

**Shripad Kantambatlu**

B.E. — Artificial Intelligence & Machine Learning

---

# 📜 License

This project is intended for educational and development purposes.

You may modify and extend the project according to your requirements.

---

## ⭐ If You Like This Project

If this project helped you learn something or you found it useful:

⭐ **Star the repository**

🍴 **Fork the project**

🐛 **Report issues**

💡 **Suggest improvements**

🤝 **Contribute to the project**

---

> **Built with Python, Flask, Machine Learning, and a passion for intelligent recommendations. 🤖✨**
