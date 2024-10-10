from tkinter import *
from tkinter import messagebox
import os,sys,pyttsx3,pickle,requests,subprocess,shutil
import threading as tr

class Main:
    def say(self, x):
        network = requests.get("https://www.google.com")
        if network.status_code == 200:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 145)
            self.engine.say(x)
            self.engine.runAndWait()
        else:
            print("No Internet Connection")
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
    def store_info(self):
        data = {"User_name":self.name.get(),"Assist_name":self.nick_name.get()}
        with open("info.txt","wb") as file:
            pickle.dump(data,file)
            
    # def use_info(self):
    #     with open("info.txt","rb") as file:
    #         data = pickle.load(file)
    #         return data["User_name"],data["Assist_name"]
        
    def initialize(self):
        if not self.name.get().strip() or not self.nick_name.get().strip():
            messagebox.showerror("Input Error", "Name and Nickname cannot be empty!")  
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
                self.store_info()
                self.button.config(text="Initialized!")
                self.say(f"Hello, My name is {self.nick_name.get()}, Program Initialized successfully!")
                # tr.Thread(target=self.background_listen, daemon=True).start()  
                subprocess.Popen(["pythonw", "background.pyw"])
                self.root.destroy()
            except Exception as e:
                print("Something is Wrong Inside!")
                print(e)

if __name__ == "__main__":
    win = Tk()
    obj = Main(win)
    win.mainloop()

