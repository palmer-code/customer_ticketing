from flask import Flask, redirect, url_for
from config import SERVER_IP, PORT
from routes.kiosk import bp as kiosk_bp
from routes.operator import bp as operator_bp
from routes.display import bp as display_bp
# from routes.operator import bp as operator_bp
# from routes.display import bp as display_bp

app = Flask(__name__, static_folder='static', template_folder='templates')

# Register blueprints
app.register_blueprint(kiosk_bp)
app.register_blueprint(operator_bp)
app.register_blueprint(display_bp)

@app.route('/')
def index():
    return redirect(url_for('kiosk.kiosk'))

if __name__ == '__main__':
    from db import init_db
    print("Initializing database...")
    init_db()
    app.run(host=SERVER_IP, port=PORT, debug=True)
