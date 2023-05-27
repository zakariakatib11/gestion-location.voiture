import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import os

def open_signup():
    os.system('python signup.py')

def open_login():
    os.system('python login.py')

window = tk.Tk()
window.title("Sign Up / Login")
window.geometry("400x200")

style = ThemedStyle(window)
style.set_theme("equilux")

title_label = ttk.Label(window, text="Welcome!", font=("Helvetica", 20))
title_label.pack(pady=20)
title_label.configure(background="#25212b")

buttons_frame = ttk.Frame(window)
buttons_frame.pack()

signup_button = ttk.Button(buttons_frame, text="Sign Up", command=open_signup)
signup_button.pack(side="left", padx=10, pady=10)

login_button = ttk.Button(buttons_frame, text="Login", command=open_login)
login_button.pack(side="left", padx=10, pady=10)

window.configure(background='#25212b')
window.geometry('400x200')
window.mainloop()
