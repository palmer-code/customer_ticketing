from flask import Blueprint, render_template, jsonify
import threading
from config import CATEGORIES
from db import add_ticket_to_db
from printer import print_ticket
import time

bp = Blueprint('kiosk', __name__)
queues = {k: [] for k in CATEGORIES.keys()}
ticket_counters = {}

def assign_counter_for_category(category_code, queues):
    meta = CATEGORIES[category_code]
    eligible_counters = meta["counters"]
    # Count tickets assigned to each eligible counter across all categories
    counter_loads = {c: 0 for c in eligible_counters}
    for queue in queues.values():
        for _, assigned_counter, _ in queue:  # <-- Unpack 3 values now
            if assigned_counter in counter_loads:
                counter_loads[assigned_counter] += 1
    # Find the counter with the fewest tickets
    min_counter = min(eligible_counters, key=lambda c: counter_loads[c])
    return min_counter

@bp.route('/kiosk')
def kiosk():
    return render_template('kiosk.html', categories=CATEGORIES)

@bp.route('/kiosk/take/<prefix>', methods=['POST'])
def take_ticket(prefix):
    if prefix not in CATEGORIES:
        return jsonify({"ok": False, "error": "Invalid category"}), 400
    ticket_counters[prefix] = ticket_counters.get(prefix, 100) + 1
    num = ticket_counters[prefix]
    counter = assign_counter_for_category(prefix, queues)
    timestamp = time.time()
    queues[prefix].append((num, counter, timestamp))  # <-- now includes timestamp
    add_ticket_to_db(prefix, num, counter)
    threading.Thread(target=print_ticket, args=(prefix, num, counter), daemon=True).start()
    return jsonify({"ok": True, "ticket": f"{prefix}{num}", "counter": counter})

