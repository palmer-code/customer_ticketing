DB = 'queue.db'
SERVER_IP = '0.0.0.0'
PORT = 5000

CATEGORIES = {
    "A": {"label": "Account Opening", "default_counter": 1},
    "L": {"label": "Loan Enquiries",  "default_counter": 2},
    "G": {"label": "General Queries", "default_counter": 3}
}
COUNTER_MAP = {1: "A", 2: "L", 3: "G"}
