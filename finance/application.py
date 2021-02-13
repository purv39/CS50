import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    users = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])
    quotes = {}

    for stock in stocks:
        quotes[stock["symbol"]] = lookup(stock["symbol"])

    share_sold = db.execute("SELECT price_per_share FROM transactions WHERE user_id = :id AND shares < 0", id = session["user_id"])
    price_sold = 0
    for row in share_sold:
        price_sold += row["price_per_share"]
    price_bought = 0
    share_bought = db.execute("SELECT price_per_share FROM transactions WHERE user_id = :id AND shares > 0", id = session["user_id"])
    for row in share_bought:
        price_bought += row["price_per_share"]

    cash_remaining = users[0]["cash"]
    total = cash_remaining + price_bought - price_sold

    return render_template("portfolio.html", quotes=quotes, stocks=stocks, total=total, cash_remaining=cash_remaining)




@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")
    else:
        quote = lookup(request.form.get("symbol"))

        shares = int(request.form.get("shares"))

        if shares <= 0 or shares == "" or quote == None:
            return apology("Not valid")

        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        cash_remaining = rows[0]["cash"]
        price_per_share = quote["price"]

        total_price = price_per_share * shares

        if total_price > cash_remaining:
            return apology("Not enough funds")
        else:
            db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id",price = total_price, user_id = session["user_id"])
            db.execute("INSERT INTO transactions (user_id,symbol,shares,price_per_share) VALUES(:user_id,:symbol,:shares,:price)",
                        user_id = session["user_id"],symbol = request.form.get("symbol"), shares = shares, price = total_price)
            flash("Bought!")

        return redirect("/")




@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = :id", id = session["user_id"])
    return render_template("history.html",transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)


        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("invalid symbol", 400)

        return render_template("quotted.html", quote=quote)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        usr = request.form.get("username")
        passw = request.form.get("password")
        conf = request.form.get("confirmation")

        rows = db.execute("SELECT * FROM users WHERE username = :user",user=usr)

        if usr == "":
            return apology("Please Enter A Username",202)
        elif len(rows) == 1:
            return apology("Username already exists",203)

        if passw == "":
            return apology("Please enter Password",300)
        elif passw != conf:
            return apology("Passwords do not match",301)

        hashed_pass = generate_password_hash(passw)

        db.execute("INSERT INTO users (username,hash) VALUES(:usr,:passw)",usr = usr, passw = hashed_pass)

        return redirect("/")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        stocks = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])

        return render_template("sell.html",stocks=stocks)
    else:
        quote = lookup(request.form.get("symbol"))

        shares = int(request.form.get("shares"))

        if shares <= 0 or shares == "" or quote == None:
            return apology("Not valid")

        stock = db.execute("SELECT SUM(shares) as total_shares  FROM transactions WHERE symbol = :symbol AND user_id = :id",
                            symbol = request.form.get("symbol"), id = session["user_id"])

        if shares > stock[0]["total_shares"]:
            return apology("You cannot sell shares more than you own")
        else:
            rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

            # How much $$$ the user still has in her account
            cash_remaining = rows[0]["cash"]
            price_per_share = quote["price"]

            # Calculate the price of requested shares
            total_price = price_per_share * shares

            db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price_per_share) VALUES(:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"],
                   symbol=request.form.get("symbol"),
                   shares=-shares,
                   price=total_price)

            flash("Sold!")


            return redirect("/")

@app.route("/add", methods = ["GET","POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add_funds.html")
    else:
        add_cash = float(request.form.get("amount"))
        if add_cash == "" or add_cash <= 0:
            return apology("Not valid")
        else:
            db.execute("UPDATE users SET cash = cash + :add WHERE id = :id", add = add_cash, id = session["user_id"])
            return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
#pk_1d8b33e8e4b541aaadb75091fc3cfd71


