from chat import DoraChat
from search import ans_questions
from intent import detect_intent
from voice import Speech_Recognition
dora_voice = Speech_Recognition()
dora = DoraChat()
try: 
    mode = ["text","voice"]
    print("Bạn muốn chat với Dora hay muốn trò chuyện cùng tớ? ")
    option = int(input("Chọn 1.text hoặc 2.voice "))
    while True:
        if option == 1: 
            user_input = input("")
            if user_input == "": 
                continue
            choose = detect_intent(user_input)
            if choose == "search": 
                answer = "\n".join(ans_questions(user_input))
                prompt = f"Từ câu hỏi của Chi: {user_input}. Đây là kết quả Dora tìm kiếm được:\n{answer}"
                print(dora.chat(prompt))
            else: print(dora.chat(user_input))
        elif option == 2: 
            user_text = dora_voice.listen()
            choose = detect_intent(user_text)
            if choose == "search": 
                answer = "\n".join(ans_questions(user_text))
                prompt = f"Từ câu hỏi của Chi: {user_text}. Đây là kết quả Dora tìm kiếm được:\n{answer}"
                response = dora.chat(prompt)
            else: 
                response = dora.chat(user_text)
            print(response)
            dora_voice.speak(response)
except KeyboardInterrupt: #Ctrl+C để thoát 
    print("Dora is offline")
    quit()