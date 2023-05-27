import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def fetch_cars_data(self):
        #Establish a connection to the MySQL database
        cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        cursor = cnx.cursor()

        query = "SELECT * FROM cars"

        cursor.execute(query)

        rows = cursor.fetchall()

        cursor.close()
        cnx.close()

        cars = []
        for row in rows:
            car = {
                "mark": row[1],
                "model": row[2],
                "year": row[3],
                "type of carburetor": row[4],
                "number of places": row[5],
                "transmission": row[6],
                "price of location per day": row[7],
                "availability": row[8],
                "image": row[9]
            }
            cars.append(car)

        return cars


class CarInventory:
    def __init__(self, master):
        self.master = master
        master.title("Car Inventory")
        self.master = master
        master.geometry('1200x800')
        master.configure(bg='#0e0e0e')
        # Create a DatabaseManager instance
        db_manager = DatabaseManager(host="localhost", user="root", password="", database="carinventory")

        # Configure the style for the black theme
        style = ttk.Style()
        tk_font = ('TkDefaultFont', 17, 'bold')
        style.theme_use('clam')
        style.configure('TLabel', foreground='grey', background='#0e0e0e')
        style.configure('TEntry', foreground='black', background='#25212b')
        style.configure('TButton', foreground='black', background='white',font=("bold", 14))
        
        style.configure('Car.TFrame', foreground='white', background='#070707', bordercolor='#3d3c42', relief='groove')
        style.map('Car.TFrame', background=[('active', '#3d3c42'), ('disabled', '#2c2b31')])

        
        title_img = Image.open('3d_title.png')
        title_photo = ImageTk.PhotoImage(title_img)
        
        title_label = tk.Label(master, image=title_photo, background='#0e0e0e')
        title_label.image = title_photo
        title_label.pack(padx=10, pady=(40, 20))
        
        self.search_frame = ttk.Frame(master, style='Car.TFrame')
        self.search_frame.pack(side=tk.TOP, fill=tk.X, padx=200, pady=(40, 10))

        self.search_entry = ttk.Entry(self.search_frame, width=40, font=("bold", 14))
        self.search_button = ttk.Button(self.search_frame, text="Search", style="TButton",command=self.search_cars)

        # Pack the widgets horizontally in the search frame
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=1)
        self.search_button.pack(side=tk.RIGHT, padx=0, pady=1)
       
       # Create a list of car attributes to search by
        car_attributes = ['ShowAll','Mark', 'Type of carburetor', 'Number of places', 'Transmission', 'Price of location per day']

        # Create a label and combobox widget for the dropdown list
        search_label = ttk.Label(self.search_frame, text="Search by:", style="TLabel")
        self.search_attribute = ttk.Combobox(self.search_frame, values=car_attributes, state='readonly', font=("bold", 14))

        # Pack the widgets horizontally in the search frame
        search_label.pack(side=tk.LEFT, padx=5, pady=1)
        self.search_attribute.pack(side=tk.LEFT, padx=5, pady=1)

   
        # Create car cards
        self.car_frame = ttk.Frame(master)
        self.car_frame.pack(fill=tk.BOTH, padx=50, pady=10)
        
        # Create a canvas and scrollbar
        self.canvas = tk.Canvas(master, width=1000, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        # Create car frame inside the canvas
        self.car_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.car_frame, anchor='nw')

        self.cars = db_manager.fetch_cars_data()



        # Create container frame for car groups
        self.group_container = ttk.Frame(self.car_frame)
        self.group_container.pack(fill=tk.BOTH, padx=140, pady=50)
        # Center the container frame
        container_width = 1200
        container_height = 600
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = (screen_width // 2) - (container_width // 2)
        y = (screen_height // 2) - (container_height // 2)
        master.geometry(f"{container_width}x{container_height}+{x}+{y}")


        self.group_frame = None
        self.card_count = 0
        
        for car in self.cars:
            # Check if we need to create a new group frame
            if self.card_count % 3 == 0:
                self.group_frame = ttk.Frame(self.group_container)
                self.group_frame.pack(side=tk.TOP, fill=tk.BOTH)

            car_card = ttk.Frame(self.group_frame, borderwidth=2, relief="groove", style='Car.TFrame')
            car_card.pack(side=tk.LEFT, padx=20, pady=20)

            image = tk.PhotoImage(file=car["image"])
            car_image = ttk.Label(car_card, image=image)
            car_image.image = image  # Keep a reference to the image
            car_image.pack(pady=10)

            mark_model_year = f"{car['mark']} {car['model']} ({car['year']})"
            car_mark_model_year = ttk.Label(car_card, text=mark_model_year, font=tk_font)
            car_mark_model_year.pack(pady=10)

            car_price = ttk.Label(car_card, text=car["price of location per day"], font=tk_font)
            car_price.pack(pady=10)

            car_info = f"Carburetor: {car['type of carburetor']}\nSeats: {car['number of places']}\nTransmission: {car['transmission']}\nAvailability: {car['availability']}"
            car_details = ttk.Label(car_card, text=car_info, font=("Helvetica", 14))
            car_details.pack(pady=10)

            self.card_count += 1

        
        # Check if there are any remaining cards
        if self.card_count % 3 != 0:
            self.group_frame = ttk.Frame(self.group_container)
            self.group_frame.pack(side=tk.TOP, fill=tk.BOTH)
            
    def search_cars(self):
        tk_font = ('TkDefaultFont', 17, 'bold')
        search_term = self.search_entry.get()
        selected_attribute = self.search_attribute.get()
        filtered_cars = []
        self.card_count = 0
    
        for car in self.cars:

            if selected_attribute == "Mark" and search_term.lower() in car["mark"].lower():
                filtered_cars.append(car)
            elif selected_attribute == "Transmission" and search_term.lower() in car["transmission"].lower():
                filtered_cars.append(car)
            elif selected_attribute == "Number of places" and search_term == car["number of places"]:
                filtered_cars.append(car)
            elif selected_attribute == "Type of carburetor" and search_term.lower() in car["type of carburetor"].lower():
                filtered_cars.append(car)
            elif selected_attribute == "Price of location per day" and search_term == car["price of location per day"]:
                filtered_cars.append(car)
            elif selected_attribute == "ShowAll":
                filtered_cars=self.cars
        print(f"selected: {selected_attribute}")
        print(f"Number of cars: {len(filtered_cars)}")   
             
        # Clear the existing car cards
        for child in self.car_frame.winfo_children():
            child.destroy()   

        # Create new car cards for the filtered cars
        if len(filtered_cars) > 0:
            self.group_container = ttk.Frame(self.car_frame)
            self.group_container.pack(fill=tk.BOTH, padx=140, pady=50)
            for car in filtered_cars:
                self.create_car_card(car, tk_font)
        else:
            no_results_text = ttk.Label(self.car_frame, text="No search results found !!", font=("bold", 17))
            no_results_text.place(relx=0.5, rely=0.1, anchor=tk.CENTER)


        self.search_entry.delete(0, tk.END)

    def create_car_card(self, car, tk_font):
        if self.card_count % 3 == 0:
            self.group_frame = ttk.Frame(self.group_container)
            self.group_frame.pack(side=tk.TOP, fill=tk.BOTH)

        car_card = ttk.Frame(self.group_frame, borderwidth=2, relief="groove", style='Car.TFrame')
        car_card.pack(side=tk.LEFT, padx=20, pady=20)

        image = tk.PhotoImage(file=car["image"])
        car_image = ttk.Label(car_card, image=image)
        car_image.image = image  # Keep a reference to the image
        car_image.pack(pady=10)

        mark_model_year = f"{car['mark']} {car['model']} ({car['year']})"
        car_mark_model_year = ttk.Label(car_card, text=mark_model_year, font=tk_font)
        car_mark_model_year.pack(pady=10)

        car_price = ttk.Label(car_card, text=car["price of location per day"], font=tk_font)
        car_price.pack(pady=10)

        car_info = f"Carburetor: {car['type of carburetor']}\nSeats: {car['number of places']}\nTransmission: {car['transmission']}\nAvailability: {car['availability']}"
        car_details = ttk.Label(car_card, text=car_info, font=("Helvetica", 14))
        car_details.pack(pady=10)
    
        self.card_count += 1
        
if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='#25212b')
    root.geometry('1040x900')
    car_inventory = CarInventory(root)
    root.mainloop()
