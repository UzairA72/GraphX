import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
from main import main_screen
import bcrypt


client=MongoClient('')#removed mongodb client id for privacy, can create new via Atlas
db = client["users_database"]
collection=db["user"]
collection.create_index("username", unique=True)
teacher=False
window = tk.Tk()
window.title("GraphX")
window.geometry("600x300")

global userid
loggedinuser=("")




def hash_algorithm(password:str):
    password_bytes=password.encode('utf-8')
    salt=bcrypt.gensalt()
    hashed_password=bcrypt.hashpw(password_bytes,salt)

    return hashed_password.decode('utf-8')  #converts hashed password to string to be stored in mongodb


def initialise(firstname,lastname,username,password,role):

    if collection.find_one({"username":username}):
        tk.messagebox.showerror("Error","Username already exists")
    else:
        user_data = {"firstname":firstname, "lastname":lastname, "username":username, "password":hash_algorithm(password), "role":role}
    
        result=collection.insert_one(user_data)

        tk.messagebox.showinfo("Success","Account created successfully!")

        global loggedinuser
        
        loggedinuser=result.inserted_id

        print(loggedinuser)
        
        return True,loggedinuser

def user_authentication(inputted_username,inputted_password):
    
    user = collection.find_one({"username":inputted_username})

    if user:
        hashed_password=user["password"]
        if bcrypt.checkpw(inputted_password.encode('utf-8'),hashed_password.encode('utf-8')):
            tk.messagebox.showinfo("Success","Login successful!")
            global loggedinuser
            loggedinuser=user.get("_id")
            return True,loggedinuser

        else:
            if inputted_username=="" or inputted_password=="":
                tk.messagebox.showerror("Error", "Incomplete field(s)")
            else:
                if collection.find_one({"username":inputted_username}):
                    tk.messagebox.showerror("Error","Incorrect Password")
    else:
        if inputted_username=="" or inputted_password=="":
                tk.messagebox.showerror("Error", "Incomplete field(s)")
        else:
            tk.messagebox.showerror("Error","User Not Found")
        return False
 
def signup_page():  
    window.destroy() #closes original page after selecting sign-up


    def role_adapter():
        global teacher 
        teacher = True
        tk.messagebox.showinfo("Notification","Teacher access will be given after authorisation")


    signupwindow=tk.Tk()
    signupwindow.title("GraphX - Sign-Up Page")
    signupwindow.geometry("500x450")
    signupwindow.iconbitmap("logo.ico")

    title_login = tk.Label(signupwindow, text="Sign-Up", font =("Arial Bold", 18))
    title_login.pack(side="top", pady=20)

    role_button=tk.Button(signupwindow, text="Teacher?", font =("Arial Bold", 12), command=role_adapter)
    role_button.pack(side = "top", padx=10, anchor="nw")
                       

    input_frame=tk.Frame(signupwindow)  #input frame to better structure the fields 
    input_frame.pack(pady=0)

    tk.Label(input_frame, text="Firstname:", font =("Arial Bold", 16)).grid(row=0, column=0, padx=10, pady=10)
    firstname_entry = tk.Entry(input_frame)     
    firstname_entry.grid(row=0, column=1, padx=5, pady=5)


    tk.Label(input_frame, text="Lastname:", font =("Arial Bold", 16)).grid(row=1, column=0, padx=10, pady=10)
    lastname_entry = tk.Entry(input_frame)
    lastname_entry.grid(row=1, column=1, padx=5, pady=5)


    tk.Label(input_frame, text="Username:", font =("Arial Bold", 16)).grid(row=2, column=0, padx=10, pady=10)
    username_entry = tk.Entry(input_frame)
    username_entry.grid(row=2, column=1, padx=5, pady=5)
    

    tk.Label(input_frame, text="Password:", font =("Arial Bold", 16)).grid(row=3, column=0, padx=10, pady=10)
    password_entry = tk.Entry(input_frame, show="*")
    password_entry.grid(row=3, column=1, padx=5, pady=5)


    tk.Label(input_frame, text="Confirm Password:", font =("Arial Bold", 16)).grid(row=4, column=0, padx=10, pady=10)
    repassword_entry = tk.Entry(input_frame, show="*")
    repassword_entry.grid(row=4, column=1, padx=5, pady=5)

    def signup():
        role="Student"
        if teacher == True:
            role="Pending Verification"
        firstname= firstname_entry.get()
        lastname= lastname_entry.get()
        username= username_entry.get()
        password= password_entry.get()
        repassword=repassword_entry.get()
        if firstname=="" or lastname=="" or username=="" or password=="" or repassword=="":
            tk.messagebox.showerror("Error", "Incomplete fields")   #popup shown if form is incomplete
            return
        if len(password)>=8 and len(password)<=20:
            if len(username)>=6 and len(username)<=15:
                lowercase=False
                uppercase=False
                num=False
                special=False
                

                for character in password:
                    if(character.isdigit()):
                        num = True
                    if(character.islower()):
                        lowercase=True
                    if(character.isupper()):
                        uppercase=True
                    if(not character.isalnum()):
                        special=True

                if lowercase==True and uppercase==True and num==True and special==True:
                    if password == repassword:
                        if initialise(firstname,lastname,username,password,role):
                            signupwindow.destroy()
                            main_screen(loggedinuser)

                    else:
                        tk.messagebox.showerror("Error", "Passwords do not match")
                else:
                    tk.messagebox.showerror("Error", "Password must include lowercase, uppercase, number and special character")
            else:
                tk.messagebox.showerror("Error", "Username must be between 6-15 characters")
        else:
            tk.messagebox.showerror("Error", "Password must be between 8-20 characters")
            


    submit_buton= tk.Button(input_frame, text="Submit", font =("Arial Bold", 16), command=signup)    # trigger a corresponding function to process inputs
    submit_buton.grid(row=5, column=0, columnspan=2, pady=35)

    signupwindow.bind("<Return>", lambda event:signup() )


    signupwindow.mainloop()

def login_page():

    window.destroy() # closes original page after selecting log in
    
    loginwindow = tk.Tk()
    loginwindow.title("GraphX - Login Page")    # new page where login details are entered
    loginwindow.geometry("400x300")
    loginwindow.iconbitmap("logo.ico")

    title_login = tk.Label(loginwindow, text="Login", font =("Arial Bold", 18))
    title_login.pack(side="top", pady=20)
    
    input_frame=tk.Frame(loginwindow)
    input_frame.pack(pady=0)


    tk.Label(input_frame, text="Username:", font =("Arial Bold", 16)).grid(row=0, column=0, padx=30, pady=40)
    username_entry = tk.Entry(input_frame)     
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Password:", font =("Arial Bold", 16)).grid(row=1, column=0, padx=30, pady=1)
    
    password_entry = tk.Entry(input_frame, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    def login():
        inputted_username = username_entry.get()                                    # nested function to process login details
        inputted_password = password_entry.get()
        if user_authentication(inputted_username,inputted_password):
            loginwindow.destroy()
            main_screen(loggedinuser)

    submit_buton= tk.Button(input_frame, text="Submit", font =("Arial Bold", 16), command=login)    #triggers credential check to gain access
    submit_buton.grid(row=3, column=0, columnspan=2, pady=35)

    loginwindow.bind("<Return>", lambda event:login() ) #enter key as an alternative way to submit details

    loginwindow.mainloop()

welcome = tk.Label(window, text="Welcome to GraphX", font =("Arial Bold", 18))
welcome.pack(pady=(50,0))

login_page_button = tk.Button(window, text="Login", padx=90, font=("Arial",12), command = login_page)
login_page_button.pack(pady=30)

signup_page_button = tk.Button(window, text="Sign-up", padx=82, font=("Arial",12), command=signup_page)
signup_page_button.pack()



window.iconbitmap("logo.ico")

window.mainloop()


print(hash_algorithm("Password12!"))