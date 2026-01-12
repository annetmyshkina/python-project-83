from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

load_dotenv()
# КЛЮЧЕВОЕ ИЗМЕНЕНИЕ:
app = Flask('page_analyzer', template_folder='../templates')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '')
        return f'''
        <div class="container mt-5">
            <div class="alert alert-success">
                <h4>Анализ страницы: <strong>{url}</strong></h4>
                <p>Функционал в разработке</p>
                <a href="/" class="btn btn-primary">← Новый анализ</a>
            </div>
        </div>
        '''
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
