from tkinter import *
import shutil
import os
import sys
import pyttsx3
import speech_recognition as sr
import threading as tr
from tkinter import messagebox
from AppOpener import open
import requests 

class Main:
    def say(self, x):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 155)
        self.engine.say(x)
        self.engine.runAndWait()

    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("500x400")

        self.intro = Label(self.root, text="Let's Start", font="cambria 25", bg="lightgrey", relief=RIDGE)
        self.intro.pack(fill=BOTH, pady=10)

        self.frame = Frame(self.root, relief=RAISED)
        self.frame.pack()

        self.label = Label(self.frame, text="Enter Your Name: ", font="consolas 15")
        self.label.grid(row=0, column=0, padx=3, pady=1)
        self.name = Entry(self.frame, font="consolas 15", bd=0, width=15, bg="lightgrey")
        self.name.grid(row=0, column=1, padx=3, pady=1)

        self.label_1 = Label(self.frame, text="Give me a Name: ", font="consolas 15")
        self.label_1.grid(row=1, column=0, padx=3, pady=1)
        self.nick_name = Entry(self.frame, font="consolas 15", bd=0, width=15, bg="lightgrey")
        self.nick_name.grid(row=1, column=1, padx=3, pady=1)

        self.button = Button(self.root, text="Initialize", font="Georgia 20", bd=2, relief=GROOVE, bg="lightcyan", command=self.initialize)
        self.button.pack()

    def listen(self):
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

    def background_listen(self):
        call_name = self.nick_name.get().lower()  
        while True:
            listening = self.listen()  
            if call_name in listening:  
                self.say(f"Hi {self.name.get()}, Nice To Meet You! How Can I help you today!")
                self.listen_for_commands()  #Greeting

    def listen_for_commands(self):
        while True:
            listening = self.listen()  #Listening ...
            if "whatsapp" in listening:
                self.say("Got it Sir!! Opening WhatsApp now.")
                open("WhatsApp")
                
            else:
                print("Command not recognized, continue listening...")  
    def initialize(self):
        if not self.name.get().strip() or not self.nick_name.get().strip():
            messagebox.showerror("Input Error", "Name and Nickname cannot be empty!")  
            return  
        else:
            tr.Thread(target=self.initialize_app, daemon=True).start()  

    def initialize_app(self):
        current_script_path = sys.argv[0]
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        destination = os.path.join(startup_folder, os.path.basename(current_script_path))
        
        if os.path.exists(destination):
            print("File Already Exists")
            os.remove(destination)
        else:
            try:
                shutil.copy(current_script_path, destination)
                print("File Copied Successfully")
                self.button.config(text="Initialized!")
                self.say(f"Hello, My name is {self.nick_name.get()}, Program Initialized successfully!")
                tr.Thread(target=self.background_listen, daemon=True).start()  
            except Exception as e:
                print("Something is Wrong Inside!")
                print(e)

if __name__ == "__main__":
    win = Tk()
    obj = Main(win)
    win.mainloop()

