from flask import render_template

from app import create_app

app = create_app()


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=5000)
