
from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '')
        return f'<h1>Анализ {url}</h1><p>Функция в разработке</p>'

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
