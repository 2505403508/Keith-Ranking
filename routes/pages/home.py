from flask import Blueprint, render_template, request

home_bp = Blueprint('home', __name__)

GAMES = [
    {
        "id": 1,
        "rank": 1,
        "name": "Elden Ring",
        "genre": "RPG",
        "score": 9.6,
        "price": 59,
        "discount": 15,
        "players": "1.2M",
        "tags": ["Soulslike", "Open World", "Action"],
        "accent": "linear-gradient(135deg, #7c3aed, #a855f7)"
    },
    {
        "id": 2,
        "rank": 2,
        "name": "Cyberpunk 2077",
        "genre": "RPG",
        "score": 9.2,
        "price": 39,
        "discount": 20,
        "players": "980K",
        "tags": ["Sci-fi", "Story", "Open World"],
        "accent": "linear-gradient(135deg, #2563eb, #06b6d4)"
    },
    {
        "id": 3,
        "rank": 3,
        "name": "Hades",
        "genre": "Action",
        "score": 9.0,
        "price": 25,
        "discount": 10,
        "players": "720K",
        "tags": ["Roguelike", "Indie", "Fast-paced"],
        "accent": "linear-gradient(135deg, #ef4444, #f97316)"
    },
    {
        "id": 4,
        "rank": 4,
        "name": "Stardew Valley",
        "genre": "Simulation",
        "score": 8.9,
        "price": 18,
        "discount": 0,
        "players": "1.5M",
        "tags": ["Cozy", "Farming", "Pixel Art"],
        "accent": "linear-gradient(135deg, #16a34a, #84cc16)"
    },
    {
        "id": 5,
        "rank": 5,
        "name": "Red Dead Redemption 2",
        "genre": "Action",
        "score": 8.8,
        "price": 49,
        "discount": 25,
        "players": "880K",
        "tags": ["Western", "Story", "Adventure"],
        "accent": "linear-gradient(135deg, #b45309, #f59e0b)"
    },
    {
        "id": 6,
        "rank": 6,
        "name": "Minecraft",
        "genre": "Sandbox",
        "score": 8.7,
        "price": 29,
        "discount": 0,
        "players": "2.1M",
        "tags": ["Creative", "Multiplayer", "Survival"],
        "accent": "linear-gradient(135deg, #0f766e, #22c55e)"
    }
]

@home_bp.route('/')
def home():
    query = request.args.get("q", "").strip().lower()
    genre = request.args.get("genre", "all")
    sort_by = request.args.get("sort", "score")

    games = GAMES

    if query:
        games = [
            game for game in games
            if query in game["name"].lower()
            or any(query in tag.lower() for tag in game["tags"])
        ]

    if genre != "all":
        games = [game for game in games if game["genre"] == genre]

    if sort_by == "price":
        games = sorted(games, key=lambda game: game["price"])
    elif sort_by == "name":
        games = sorted(games, key=lambda game: game["name"].lower())
    else:
        games = sorted(games, key=lambda game: (-game["score"], game["rank"]))

    return render_template(
        "home.html",
        games=games,
        selected_genre=genre,
        selected_sort=sort_by,
        search_query=request.args.get("q", "")
    )
