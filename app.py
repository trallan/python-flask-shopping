from flask import Flask, render_template, request, session, redirect, g
from flask_session import Session
import sqlite3

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("store.db")
        g.db.row_factory = sqlite3.Row
    return g.db

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    db = get_db()
    books = db.execute("SELECT * FROM books")
    return render_template("books.html", books=books)

@app.route("/cart")
def cart():

    if "cart" not in session:
        session["cart"] = []

    if request.method == "POST":
        book_id = request.form.get("id")
        if book_id:
            session["cart"].append(book_id)
        return redirect("/cart")
    
    db = get_db()
    books = db.execute("SELECT * FROM books WHERE id IN (?)", session["cart"])
    return render_template("cart.html", books=books)