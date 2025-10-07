from flask import Blueprint, render_template, jsonify
from config import CATEGORIES
from db import mark_served_in_db
from tts import tts_say

bp = Blueprint('operator', __name__, url_prefix="/operator")

# in-memory queues shared with kiosk
from routes.kiosk import queues

current_serving = {}  # counter_number: (prefix, num)

@bp.route('/<int:counter>')
def operator(counter):
    return render_template('operator.html', counter=counter, categories=CATEGORIES)

@bp.route('/<int:counter>/call', methods=['POST'])
def call_next(counter):
    # Collect all tickets assigned to this counter from all categories
    candidates = []
    for prefix, queue in queues.items():
        for i, (num, assigned_counter, timestamp) in enumerate(queue):
            if assigned_counter == counter:
                candidates.append((timestamp, prefix, i, num))
    if not candidates:
        return jsonify({"ok": False, "message": "No tickets"}), 200

    # Find the oldest ticket (smallest timestamp)
    candidates.sort()
    timestamp, prefix, idx, num = candidates[0]
    # Remove from the queue
    queues[prefix].pop(idx)
    mark_served_in_db(prefix, num)
    announce_text = f"Ticket {prefix}{num}, please proceed to counter {counter}"
    tts_say(announce_text)
    current_serving[counter] = (prefix, num)  # <-- Track currently serving
    return jsonify({"ok": True, "ticket": f"{prefix}{num}", "counter": counter, "announce": announce_text})

@bp.route('/<int:counter>/new_tickets')
def new_tickets(counter):
    tickets = []
    for prefix, queue in queues.items():
        for num, assigned_counter, timestamp in queue:
            if assigned_counter == counter:
                tickets.append((timestamp, prefix, num))
    # Sort by timestamp (oldest first)
    tickets.sort()
    ticket_strings = [f"{prefix}{num}" for _, prefix, num in tickets]
    return jsonify(ticket_strings)

@bp.route('/display/current')
def display_current():
    # Only show counters 1, 2, 3
    result = {}
    for counter in [1, 2, 3]:
        if counter in current_serving:
            prefix, num = current_serving[counter]
            result[counter] = f"{prefix}{num}"
        else:
            result[counter] = "-"
    return jsonify(result)
