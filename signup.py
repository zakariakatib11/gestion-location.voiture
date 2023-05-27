import tkinter as tk
import tkinter.ttk as ttk
import mysql.connector
import customtkinter as ctk
from login import LoginWindow

class DatabaseManager:
    def __init__(self):
        # Establish a connection to the MySQL database
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="users"
        )
        self.cursor = self.connection.cursor()
        
        if self.connection.is_connected():
         print("Connected to the database!")
        else:
         print("Failed to connect to the database!")

    def execute_query(self, query, values=None):
        self.cursor.execute(query, values)
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

class SignupWindow:
    def __init__(self, master):
        self.master = master
        self.db_manager = DatabaseManager()
        master.title("Signup Window")

        # Configure the style for the black theme
        style = ttk.Style()
        tk_font = ('TkDefaultFont', 17, 'bold')
        style.theme_use('clam')
        style.configure('TLabel', foreground='grey', background='#25212b')
        style.configure('TEntry', foreground='black', background='#25212b')
        style.configure('TButton', foreground='#e4deed', background='#25212b', font=("bold", 14))

        title_label = ctk.CTkLabel(root, text="SIGN UP", font=ctk.CTkFont(size=50, weight="bold"))
        title_label.pack(padx=10, pady=(40, 20))

        self.username_label = ttk.Label(master, text="Username:", font=tk_font)
        self.username_label.pack(pady=(20, 5), padx=10)
        self.username_entry = ttk.Entry(master, width=30, font=("bold", 14))
        self.username_entry.pack(pady=20, padx=30)
        
        self.password_label = ttk.Label(master, text="Password:", font=tk_font)
        self.password_label.pack(pady=(10, 5), padx=10)
        self.password_entry = ttk.Entry(master, show="*", width=30, font=("bold", 14))
        self.password_entry.pack(pady=5, padx=10)
        
        self.show_password_button = ttk.Button(master, text="𓏗", command=self.toggle_password_visibility)
        self.show_password_button.pack(pady=5, padx=10)
        self.show_password_button.config(width=1, padding=1)


        self.retype_password_label = ttk.Label(master, text="Retype Password:", font=tk_font)
        self.retype_password_label.pack(pady=(10, 5), padx=10)
        self.retype_password_entry = ttk.Entry(master, show="*", width=30, font=("bold", 14))
        self.retype_password_entry.pack(pady=5, padx=10)

        self.signup_button = ttk.Button(master, text="SIGN UP", command=self.signup)
        self.signup_button.pack(pady=27)
        
        label1 = ctk.CTkLabel(master, text="Already have an account?", font=tk_font, text_color='#bfbfbf')
        label1.pack(pady=2)
        login_label = ctk.CTkLabel(master, text="Log in", font=tk_font, underline=0, text_color='#e4deed')
        login_label.pack(pady=0)
        login_label.bind('<Button-1>', self.open_login_window)

    def toggle_password_visibility(self):
      if self.password_entry.cget('show') == '*':
          self.password_entry.config(show='')
          self.retype_password_entry.config(show='')
      else:
          self.password_entry.config(show='*')
          self.retype_password_entry.config(show='*')
          
    def signup(self):
      username = self.username_entry.get()
      password = self.password_entry.get()
      retype_password = self.retype_password_entry.get()
      
      # Check for errors  
      errors = []
      if not username:
          errors.append("Username is required.")
      if not password:
          errors.append("Password is required.")
      elif len(password) < 8:
          errors.append("Password must be at least 8 characters.")
      if not retype_password:
          errors.append("Retype Password is required.")
      elif retype_password != password:
          errors.append("Passwords do not match.")

      if errors:
          error_message = "\n".join(errors)
          tk.messagebox.showerror("Signup Error", error_message)
          self.username_entry.delete(0, tk.END)
          self.password_entry.delete(0, tk.END)
          self.retype_password_entry.delete(0, tk.END)
      else:
          #No errors, store username and password in the database
          query = "INSERT INTO users_table (username, password) VALUES (%s, %s)"
          values = (username, password)
          self.db_manager.execute_query(query, values)
          self.db_manager.close_connection()

          self.open_login_window(None)


    def open_login_window(self, event):
        self.master.destroy()
        root = tk.Tk()
        root.configure(background='#25212b')
        root.geometry('750x450')
        login_window = LoginWindow(root)
        root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='#25212b')
    root.geometry('850x600')
    signup_window = SignupWindow(root)
    root.mainloop()
