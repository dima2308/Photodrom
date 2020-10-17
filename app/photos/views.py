from app import db
from . import photos
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required
from app.models import Photo, Category, Comment, User
from .forms import PhotoForm, CommentForm
from app.utils import sort_photos


@photos.route('/')
def index():
    search = request.args.get('search')
    page = request.args.get('page')
    sort_param = request.args.get('sort')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if sort_param:
        photos = sort_photos(sort_param)
        pages = photos.paginate(page=page, per_page=6)
        return render_template('photos/include/set_photos.html', pages=pages)

    if search:
        photos = Photo.query.filter(Photo.title.contains(
            search) | Photo.description.contains(search))
    else:
        photos = Photo.query

    pages = photos.paginate(page=page, per_page=6)

    return render_template('photos/photos.html', pages=pages)


@photos.route('/users')
@login_required
def users():
    users = User.query.all()
    photos = len(Photo.query.all())
    return render_template('photos/users.html', users=users, count_photos=photos)


@photos.route('/<slug>')
def photo_detail(slug):
    photo = Photo.query.filter(Photo.slug == slug).first_or_404()
    form = CommentForm()
    return render_template('photos/photo_detail.html', photo=photo, form=form)


@photos.route('/add_photo', methods=["GET", "POST"])
@login_required
def add_photo():
    form = PhotoForm()

    if request.method == 'POST' and form.validate_on_submit():
        form_title = request.form.get('title').capitalize()
        form_description = request.form.get('description')
        form_url = request.form.get('url')
        form_category = request.form.get('category')

        photo = Photo.query.filter(Photo.title == form_title).first_or_404()
        category_id = Category.query.filter(
            Category.name == form_category).first_or_404()

        if not(photo):
            new_photo = Photo(title=form_title, slug=form_title, description=form_description, url=form_url,
                              category=category_id, author_id=current_user.user_id)

            db.session.add(new_photo)
            db.session.commit()

            return redirect('/')
        else:
            flash("Фотография с таким названием уже существует")

    return render_template('photos/add_photo.html', form=form)


@photos.route('/<slug>/edit', methods=["GET", "POST"])
@login_required
def edit_photo(slug):
    photo = Photo.query.filter(Photo.slug == slug).first_or_404()
    form = PhotoForm(formdata=request.form, obj=photo)

    if request.method == 'POST' and form.validate_on_submit():
        form_title = request.form.get('title').capitalize()
        if Photo.query.filter(Photo.title == form_title).first_or_404():
            if photo.title == form_title:
                pass
            else:
                flash('Фотография с таким названием уже существует!')
                return render_template('photos/edit_photo.html', photo=photo, form=form)

        category_id = Category.query.filter(
            Category.name == request.form.get('category')).first_or_404()

        photo.title = request.form.get('title').capitalize()
        photo.description = request.form.get('description')
        photo.url = request.form.get('url')
        photo.category = category_id

        db.session.commit()

        return redirect(url_for('photos.photo_detail', slug=photo.slug))

    return render_template('photos/edit_photo.html', photo=photo, form=form)


@photos.route('/<slug>/delete', methods=["GET", "POST"])
@login_required
def delete_photo(slug):
    photo = Photo.query.filter(Photo.slug == slug).first_or_404()

    db.session.delete(photo)
    db.session.commit()

    return redirect(url_for('photos.index'))


@photos.route('/<slug>/like')
def like(slug):
    photo = Photo.query.filter(Photo.slug == slug).first()

    if current_user in photo.likes:
        photo.likes.remove(current_user)
        photo.count_likes = photo.count_likes - 1
    else:
        photo.likes.append(current_user)
        photo.count_likes = photo.count_likes + 1

    db.session.commit()

    return redirect(url_for('photos.index'))


@photos.route('/<slug>/add_comment', methods=['GET', 'POST'])
def add_comment(slug):
    form = CommentForm()
    photo = Photo.query.filter(Photo.slug == slug).first_or_404()

    if request.method == 'POST' and form.validate_on_submit():
        photo = Photo.query.filter(Photo.slug == slug).first_or_404()
        form_body = request.form.get('body')

        new_comment = Comment(author_id=current_user.user_id,
                              photo_id=photo.photo_id, body=form_body)

        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('photos.photo_detail', slug=photo.slug))

    return render_template('photos/photo_detail.html', photo=photo, form=form)
