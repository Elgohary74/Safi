from flask import render_template
from app import create_app

app = create_app()

# --- Index Route ---
@app.route("/")
def index():
    return render_template("index.html")

# --- Dashboard Routes ---
@app.route("/dashboard")
def dashboard_index():
    return render_template("dashboard.html", groups=[], net_balance=0, amount_owed=0, amount_owing=0)

@app.route("/activity")
def dashboard_activity():
    return render_template("activity.html", activities=[])

@app.route("/settings")
def dashboard_settings():
    return render_template("settings.html")

# --- Group Routes ---
@app.route("/groups")
def list_groups():
    return render_template("groups.html", groups=[])

@app.route("/groups/create", methods=["POST"])
def create_group():
    return render_template("groups.html", groups=[])

# --- Static Pages Routes ---
@app.route("/info/about")
def about():
    return render_template("about.html")

@app.route("/info/faq")
def faq():
    return render_template("faq.html")

@app.route("/info/contact")
def contact():
    return render_template("contact.html")

# --- Auth Routes  ---
@app.route("/login")
def login_view():
    return render_template("auth_login.html")

@app.route("/register")
def register_view():
    return render_template("auth_register.html")

# --- Error Handlers ---
@app.errorhandler(400)
def bad_request(e):
    return render_template('error.html', error_code=400, error_message="Bad Request"), 400

@app.errorhandler(401)
def unauthorized(e):
    return render_template('error.html', error_code=401, error_message="Unauthorized Access"), 401

@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html', error_code=403, error_message="Forbidden"), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page Not Found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_code=500, error_message="Internal Server Error"), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)