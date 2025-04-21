from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import ChineseWord, KnownWord, CustomWord, User
from . import db
import requests
import json
import os
from urllib.parse import quote

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

    return render_template("home.html", demonstrator=demonstrator, user=current_user)



@views.route('/contact')
def contact():
    # Dynamic data
    people = [
        {"name": "Lauren Koch", "email": "lrkc1756@umwelt-campus.de", "description": "Developer", "image": "lauren.png", "tel": "+49 45758 8383"},
    ]
    return render_template("contact.html", people=people, user=current_user)


def load_sample_data():
    return [
        {
            "chinese": "蘋果",
            "pinyin": "píngguǒ",
            "english": "apple",
            "part_of_speech": "noun",
            "audio": "https://www.moedict.tw/音檔/%E8%98%8B%E6%9E%9C.mp3",
            "image": "https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg"
        }
    ]
    
    
@views.route('/dictionary', methods=['GET', 'POST'])
def dictionary():
    # Try to fetch from Moedict API first
    search_term = request.args.get('search', '')
    words = []
    
    if search_term:
        # Fetch from Moedict API
        moedict_data = get_moedict_entry(search_term)
        if moedict_data:
            words.append(format_moedict_data(moedict_data))
    else:
        # Fallback to sample data
        words = load_sample_data()
    
    # Add audio URLs to all words
    for word in words:
        word['audio'] = f"https://api.voicerss.org/?key=107f190147ab4b6e91fc3d620792254b&hl=zh-tw&src={quote(word['chinese'])}&c=MP3"
    
    return render_template('dictionary.html', words=words, user=current_user)


@views.route('/about')
def about():
    return render_template("about.html", user=current_user)


