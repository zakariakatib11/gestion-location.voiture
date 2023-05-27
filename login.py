import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from inventory import CarInventory
import mysql.connector

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

    def get_user_by_credentials(self, username, password):
        query = "SELECT * FROM users_table WHERE username = %s AND password = %s"
        values = (username, password)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Login Window")
        
        # Configure the style for the black theme
        style = ttk.Style()
        tk_font = ('TkDefaultFont', 17, 'bold')
        style.theme_use('clam')
        style.configure('TLabel', foreground='grey', background='#25212b')
        style.configure('TEntry', foreground='black', background='#25212b')
        style.configure('TButton', foreground='#e4deed', background='#25212b', font=("bold", 14))

        title_label = ctk.CTkLabel(master, text="LOGIN", font=ctk.CTkFont(size=50, weight="bold"))
        title_label.pack(padx=10, pady=(40, 20))

        self.username_label = ttk.Label(master, text="Username:", font=tk_font)
        self.username_label.pack(pady=(20, 5), padx=10)
        self.username_entry = ttk.Entry(master, width=30, font=("bold", 14))
        self.username_entry.pack(pady=20, padx=30)

        self.password_label = ttk.Label(master, text="Password:", font=tk_font)
        self.password_label.pack(pady=(10, 5), padx=10)
        self.password_entry = ttk.Entry(master, show="*", width=30, font=("bold", 14))
        self.password_entry.pack(pady=5, padx=10)

        self.login_button = ttk.Button(master, text="ENTER", command=self.login)
        self.login_button.pack(pady=27)

        self.db_manager = DatabaseManager()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.db_manager.get_user_by_credentials(username, password)
        
        if user:
            print("Login successful")
            self.open_car_inventory_window(None)
            
        else:
            tk.messagebox.showerror("Login Error", "Invalid credentials")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def open_car_inventory_window(self,event):
        # Destroy the login window and open the car inventory window
        self.master.destroy()
        root = tk.Tk()
        root.configure(background='#25212b')
        root.geometry('750x450')
        car_inventory = CarInventory(root)
        root.mainloop()
            
    def __del__(self):
        self.db_manager.close_connection()

if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='#25212b')
    root.geometry('750x450')
    login_window = LoginWindow(root)
    root.mainloop()
