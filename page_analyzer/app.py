import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from page_analyzer.models import URLService

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

url_service = URLService()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls", methods=["GET", "POST"])
def urls():
    if request.method == "POST":
        url_input = request.form["url"].strip()
        success, message, url_id = url_service.create_url(url_input)

        flash(message, "danger" if not success else "success")

        if url_id:
            return redirect(url_for("url", id=url_id))
        return render_template("urls.html"), 422

    return render_template(
        "urls.html",
        urls=url_service.get_urls_with_last_check())


@app.route("/urls/<int:id>")
def url(id):
    url_data = url_service.get_url_by_id(id)
    if not url_data:
        return redirect(url_for("urls"))

    checks = url_service.get_checks_url(id)
    return render_template("url.html", url=url_data, checks=checks)


@app.route("/urls/<int:id>/checks", methods=["POST"])
def check_url(id):
    if url_service.create_check_url(id):
        flash("Страница успешно проверена", "success")
    else:
        flash("Произошла ошибка при проверке", "danger")

    return redirect(url_for("url", id=id))


if __name__ == "__main__":
    app.run()
