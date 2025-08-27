from flask import Blueprint, render_template, jsonify
import threading
from config import CATEGORIES
from db import add_ticket_to_db
from printer import print_ticket

bp = Blueprint('kiosk', __name__)
queues = {k: [] for k in CATEGORIES.keys()}
ticket_counters = {}

@bp.route('/kiosk')
def kiosk():
    return render_template('kiosk.html', categories=CATEGORIES)

@bp.route('/kiosk/take/<prefix>', methods=['POST'])
def take_ticket(prefix):
    if prefix not in CATEGORIES:
        return jsonify({"ok": False, "error": "Invalid category"}), 400
    # increment ticket number
    ticket_counters[prefix] = ticket_counters.get(prefix, 100) + 1
    num = ticket_counters[prefix]
    counter = CATEGORIES[prefix]['default_counter']
    queues[prefix].append((num, counter))
    add_ticket_to_db(prefix, num, counter)
    threading.Thread(target=print_ticket, args=(prefix, num, counter), daemon=True).start()
    return jsonify({"ok": True, "ticket": f"{prefix}{num}", "counter": counter})

