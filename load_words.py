from website import create_app, db
from website.models import ChineseWord
import json

app = create_app()

print("🐉 Loading Chinese words...")  # Add this at the top


with app.app_context():
    db.drop_all()
    db.create_all()


    with open('website/static/data/hsk1_sample.json', encoding='utf-8') as f:
       words = json.load(f)


    for entry in words:
        word = ChineseWord(**entry)
        db.session.add(word)

    db.session.commit()
    print("✅ Seeded ChineseWord table with sample data.")
