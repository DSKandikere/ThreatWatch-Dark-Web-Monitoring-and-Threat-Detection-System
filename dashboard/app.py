from flask import Flask, render_template, request, redirect, session
from elasticsearch import Elasticsearch
import sqlite3
from collections import Counter

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Elasticsearch Connection
es = Elasticsearch("http://localhost:9200")


# =========================================================
# DATABASE SETUP
# =========================================================
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    # Default users
    c.execute(
        "INSERT OR IGNORE INTO users VALUES ('admin', 'admin123', 'admin')"
    )

    c.execute(
        "INSERT OR IGNORE INTO users VALUES ('analyst', 'analyst123', 'analyst')"
    )

    conn.commit()
    conn.close()


# =========================================================
# LOGIN REQUIRED DECORATOR
# =========================================================
def login_required(f):
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect("/login")
        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper


# =========================================================
# ROLE CHECK DECORATOR
# =========================================================
def role_required(role):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if session.get("role") != role:
                return "Access Denied", 403
            return f(*args, **kwargs)

        wrapper.__name__ = f.__name__
        return wrapper

    return decorator


# =========================================================
# LOGIN PAGE
# =========================================================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password)
        )

        result = c.fetchone()
        conn.close()

        if result:
            session["user"] = username
            session["role"] = result[0]
            return redirect("/")

        else:
            return "Invalid Credentials"

    return render_template("login.html")


# =========================================================
# LOGOUT
# =========================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# =========================================================
# DASHBOARD
# =========================================================
@app.route("/")
@login_required
def index():

    query = request.args.get("q", "")

    # Search Query
    if query:

        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": [
                        "content",
                        "parsed_data.emails",
                        "parsed_data.passwords",
                        "parsed_data.credit_cards",
                        "parsed_data.api_keys",
                        "parsed_data.phone_numbers",
                        "parsed_data.usernames",
                        "parsed_data.addresses",
                        "parsed_data.employee_ids",
                        "parsed_data.student_ids"
                    ]
                }
            }
        }

    else:
        body = {
            "query": {
                "match_all": {}
            }
        }

    # Elasticsearch Search
    res = es.search(index="darkweb", body=body, size=100)

    hits = res["hits"]["hits"]

    results = [hit["_source"] for hit in hits]

    # =====================================================
    # ANALYTICS COUNTERS
    # =====================================================
    dates = []

    email_count = 0
    password_count = 0
    creditcard_count = 0
    apikey_count = 0
    phone_count = 0
    username_count = 0
    address_count = 0
    employeeid_count = 0
    studentid_count = 0

    # =====================================================
    # LOOP THROUGH RESULTS
    # =====================================================
    for item in results:

        # Date Extraction
        if "timestamp" in item:
            dates.append(item["timestamp"][:10])

        parsed = item.get("parsed_data", {})

        # Count Leaked Data
        email_count += len(parsed.get("emails", []))
        password_count += len(parsed.get("passwords", []))
        creditcard_count += len(parsed.get("credit_cards", []))
        apikey_count += len(parsed.get("api_keys", []))
        phone_count += len(parsed.get("phone_numbers", []))
        username_count += len(parsed.get("usernames", []))
        address_count += len(parsed.get("addresses", []))
        employeeid_count += len(parsed.get("employee_ids", []))
        studentid_count += len(parsed.get("student_ids", []))

    # =====================================================
    # DATE-WISE BREACH COUNTS
    # =====================================================
    date_counts = Counter(dates)

    chart_labels = list(date_counts.keys())
    chart_values = list(date_counts.values())

    # =====================================================
    # LEAK TYPE CHART
    # =====================================================
    leak_labels = [
        "Emails",
        "Passwords",
        "Credit Cards",
        "API Keys",
        "Phone Numbers",
        "Usernames",
        "Addresses",
        "Employee IDs",
        "Student IDs"
    ]

    leak_values = [
        email_count,
        password_count,
        creditcard_count,
        apikey_count,
        phone_count,
        username_count,
        address_count,
        employeeid_count,
        studentid_count
    ]

    # =====================================================
    # RENDER TEMPLATE
    # =====================================================
    return render_template(
        "index.html",

        results=results,
        role=session.get("role"),
        query=query,

        # Date chart
        chart_labels=chart_labels,
        chart_values=chart_values,

        # Leak analytics chart
        leak_labels=leak_labels,
        leak_values=leak_values,

        # Individual Counters
        email_count=email_count,
        password_count=password_count,
        creditcard_count=creditcard_count,
        apikey_count=apikey_count,
        phone_count=phone_count,
        username_count=username_count,
        address_count=address_count,
        employeeid_count=employeeid_count,
        studentid_count=studentid_count
    )


# =========================================================
# ADMIN PANEL
# =========================================================
@app.route("/admin")
@login_required
@role_required("admin")
def admin_panel():
    return "Admin Panel - Full Access"


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
