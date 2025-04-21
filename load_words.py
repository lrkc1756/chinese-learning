from website import create_app, db
from website.models import ChineseWord

app = create_app()

print("🐉 Loading Chinese words...")  # Add this at the top


with app.app_context():
    db.drop_all()
    db.create_all()

    words = [
        {"chinese": "蘋果", "pinyin": "píngguǒ", "english": "apple", "part_of_speech": "noun"},
        {"chinese": "喜歡", "pinyin": "xǐhuān", "english": "to like", "part_of_speech": "verb"},
        {"chinese": "吃", "pinyin": "chī", "english": "to eat", "part_of_speech": "verb"},
        {"chinese": "書", "pinyin": "shū", "english": "book", "part_of_speech": "noun"},
        {"chinese": "學生", "pinyin": "xuéshēng", "english": "student", "part_of_speech": "noun"},
        {"chinese": "喝", "pinyin": "hē", "english": "to drink", "part_of_speech": "verb"},
        {"chinese": "漂亮", "pinyin": "piàoliang", "english": "beautiful", "part_of_speech": "adjective"},
        {"chinese": "快樂", "pinyin": "kuàilè", "english": "happy", "part_of_speech": "adjective"},
        {"chinese": "跑", "pinyin": "pǎo", "english": "to run", "part_of_speech": "verb"},
        {"chinese": "狗", "pinyin": "gǒu", "english": "dog", "part_of_speech": "noun"},
        # Add more here
    ]

    for entry in words:
        word = ChineseWord(**entry)
        db.session.add(word)

    db.session.commit()
    print("✅ Seeded ChineseWord table with sample data.")
