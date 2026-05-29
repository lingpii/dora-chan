from chat import DoraChat
from search import ans_questions
from intent import detect_intent
from voice import Speech_Recognition
from emotion import extract_emotion, strip_emotion_tag
from vtube import VTubeController
from lipsync import speak_with_lipsync
import asyncio
async def main(): 
    dora_voice = Speech_Recognition()
    dora = DoraChat()
    controller = VTubeController()
    await controller.connect()
    await controller.list_hotkeys()
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
                    response = dora.chat(prompt)
                else:
                    response = dora.chat(user_input)
                if not response:
                    continue
                emotion = extract_emotion(response)
                clean = strip_emotion_tag(response)
                print(clean)
                await controller.trigger_expression(emotion)
                wav_path = await asyncio.to_thread(dora_voice.generate_wav, clean)
                await speak_with_lipsync(wav_path, controller)
            elif option == 2:
                user_text = dora_voice.listen()
                choose = detect_intent(user_text)
                if choose == "search":
                    answer = "\n".join(ans_questions(user_text))
                    prompt = f"Từ câu hỏi của Chi: {user_text}. Đây là kết quả Dora tìm kiếm được:\n{answer}"
                    response = dora.chat(prompt)
                else:
                    response = dora.chat(user_text)
                if not response:
                    continue
                emotion = extract_emotion(response)
                clean = strip_emotion_tag(response)
                print(clean)
                await controller.trigger_expression(emotion)
                wav_path = await asyncio.to_thread(dora_voice.generate_wav, clean)
                await speak_with_lipsync(wav_path, controller)
    except KeyboardInterrupt:
        print("Dora is offline")
    finally:
        await controller.vts.close()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

