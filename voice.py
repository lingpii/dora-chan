import speech_recognition as sr
from vieneu import Vieneu
import pygame
import os
import tempfile 
import re
class Speech_Recognition(): 
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts = Vieneu(mode="turbo")
        self.voice = self.tts.get_preset_voice("Thục Đoan (Nữ - Miền Nam)")
    def listen(self): 
        try: 
            with self.microphone as source: 
                print("Dora nghe nè")
                audio = self.recognizer.listen(source)
            text = self.recognizer.recognize_google(audio, language = "vi-VN")
            return text
        except sr.UnknownValueError: 
            return f"Dora-chan hem nghe rõ. Bạn nói lại giúp Dora nhé."
        except sr.RequestError: 
            return f"Dora-chan mất kết nối với bạn rồi..."
    def clean_text(self,text): 
        text = re.sub(r'\*\*', '', text)
        text = re.sub(r'\*', '', text)
        text = re.sub(r'\(.*?\)', '', text)
        text = re.sub(r'\#','',text)
        text = re.sub(r'^\-\s*','',text)
        return text
    def speak(self,text):
        text = self.clean_text(text)
        audio = self.tts.infer(text=text,voice = self.voice)
        self.tts.save(audio,"dora_response.wav")
        #playing
        pygame.mixer.init()
        pygame.mixer.music.load("dora_response.wav")
        pygame.mixer.music.play()
        #done playing 
        while pygame.mixer.music.get_busy(): 
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()
    def generate_wav(self, text):
        text = self.clean_text(text)
        audio = self.tts.infer(text=text, voice=self.voice)
        self.tts.save(audio, "dora_response.wav")
        return "dora_response.wav"