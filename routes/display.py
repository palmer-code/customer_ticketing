from flask import Blueprint, render_template, jsonify
import sqlite3
from config import CATEGORIES, DB

bp = Blueprint('display', __name__)

@bp.route('/display')
def display():
    return render_template('display.html')

@bp.route('/api/status')
def api_status():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    last_served = {}
    for prefix in CATEGORIES.keys():
        c.execute("SELECT number, counter, served_at FROM tickets WHERE prefix=? AND status='served' ORDER BY served_at DESC LIMIT 1", (prefix,))
        r = c.fetchone()
        last_served[prefix] = {"number": r[0], "counter": r[1], "served_at": r[2]} if r else None
    conn.close()
    return jsonify({"last_served": last_served})
