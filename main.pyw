from tkinter import *
from PIL import Image, ImageTk
import webbrowser
import shutil
import os
import sys
import pyttsx3
import speech_recognition as sr
import threading as tr
from tkinter import messagebox

class Main:
    def say(self, x):
        self.engine = pyttsx3.init()
        self.engine.getProperty("rate")
        self.engine.setProperty("rate", 155)
        self.engine.say(x)
        self.engine.runAndWait()

    def __init__(self, root):
        self.root = root
        self.root.title("Login .")
        self.root.geometry("500x400")

        self.intro = Label(self.root, text=" Let's Start ", font="cambria 25", bg="lightgrey", relief=RIDGE)
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

        self.frame_1 = Frame(self.root, relief=RAISED, bg="lightgrey")
        self.frame_1.pack(side=BOTTOM, fill=BOTH)

        self.tell = Label(self.frame_1, text="Follow Me On :", font="cambria 20", bg="lightgrey")
        self.tell.grid(column=0, row=0, padx=1, pady=1)

        # Twitter
        image = Image.open("twitter.png")
        resized_image0 = image.resize((50, 50), Image.LANCZOS)
        self.twitter_img = ImageTk.PhotoImage(resized_image0)
        
        self.twitter = Button(self.frame_1, text="Twitter", bg="lightgrey", image=self.twitter_img, bd=0, 
                              command=lambda: webbrowser.open("https://x.com/Mrs0lver"))
        self.twitter.grid(column=1, row=0, padx=2, pady=2)

        # YouTube
        image = Image.open("youtube.png")
        resized_image1 = image.resize((50, 50), Image.LANCZOS)
        self.youtube_img = ImageTk.PhotoImage(resized_image1)
        
        self.youtube = Button(self.frame_1, text="YouTube", bg="lightgrey", image=self.youtube_img, bd=0, 
                              command=lambda: webbrowser.open("https://www.youtube.com/@Mrs0lver"))
        self.youtube.grid(column=2, row=0, padx=2, pady=2)

        # GitHub 
        image = Image.open("github.png")
        resized_image2 = image.resize((60, 60), Image.LANCZOS)
        self.github_img = ImageTk.PhotoImage(resized_image2)
        
        self.github = Button(self.frame_1, text="GitHub", bg="lightgrey", image=self.github_img, bd=0, command=lambda: webbrowser.open("https://github.com/MrS0lver"))
        self.github.grid(column=3, row=0, padx=2, pady=2)

        self.button = Button(self.root, text="Initilize", font="Georgia 20", bd=2, relief=GROOVE, bg="lightcyan", command=self.initilize)
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
                return data
            except Exception as e:
                print("SOMETHING WENT WRONG!!!")
    def background_listen(self):
        call_name = self.nick_name.get().title() # Lowercase to handle case insensitivity
        while True:
            listening = self.listen()  # Capture speech and convert to lowercase
            if call_name in listening:
                self.say(f"Hi {self.name.get()}, Nice To Meet You!, How Can I help you Today!")



    def initilize(self):
        if not self.name.get().strip() or not self.nick_name.get().strip():
            messagebox.showerror("Input Error", "Name and Nickname cannot be empty!")  # Show error message
         # Exit the method to avoid further execution
        else:
            tr.Thread(target=self.inilize, daemon=True).start()  # Fix spelling to match the function name

    def inilize(self):
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
                # Start listening for the name in the background
                # tr.Thread(target=self.background_listen,daemon=True).start()
                self.background_listen()
            except Exception as e:
                print("Something is Wrong Inside!")
                print(e)


if __name__ == "__main__":
    win = Tk()
    obj = Main(win)
    win.mainloop()

