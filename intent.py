from chat import DoraChat
from search import ans_questions


question_words = ["thời tiết","giá", "tin tức", "hôm nay", "mới nhất","tốt nhất", "nên mua", "review", "có nên",
                  "ở đâu", "gần đây", "địa chỉ", "tra cứu", "tìm kiếm","hỏi google", "hỏi gg", "tra gg", "tra google"]
def detect_intent(text): 
    if any( kw in text for kw in question_words): 
        detect = "search"
    else: 
        detect = "chat"
    return detect