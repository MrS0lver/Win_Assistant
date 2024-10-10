import speech_recognition as sr
import requests,pyttsx3,pickle,time,requests as rq
from AppOpener import open,close

class Main:
    def __init__(self):
        try:
                with open("info.txt","rb") as file:
                        self.data = pickle.load(file)
                        print(self.data["Assist_name"])
        except Exception as e:
             print("Try AGain!")
    def say(self,x):
        engine = pyttsx3.init()
        engine.setProperty("rate","145")
        engine.say(x)
        engine.runAndWait()
    def listen(self):
        url = "https://www.google.com"
        resp = rq.get(url)
        if resp.status_code == 200:
            rec = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                rec.adjust_for_ambient_noise(source)
                audio = rec.listen(source)
                try:
                    print("Recognizing...")
                    data = rec.recognize_google(audio)
                    print(data)
                    return data.lower() 
                except Exception as e:
                    print("SOMETHING WENT WRONG!!!")
                    return ""  
        else:
            print("No Internet Connection!!!")
            pass
    def background_listen(self):
        call_name = self.data["Assist_name"].lower()  
        while True:
            listening = self.listen()  
            if call_name in listening:  
                    self.say(f"Hi {self.data["User_name"]}, Nice To Meet You! How Can I help you today!")
                    self.listen_for_commands()  #Greeting
            else:
                    pass
    def listen_for_commands(self):
        while True:
            listening = self.listen()  # Listening ...
            if "whatsapp" in listening:
                try:
                    self.say("Got it Sir!! Opening WhatsApp now.")
                    open("WhatsApp")
                except Exception as e:
                    self.say("WhatsApp is not available on your computer!")
            
            elif "time" in listening:
                try:
                    current_time = f"The time is {time.strftime('%I:%M %p')}"  # Correct time format
                    self.say(current_time)
                except Exception as e:
                    pass
            
            else:
                print("Command not recognized, continue listening...")

call_assist = Main()
call_assist.background_listen()

