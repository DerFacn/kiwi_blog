import os
import json
from app import db
from json.decoder import JSONDecodeError
from app.models import Post, PostTag, Tag
from .utils import count_reading_time, safe_filename, allowed_file
from app.utils import jwt_required, get_user, get_first_or_false, get_all
from flask import render_template, request, flash, current_app, abort, redirect, url_for


def fetch_tags():
    tags_results = get_all(Tag.select())

    response = [tag.name for tag in tags_results]

    return response


def view_post(post_id):
    post = get_first_or_false(Post.select().filter_by(id=post_id))

    if not post:
        return abort(404)

    response = {
        "id": post.id,
        "preview": post.preview,
        "title": post.title,
        "tags": post.tags,
        "content": post.content,
        "author": post.author,
        "created_at": post.created_at
    }

    return render_template('posts/post.html', title=post.title, post=response)


@jwt_required
def create_post():
    if request.method == 'POST':
        errors = False
        title = request.form.get('title')  # TODO: maybe rewrite this all with marshmallow?
        preview = request.files.get('preview')
        tags_raw = request.form.get('tags')
        content = request.form.get('content')

        if not title:
            flash('Title is required!', 'danger')
            errors = True

        if not preview:  # In case if form doesn't have preview part
            flash('No preview part!', 'danger')
            errors = True

        if preview.filename == "":  # In case if empty file
            flash('Preview not selected!', 'danger')
            errors = True

        if not allowed_file(preview.filename):
            flash('Not allowed filetype!', 'danger')
            errors = True

        if not content:
            flash('Content is required!')
            errors = True

        if errors:
            return render_template('posts/create.html', title="New post")
            # TODO: yes, i must refactor this on marshmallow

        user = get_user()

        # Saving file
        filetype = preview.filename.split('.')[-1]
        filename = safe_filename(user.username) + f".{filetype}"
        path = os.path.join(current_app.config.get('PREVIEWS_STORAGE'), filename)
        preview.save(path)

        # Creating new post
        new_post = Post(
            preview=filename,
            title=title,
            content=content,
            reading_time=count_reading_time(content),
            author_id=user.uuid
        )

        db.session.add(new_post)
        db.session.flush()

        # Creating new tags
        try:
            tags_list = json.loads(tags_raw)
            tags = [tag['value'] for tag in tags_list]

            for value in tags:
                tag = get_first_or_false(Tag.select().filter_by(name=value))

                if not tag:
                    tag = Tag(name=value)
                    db.session.add(tag)
                    db.session.flush()

                new_post_tag = PostTag(post_id=new_post.id, tag_id=tag.id)
                db.session.add(new_post_tag)
                db.session.flush()
        except JSONDecodeError:
            pass
        except KeyError:  # In case if user sends broken tag list
            flash("Unexpected tag format! Try again.")
            return render_template('posts/create.html', title="New post")

        db.session.commit()

        return redirect(url_for('posts.view_post', post_id=new_post.id))

    return render_template('posts/create.html', title="New post")


@jwt_required
def edit_post(post_id: int):
    user = get_user()
    post = get_first_or_false(Post.select().filter_by(id=post_id))

    if not post:
        return abort(404)

    if user.uuid != post.author_id:
        return redirect(url_for('main.index'))

    tags_names = ", ".join([post_tag.tag.name for post_tag in post.tags])

    if request.method == 'POST':
        errors = False
        title = request.form.get('title')
        preview = request.files.get('preview')
        tags_raw = request.form.get('tags')
        content = request.form.get('content')

        if not title:
            flash('Title is required!', 'danger')

        if not content:
            flash('Content is required!', 'danger')
            errors = True

        if errors:
            return render_template('posts/edit.html', title=f"Editing '{post.title}'", post=post, tags=tags_names)

        if preview and allowed_file(preview.filename):
            filetype = preview.filename.split('.')[-1]
            filename = safe_filename(user.username) + f".{filetype}"
            path = os.path.join(current_app.config.get('PREVIEWS_STORAGE'), filename)
            preview.save(path)

            post.preview = filename

        try:
            tags_list = json.loads(tags_raw)
            tags = [tag['value'] for tag in tags_list]

            for value in tags:
                if value in tags_names:
                    continue

                tag = get_first_or_false(Tag.select().filter_by(name=value))

                if not tag:
                    tag = Tag(name=value)
                    db.session.add(tag)
                    db.session.flush()

                new_post_tag = PostTag(post_id=post.id, tag_id=tag.id)
                db.session.add(new_post_tag)
                db.session.flush()
        except JSONDecodeError:
            pass
        except KeyError:  # In case if user sends broken tag list
            flash("Unexpected tag format! Try again.")
            return render_template('posts/edit.html', title=f"Editing '{post.title}'", post=post, tags=tags_names)

        post.title = title
        post.content = content

        db.session.commit()

        return redirect(url_for('main.you'))

    return render_template('posts/edit.html', title=f"Editing '{post.title}'", post=post, tags=tags_names)


@jwt_required
def delete_post(post_id: int):
    user = get_user()
    post = get_first_or_false(Post.select().filter_by(id=post_id))

    if not post:
        return abort(404)

    if user.uuid != post.author_id:
        return redirect(url_for('main.index'))

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('main.you'))
