
import speech_recognition as sr
import requests, pyttsx3, pickle, time, os
from AppOpener import open

class Main:
    def __init__(self):
        self.load_info()

    def load_info(self):
        if os.path.exists("info.txt"):
            try:
                with open("info.txt", "rb") as file:
                    self.data = pickle.load(file)
                print("Data loaded successfully:", self.data)
            except Exception as e:
                print(f"Error loading file: {e}")
                self.data = None
        else:
            print("File Not Exist!!")

    def say(self, x):
        engine = pyttsx3.init()
        engine.setProperty("rate", 145)
        engine.say(x)
        engine.runAndWait()

    def listen(self):
        url = "https://www.google.com"
        try:
            resp = requests.get(url)
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
                    except sr.UnknownValueError:
                        print("Google Speech Recognition could not understand audio")
                    except sr.RequestError as e:
                        print(f"Could not request results from Google Speech Recognition service; {e}")
            else:
                print("No Internet Connection!!!")
        except requests.ConnectionError:
            print("No Internet Connection!!!")
        return ""

    def background_listen(self):
        if self.data:
            self.say("I am running sir")
            call_name = self.data["Assist_name"].lower()
            while True:
                listening = self.listen()
                if call_name in listening:
                    self.say(f"Hi {self.data['User_name']}, Nice To Meet You! How Can I help you today!")
                    self.listen_for_commands()
        else:
            print("No data loaded. Please run the Entry.pyw file first.")

    def listen_for_commands(self):
        while True:
            listening = self.listen()
            if "whatsapp" in listening:
                try:
                    self.say("Got it Sir!! Opening WhatsApp now.")
                    open("WhatsApp")
                except Exception as e:
                    self.say("WhatsApp is not available on your computer!")
            elif "time" in listening:
                try:
                    current_time = f"The time is {time.strftime('%I:%M %p')}"
                    self.say(current_time)
                except Exception as e:
                    print(f"Error getting time: {e}")
            elif "exit" in listening or "quit" in listening:
                self.say("Goodbye!")
                break
            else:
                print("Command not recognized, continue listening...")

if __name__ == "__main__":
    main_obj = Main()
    main_obj.background_listen()