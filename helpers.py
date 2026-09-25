import os
import sqlite3

from flask import redirect, render_template, session
from functools import wraps


# Initialize kmeans.db
DB_PATH = os.path.join("db", "kmeans.db")
SCHEMA_PATH = os.path.join("db", "schema.sql")

os.makedirs("db", exist_ok=True)

conn = sqlite3.connect(DB_PATH)

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    conn.executescript(f.read())
    

# Decorate routes to require login.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


# Execute a query in database
def sqlexecute(query, *args):
    conn = sqlite3.connect("db/kmeans.db")
    
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(query, args)
    
    result = None
    query_clean = query.strip().upper()
    
    if query_clean.startswith("SELECT"):
        result = [dict(row) for row in cursor.fetchall()]
    else:
        conn.commit()
        if query_clean.startswith("INSERT"):
            result = cursor.lastrowid
        else:
            result =  cursor.rowcount
            
    conn.close()
    return result
    
# Return an error page
def httperror(message, errorcode):
    return render_template("errorpage.html", message=message, errorcode=errorcode)