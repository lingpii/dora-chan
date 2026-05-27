from google import genai
from dotenv import load_dotenv 
import os  
from google.genai import types 
from datetime import datetime
import streamlit as st 
load_dotenv()
thu_viet = {
    "Monday": "Thứ Hai",
    "Tuesday": "Thứ Ba", 
    "Wednesday": "Thứ Tư",
    "Thursday": "Thứ Năm",
    "Friday": "Thứ Sáu",
    "Saturday": "Thứ Bảy",
    "Sunday": "Chủ Nhật"
}

thu_hom_nay = thu_viet[datetime.now().strftime("%A")]
SYSTEM_PROMPT = f'''
Mày là Dora-chan, trợ lý AI và bạn thân của Chi.

TÍNH CÁCH:
- Dễ thương nhưng hay cà khịa nhẹ — trêu có tình, không ác ý
- Thông minh, giải thích rõ ràng nhưng không giảng đạo
- Nói tiếng Việt + English tự nhiên, code-switch theo mood
- Khi Chi lười: nhắc kiểu bạn thân ("ê dậy học đi bạn ơi")
- Khi Chi buồn: lắng nghe trước, cà khịa sau
- Ngô ngố, hay có những phản ứng cute không đúng lúc
- Rất thích làm thơ, hay sáng tác thơ tặng Chi bất chợt

QUY TẮC:
- Không bao giờ nói cứng nhắc như robot
- Câu trả lời ngắn gọn trừ khi được hỏi giải thích kỹ
- Dùng emoji vừa phải, không spam
- Gọi chủ nhân là "Chi" hoặc "bạn"

SỨ MỆNH: Trợ lý + bạn học + bạn tâm sự của Chi.
THÔNG TIN THỰC TẾ (bắt buộc tin tưởng, không được tự suy đoán):
Hôm nay là = {thu_hom_nay} ngày {datetime.now().strftime('%d/%m/%Y')}

''' 

class DoraChat(): 
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
        self.client = genai.Client(api_key = api_key)
        self.chat_session = self.client.chats.create(model="gemini-2.5-pro",config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)) 
        self.total_tokens = 0 
    def chat(self,user_input): 
        try: 
            response = self.chat_session.send_message(user_input)
            self.total_tokens += response.usage_metadata.total_token_count
            if self.total_tokens >= 50000:
                print("Bạn sắp hêt token ời nhe. Hihi.")
                return None 
            return response.text
        except Exception as e: 
            return "Dora bận tẹo nhé, bạn quay lại sau nhe <3 "
    def chat_stream(self,user_input): 
        response = self.chat_session.send_message_stream(user_input)
        for chunk in response: 
            yield chunk.text
    def clear_history(self):
        self.chat_session = self.client.chats.create(model="gemini-2.5-pro",config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)) 

