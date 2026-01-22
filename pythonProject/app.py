from datetime import datetime
from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect, secure_filename
import os
import re


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///article.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    intro = db.Column(db.String, nullable=False)
    full_title = db.Column(db.Text, nullable=False)
    full_text = db.Column(db.Text, nullable=False)
    image_urls = db.Column(db.Text, nullable=False)
    full_ingredient = db.Column(db.Text, nullable=False)
    full_gram = db.Column(db.Text, nullable=False)
    number = db.Column(db.Integer)
    ingredient_num = db.Column(db.Integer)
    file_dish = db.Column(db.Text, nullable=False)
    select_gram = db.Column(db.Text, nullable=False)


@app.route('/add_recipe', methods=['POST', 'GET'])
def add_recipe():
    if request.method == 'POST':
        name = request.form['name']
        intro = request.form['intro']
        number = request.form['part']
        ingredient = request.form['ingredient']
        if number == '' or int(number) <= 0 or int(number) > 10:
            return 'некоректное значение главы'
        else:
            if ingredient == '' or int(ingredient) <= 0:
                return 'некоректное значение главы'
            else:
                return redirect(url_for('recipe',
                                        name=name,
                                        intro=intro,
                                        number=number,
                                        ingredient=ingredient))
    return render_template('add_recipe.html')


@app.route(
    '/settings_recipe/<name>_<intro>_<number>_<ingredient>',
           methods=['POST', 'GET'])
def recipe(name, intro, number, ingredient):
    number1 = int(number)
    ingredient1 = int(ingredient)
    if request.method == 'POST':
        name = request.form['name']
        intro = request.form['intro']
        file_dish = request.files['image_dish']
        full_text = []
        full_title = []
        image_urls = []
        full_ingredient = []
        full_gram = []
        full_select = []
        delimiter = ' $$$ '  # Замените на нужный вам разделитель

        for i in range(number1):
            file = request.files.get(f'image{i}')
            if file:
                filename = secure_filename(file.filename)
                upload_folder = os.path.join('static', 'uploads')
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                image_url = f'static/uploads/{filename}'
                image_urls.append(image_url)
                image_delimiter = delimiter.join(image_urls)
            else:
                print("Файл не был передан.")


        for i in range(ingredient1):
            ingredient2 = request.form.get(f'ingredient{i}')
            gram = request.form.get(f'gram{i}')
            full_ingredient.append(ingredient2)
            ingredient_delimiter = delimiter.join(full_ingredient)
            full_gram.append(gram)
            gram_delimiter = delimiter.join(full_gram)
            gram_select = request.form[f'gram_select{i}']
            full_select.append(gram_select)
            select_delimiter = delimiter.join(full_select)


        for i in range(number1):
            title = request.form.get(f'title{i}', '')
            full_title.append(title)
            title_delimiter = delimiter.join(full_title)
            text = request.form.get(f'text{i}', '')
            full_text.append(text)
            text_delimiter = delimiter.join(full_text)


        if file_dish:
            filename = secure_filename(file_dish.filename)
            upload_folder = os.path.join('static', 'uploads')
            file_path = os.path.join(upload_folder, filename)
            file_dish.save(file_path)
            dish_url = f'static/uploads/{filename}'
        article = Article(
            name=name,
            intro = intro,
            full_title = title_delimiter,
            full_text = text_delimiter,
            image_urls = image_delimiter,
            full_ingredient = ingredient_delimiter,
            full_gram = gram_delimiter,
            number = number1,
            ingredient_num = ingredient1,
            file_dish = dish_url,
            select_gram = select_delimiter
        )
        try:
            db.session.add(article)
            db.session.commit()
        except:
            return 'не удалось создать статью'

        return redirect('/')
    return render_template('settings_recipe.html',
                           name=name,
                           intro=intro,
                           number=number1,
                           ingredient=ingredient1)


@app.route('/')
@app.route('/posts')
def posts():
    articles = Article.query.all()
    return render_template("home.html", articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    delimiter = ' $$$ '
    return render_template("post_detail.html", article=article)


if __name__ == '__main__':
    app.run(debug=True)
