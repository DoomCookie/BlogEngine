import datetime

from flask import Flask, render_template, url_for, redirect

from data import db_session

from forms.user import RegisterForm, LoginForm
from forms.post import CreatePostForm, DeletePostForm, EditPostForm
from forms.tag import CreateTagForm, DeleteTagForm, EditTagForm

from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user

from flask_restful import reqparse, abort, Api, Resource, reqparse
from data import post_resources

from data.users import User
from data.posts import Post
from data.tags import Tag

from slugify import slugify
from time import time

# TODO:  удаление редактикрование тэгов *
#        автоматическое создание ссылки *
#        проверка ссылки на то, что она не совпадает с create, delete*
#        проверка, что ссылка уникальная, если нет добавить к ней время*
#        Отображение не всего текста в превьюхе*
#        REFACTORING всего кода на одинаковые названия, ковычки, красоту*
#        запилть лайки дизлайки для обычных пользователей
#        админка для назначения пользователей админами
#        добавить комментарии - космос


DB_PATH = 'db/db.sqlite3'

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'BlockEngine'


login_manager = LoginManager()
login_manager.init_app(app)

def get_slug(obj, txt):
    db_sess = db_session.create_session()
    objs = db_sess.query(obj.__class__).filter()
    slug = slugify(txt)
    if slug in [x.slug for x in db_sess.query(obj.__class__)[:]] or slug in ['create', 'delete', 'edit']:
        slug = slug + '-' +str(int(time()))
    return slug

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).filter(Post.is_private != True)[::-1]
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message='Такой пользователь уже есть')
        user = User(
            name=form.name.data,
            email=form.email.data,
            role=10
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message='Неправильный логин или пароль',
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/post/create',  methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    db_sess = db_session.create_session()
    form.tags.choices = [(x.title, x.title) for x in db_sess.query(Tag)]
    if form.validate_on_submit():
        post = Post()
        post.title = form.title.data
        post.content = form.content.data
        post.is_private = form.is_private.data
        if form.slug.data == '':
            post.slug = get_slug(post, post.title)
        else:
            post.slug = get_slug(post, form.slug.data)
        for tag in db_sess.query(Tag):
            if tag.title in form.tags.data:
                post.tags.append(tag)

        post.user_id = current_user.id
        db_sess.add(post)
        db_sess.commit()
        return redirect('/')
    return render_template('create_post.html', title='Добавление поста',
                           form=form)

@app.route('/post/<string:slug>',  methods=['GET', 'POST'])
def post_detail(slug):
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.is_private != True, Post.slug == slug).first()
    return render_template('post_detail.html', post=post, detail=True)

@app.route('/post/<string:slug>/edit',  methods=['GET', 'POST'])
@login_required
def post_edit(slug):
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.is_private != True, Post.slug == slug).first()
    form = EditPostForm(obj=post)
    form.tags.choices = [(x.title, x.title) for x in db_sess.query(Tag)]
    # form.tags.default = [x.title for x in db_sess.query(Tag)] для установки тегов,
    # form.process() которые стоят до изменения, но это не работает
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_private = form.is_private.data
        if form.slug.data == '':
            post.slug = get_slug(post, post.title)
        else:
            post.slug = get_slug(post, form.slug.data)
        post.tags.clear()
        for tag in db_sess.query(Tag):
            if tag.title in form.tags.data:
                post.tags.append(tag)
        post.user_id = current_user.id
        db_sess.commit()
        return redirect('/')
    return render_template('edit_post.html', title='Добавление поста',
                            post=post, form=form)

@app.route('/post/<string:slug>/delete',  methods=['GET', 'POST'])
@login_required
def post_delete(slug):
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.is_private != True, Post.slug == slug).first()
    form = DeletePostForm()
    if form.validate_on_submit():
        db_sess.delete(post)
        db_sess.commit()
        return redirect('/')
    return render_template('delete_post.html', title='Добавление поста',
                            post=post, form=form)

@app.route('/tags')
def tags_list():
    db_sess = db_session.create_session()
    tags = db_sess.query(Tag)
    return render_template('tags_list.html', tags=tags)

@app.route('/tag/create',  methods=['GET', 'POST'])
@login_required
def create_tag():
    form = CreateTagForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        tag = Tag()
        tag.title = form.title.data
        if form.slug.data == "":
            tag.slug = get_slug(tag, tag.title)
        else:
            tag.slug = get_slug(tag, form.slug.data)
        db_sess.add(tag)
        db_sess.commit()
        return redirect('/')
    return render_template('create_tag.html', title='Добавление тега',
                           form=form)

@app.route('/tag/<string:slug>',  methods=['GET', 'POST'])
def tag_detail(slug):
    db_sess = db_session.create_session()
    tag = db_sess.query(Tag).filter(Tag.slug== slug).first()
    posts = db_sess.query(Post).filter(Post.is_private != True, Post.tags.contains(tag))[::-1]
    return render_template('tag_detail.html', posts=posts, tag=tag)

@app.route('/tag/<string:slug>/edit',  methods=['GET', 'POST'])
def tag_edit(slug):
    db_sess = db_session.create_session()
    tag = db_sess.query(Tag).filter(Tag.slug == slug).first()
    form = EditTagForm(obj=tag)
    if form.validate_on_submit():
        tag.title = form.title.data
        if form.slug.data == '':
            tag.slug = get_slug(tag, tag.title)
        else:
            tag.slug = get_slug(tag, form.slug.data)
        db_sess.commit()
        return redirect('/')
    return render_template('edit_tag.html', title='Добавление тега',
                           form=form)

@app.route('/tag/<string:slug>/delete',  methods=['GET', 'POST'])
def tag_delete(slug):
    db_sess = db_session.create_session()
    tag = db_sess.query(Tag).filter(Tag.slug == slug).first()
    form = DeleteTagForm()
    if form.validate_on_submit():
        db_sess.delete(tag)
        db_sess.commit()
        return redirect('/')
    return render_template('delete_tag.html', title='Добавление поста',
                            tag=tag, form=form)


def main():

    # для списка объектов
    api.add_resource(post_resources.PostListResource, '/api/posts')

    # для одного объекта
    api.add_resource(post_resources.PostResource, '/api/posts/<int:post_id>')

    db_session.global_init(DB_PATH)
    app.run(port=5000, host='127.0.0.1')


if __name__ == '__main__':
    main()
