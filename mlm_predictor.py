class ChineseMLMPredictor:
    # ... (keep existing __init__ and predict_masked_words methods)
    
    def predict_for_sentence_frame(self, frame, known_words):
        """Predict multiple masked positions in a sentence frame"""
        predictions = {}
        
        while "[MASK]" in frame:
            # Get predictions for the first mask found
            mask_pos = frame.find("[MASK]")
            temp_frame = frame[:mask_pos] + "[MASK]" + frame[mask_pos+6:]
            
            word_predictions = self.predict_masked_words(temp_frame, known_words, top_k=5)
            if word_predictions:
                predictions[mask_pos] = [word for word, score in word_predictions][:3]
            
            # Replace this mask to predict next one
            frame = frame.replace("[MASK]", word_predictions[0][0], 1)
        
        return predictions