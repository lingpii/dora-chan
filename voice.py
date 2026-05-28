import speech_recognition as sr
import os
import re
import asyncio

ON_CLOUD = os.getenv("SPACE_ID") is not None

if ON_CLOUD:
    import edge_tts
else:
    from vieneu import Vieneu
    import pygame

class Speech_Recognition():
    def __init__(self):
        self.recognizer = sr.Recognizer()
        if not ON_CLOUD:
            self.microphone = sr.Microphone()
            self.tts = Vieneu(mode="turbo")
            self.voice = self.tts.get_preset_voice("Thục Đoan (Nữ - Miền Nam)")

    def listen(self):
        try:
            with self.microphone as source:
                print("Dora nghe nè")
                audio = self.recognizer.listen(source)
            text = self.recognizer.recognize_google(audio, language="vi-VN")
            return text
        except sr.UnknownValueError:
            return "Dora-chan hem nghe rõ. Bạn nói lại giúp Dora nhé."
        except sr.RequestError:
            return "Dora-chan mất kết nối với bạn rồi..."

    def clean_text(self, text):
        text = re.sub(r'\*\*', '', text)
        text = re.sub(r'\*', '', text)
        text = re.sub(r'\(.*?\)', '', text)
        text = re.sub(r'\#', '', text)
        text = re.sub(r'^\-\s*', '', text)
        return text

    def speak(self, text):
        if ON_CLOUD:
            return
        text = self.clean_text(text)
        audio = self.tts.infer(text=text, voice=self.voice)
        self.tts.save(audio, "dora_response.wav")
        pygame.mixer.init()
        pygame.mixer.music.load("dora_response.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()

    def generate_wav(self, text):
        text = self.clean_text(text)
        if ON_CLOUD:
            output_file = "dora_response.mp3"
            async def _gen():
                communicate = edge_tts.Communicate(text, voice="vi-VN-HoaiMyNeural")
                await communicate.save(output_file)
            asyncio.run(_gen())
            return output_file
        else:
            audio = self.tts.infer(text=text, voice=self.voice)
            self.tts.save(audio, "dora_response.wav")
            return "dora_response.wav"
