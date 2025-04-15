from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import ChineseWord, KnownWord, CustomWord, User
from . import db
import json
import os

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    demonstrator = [
        {"name": "LCA", "description": "...", "image": "lca.png"},
        # ... other items
    ]

    if request.method == 'POST': 
        word_id = request.form.get('word_id')  # Get the word ID from the form

        if not word_id:
            flash('No word selected!', category='error')
        else:
            already_known = KnownWord.query.filter_by(user_id=current_user.id, word_id=word_id).first()

            if already_known:
                flash('You already marked this word as known.', category='info')
            else:
                new_known = KnownWord(word_id=word_id, user_id=current_user.id)
                db.session.add(new_known)
                db.session.commit()
                flash('Word added to known words!', category='success')

    return render_template("dictionary.html", demonstrator=demonstrator, user=current_user)



@views.route('/contact')
def contact():
    # Dynamic data
    people = [
        {"name": "Lauren Koch", "email": "lrkc1756@umwelt-campus.de", "description": "Developer", "image": "lauren.png", "tel": "+49 45758 8383"},
    ]
    return render_template("contact.html", people=people, user=current_user)

@views.route('/dictionary')
def dictionary():
    json_path = os.path.join(os.path.dirname(__file__), 'static', 'data', 'hsk1_sample.json')
    with open(json_path, encoding='utf-8') as f:
        words = json.load(f)
    return render_template("dictionary.html", words=words, user=current_user)

@views.route('/about')
def about():
    return render_template("about.html", user=current_user)