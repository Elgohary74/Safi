from flask import render_template

from app import create_app

app = create_app()


@app.route("/")
def index():
    return render_template("index.html")


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


# --- Error Handlers ---
@app.errorhandler(400)
def bad_request(e):
    return (
        render_template("error.html", error_code=400, error_message="Bad Request"),
        400,
    )


@app.errorhandler(401)
def unauthorized(e):
    return (
        render_template(
            "error.html", error_code=401, error_message="Unauthorized Access"
        ),
        401,
    )


@app.errorhandler(403)
def forbidden(e):
    return render_template("error.html", error_code=403, error_message="Forbidden"), 403


@app.errorhandler(404)
def page_not_found(e):
    return (
        render_template("error.html", error_code=404, error_message="Page Not Found"),
        404,
    )


@app.errorhandler(500)
def internal_server_error(e):
    return (
        render_template(
            "error.html", error_code=500, error_message="Internal Server Error"
        ),
        500,
    )


if __name__ == "__main__":
    app.run(port=5000)
