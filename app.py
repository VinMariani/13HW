from flask import Flask, request, render_template, send_from_directory
from functions import get_tags, read_json, get_posts_by_tag, add_post

POST_PATH = "posts.json"
UPLOAD_FOLDER = "uploads/images"

app = Flask(__name__)


@app.route("/")
def page_index():
    data = read_json(POST_PATH)
    return render_template('index.html', tags=get_tags(data))


@app.route("/tag")
def page_tag():
    tag = request.args.get("tag")

    data = read_json(POST_PATH)
    posts = get_posts_by_tag(data, tag)
    return render_template('post_by_tag.html', tag=tag, posts=posts)


@app.route("/post", methods=["GET", "POST"]) #создание поста
def page_post_create():
    if request.method == "GET":
        return render_template("post_form.html")

    content = request.form.get('content')
    picture = request.files.get('picture')

    path = f'{UPLOAD_FOLDER}/{picture.filename}' #путь, куда сохранится картинка
    post = {                                     #добавляем пост в файл json
        'content': content,
        'pic': f'/{path}'
    }

    picture.save(path)         #сохраняем картинку из нового поста (загруженную пользователем)
    add_post(POST_PATH, post)  #добавляем пост

    return render_template('post_uploaded.html', post=post)


@app.route("/uploads/<path:path>") #ищем картинку, введя ее имя в строке браузера
def static_dir(path):
    return send_from_directory("uploads", path)


app.run()
