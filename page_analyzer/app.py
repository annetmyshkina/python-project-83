from flask import Flask, render_template, flash, request, redirect, url_for
from page_analyzer.models import create_url, get_urls, get_url_by_id
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__, template_folder="../templates")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/urls", methods=['GET', 'POST'])
def urls():
    if request.method == 'POST':
        url_input = request.form['url'].strip()
        success, message, result = create_url(url_input)

        flash(message, 'danger' if not success else 'success')

        if not result:
            return redirect(url_for('index'))

        return redirect(url_for('url', url_id=result))

    return render_template('urls.html', urls=get_urls())



@app.route("/urls/<int:url_id>")
def url(url_id):
    url_data = get_url_by_id(url_id)
    if not url_data:
        return redirect(url_for('urls'))
    return render_template('url.html', url=url_data)


if __name__ == "__main__":
    app.run()
