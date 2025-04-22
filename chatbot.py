from mlm_predictor import ChineseMLMPredictor


class DynamicChineseChatBot:
    def __init__(self):
        self.mlm = ChineseMLMPredictor()
        self.sentence_frames = [
            "我[MASK][noun]。",
            "[noun][MASK]吗？",
            "这是[MASK][noun]。",
            "我想[MASK][noun]。",
            "[noun]很[MASK]。"
        ]
    
def generate_interactive_response(self, user_id):
    print(f"📥 Generating sentence for user {user_id}")
    
    known_words = self.get_known_words(user_id)
    print("✅ Known words:", known_words)
    
    known_by_type = self.get_known_words_by_type(user_id)
    print("✅ Known words by type:", known_by_type)
    
    # Check if we have any nouns
    if 'noun' not in known_by_type or not known_by_type['noun']:
        print("⚠️ No nouns found")
        return {
            "base_sentence": "我吃[MASK]",
            "predictions": {2: ["苹果", "米饭", "面包"]},
            "noun_used": None
        }

    frame = random.choice([f for f in self.sentence_frames if "[noun]" in f])
    noun = random.choice(known_by_type['noun'])
    frame = frame.replace("[noun]", noun)

    print("🧱 Frame:", frame)

    predictions = self.mlm.predict_for_sentence_frame(frame, known_words)
    print("🎯 Predictions:", predictions)

    return {
        "base_sentence": frame,
        "predictions": predictions,
        "noun_used": noun
    }
