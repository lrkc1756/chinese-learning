import json
from website import create_app, db
from website.models import Word

app = create_app()

with app.app_context():
    with open('website/static/data/hsk1_sample.json', encoding='utf-8') as f:
        data = json.load(f)
        for entry in data:
            # Check if the word already exists (prevent duplicates)
            existing = Word.query.filter_by(chinese=entry['chinese']).first()
            if not existing:
                word = Word(
                    chinese=entry['chinese'],
                    pinyin=entry['pinyin'],
                    english=entry['english'],
                    part_of_speech=entry['part_of_speech'],
                    image=entry['image'],
                    audio=entry['audio']
                )
                db.session.add(word)

        db.session.commit()
        print("✅ HSK words loaded!")
