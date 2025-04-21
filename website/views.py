from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import ChineseWord, KnownWord, CustomWord, User
from . import db
import requests
import json
import os
from urllib.parse import quote
from .models import ChineseWord

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
    words = ChineseWord.query.all()
    
    if search_term:
        # Fetch from Moedict API
        moedict_data = get_moedict_entry(search_term)
        if moedict_data:
            words.append(format_moedict_data(moedict_data))
    
    # Add audio URLs to all words
    for word in words:
        if isinstance(word, dict):
            word['audio'] = f"https://api.voicerss.org/?key=107f190147ab4b6e91fc3d620792254b&hl=zh-tw&src={quote(word['chinese'])}&c=MP3"
        else:
            word.audio = f"https://api.voicerss.org/?key=107f190147ab4b6e91fc3d620792254b&hl=zh-tw&src={quote(word.chinese)}&c=MP3"
            
    if current_user.is_authenticated:
        known_word_ids = {kw.word_id for kw in current_user.known_words}
    else:
        known_word_ids = set()


    return render_template('dictionary.html', words=words, known_word_ids=known_word_ids, user=current_user)


@views.route('/mark_known', methods=['POST'])
@login_required
def mark_known():
    data = request.get_json()
    word_id = data.get('word_id')

    if not word_id:
        return jsonify({'success': False, 'message': 'No word ID provided'}), 400

    already_known = KnownWord.query.filter_by(user_id=current_user.id, word_id=word_id).first()

    if already_known:
        return jsonify({'success': True, 'message': 'Already known'})
    else:
        new_known = KnownWord(word_id=word_id, user_id=current_user.id)
        db.session.add(new_known)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Word saved'})


@views.route('/about')
def about():
    return render_template("about.html", user=current_user)


