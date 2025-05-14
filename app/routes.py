from flask import Blueprint, request, render_template, jsonify, session, redirect, url_for
from .database import search_people

routes = Blueprint("routes", __name__)

@routes.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "152212":
            session["authorized"] = True  # ✅ теперь с отступом
            return redirect(url_for("routes.search"))
    return render_template("login.html")

@routes.route("/search")
def search():
    if not session.get("authorized"):
        return redirect(url_for("routes.index"))
    return render_template("search.html")

@routes.route("/api/search")
def api_search():
    if not session.get("authorized"):
        return jsonify({"error": "unauthorized"}), 401
    q = request.args.get("q", "")
    results = search_people(q)
    return jsonify({"results": [
        {
            "last_name": r[0], "first_name": r[1], "middle_name": r[2],
            "birthdate": r[3], "phone": r[4], "position": r[5]
        } for r in results
    ]})
