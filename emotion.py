import re

def extract_emotion(response_text):
    match = re.search(r'\[EMOTION:(\w+)\]', response_text)
    if match:
        emotion = match.group(1).lower()
        if emotion in ("happy", "sad", "angry", "excited", "neutral"):
            return emotion
    return "neutral"

def strip_emotion_tag(response_text):
    return re.sub(r'\s*\[EMOTION:\w+\]', '', response_text).strip()

# fallback keyword detect (dùng khi không có tag)
def detect_emotion(user_input):
    text = user_input.lower()
    happy_words = ["thích", "dễ thương", "hihi", "hehe", "vui", "hạnh phúc", "tuyệt vời", "hớn hở"]
    sad_words = ["tội", "tiếc", "nhớ", "buồn", "thất vọng", "đau lòng"]
    angry_words = ["tức giận", "giận dỗi", "hờn", "quá đáng", "bực", "ghét", "chán", "phiền"]
    excited_words = ["quào", "wow", "quá xá đã", "thật bất ngờ", "không thể tin", "omg"]
    if any(w in text for w in excited_words): return "excited"
    elif any(w in text for w in happy_words): return "happy"
    elif any(w in text for w in sad_words): return "sad"
    elif any(w in text for w in angry_words): return "angry"
    else: return "neutral"
