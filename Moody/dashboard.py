from . import ModelDriver
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

import base64
from PIL import Image
import io

from Moody.auth import login_required
from Moody.db import get_db

import operator


bp = Blueprint('dashboard', __name__)


@bp.route('/')
def index():
    """Show all the moods, most recent first."""
    if g.user != None:
        db = get_db()
        
        moods = db.execute(
            'SELECT m.id, mood_type, created, author_id, username'
            ' FROM mood m JOIN user u ON m.author_id = u.id'
            ' WHERE m.author_id = ?',
            (g.user['id'],)
        ).fetchall()

        
        mood_counter = {}

        for mood in moods:
            if(mood['mood_type'] in mood_counter):
                mood_counter[mood['mood_type']] += 1
            else:
                mood_counter[mood['mood_type']] = 1

        frequent_mood = max(mood_counter.items(), key=operator.itemgetter(1))[0]

        for key, value in mood_counter.items():
            mood_counter[key] = value/len(moods) * 100

        return render_template('dashboard/index.html', moods=moods, moods_size=len(moods), frequent_mood=frequent_mood, mood_distribution = mood_counter)

    return render_template('about.html')




@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == 'POST':
        f = request.form['file']

        f += "======================"
        base64_image_str = f[f.find(",")+1:]

        print(base64_image_str)

        imgdata = base64.b64decode(base64_image_str)
        filename = 'Moody/test_image.png'

        with open(filename, 'wb') as fil3:
            fil3.write(imgdata)

        im = Image.open("Moody/test_image.png")
        rgb_im = im.convert('RGB')
        rgb_im.save('Moody/test_image.jpg')


        mood_type = ModelDriver.do_all('test_image.jpg')

        error = None

        if not mood_type:
            error = 'mood_type is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO mood (mood_type, author_id)'
                ' VALUES (?,  ?)',
                (mood_type, g.user['id'])
            )
            db.commit()
            return redirect(url_for('dashboard.index'))

    return render_template('dashboard/create.html')




#commenting out get post route


# def get_post(id, check_author=True):
#     """Get a post and its author by id.
#     Checks that the id exists and optionally that the current user is
#     the author.
#     :param id: id of post to get
#     :param check_author: require the current user to be the author
#     :return: the post with author information
#     :raise 404: if a post with the given id doesn't exist
#     :raise 403: if the current user isn't the author
#     """
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, "Post id {0} doesn't exist.".format(id))

#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)

#     return post







# Commenting out update and delete routes

# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
# def update(id):
#     """Update a post if the current user is the author."""
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ? WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/update.html', post=post)


# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
#     """Delete a post.
#     Ensures that the post exists and that the logged in user is the
#     author of the post.
#     """
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('blog.index'))