from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Note
import json
# standard routes - homepage, etc - creates a blueprint for views - flask app

views = Blueprint('views', __name__)


# define route with decorator - how pages defined in url - the home page

@views.route('/', methods=['GET', 'POST'])  # post method allowed for route
@login_required
def home():
    if request.method == 'POST': #check
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id) #add note
            db.session.add(new_note)
            db.session.commit()
            flash('Note is added!', category='success')

    return render_template("home.html", user=current_user)  # "<h1>Test</h1>" render template


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

