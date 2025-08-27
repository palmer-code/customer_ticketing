from flask import Blueprint, render_template, jsonify
from config import CATEGORIES
from db import mark_served_in_db
from tts import tts_say

bp = Blueprint('operator', __name__, url_prefix="/operator")

# in-memory queues shared with kiosk
from routes.kiosk import queues

@bp.route('/<int:counter>')
def operator(counter):
    return render_template('operator.html', counter=counter, categories=CATEGORIES)

@bp.route('/<int:counter>/call', methods=['POST'])
def call_next(counter):
    served = None
    for prefix, meta in CATEGORIES.items():
        if meta.get('default_counter') == counter and queues[prefix]:
            num, assigned_counter = queues[prefix].pop(0)
            served = (prefix, num, assigned_counter)
            break

    if not served:
        return jsonify({"ok": False, "message": "No tickets"}), 200

    prefix, num, assigned_counter = served
    mark_served_in_db(prefix, num)
    announce_text = f"Ticket {prefix}{num}, please proceed to counter {counter}"
    tts_say(announce_text)
    return jsonify({"ok": True, "ticket": f"{prefix}{num}", "counter": counter, "announce": announce_text})
