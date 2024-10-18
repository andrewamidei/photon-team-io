'''
The intention of this file is to serve as the ui library for Photon
Laser Tag software.

As of 9/13/2024 this module will run a simple splash screen and
display a entry terminal for use in setting up your game of laser
tag.
'''

import customtkinter as ctk
from PIL import Image
import time

# --- Modules ---
import database as db

from udp_client import send_udp_message

# Sets the appearance of the window
# Supported modes : Light, Dark, System
ctk.set_appearance_mode("Dark")   
# Sets the color of the widgets in the window
# Supported themes : green, dark-blue, blue    
ctk.set_default_color_theme("dark-blue")    

# Splash screen
SPLASH_SCREEN_DURATION = 5  # In seconds
SPLASH_SCREEN_LOCATION = "Images/logo.jpg"

# padding
COLUMN_PADDING = 0 # Standard padding used between entry boxes
ROW_PADDING = 20 # Standard padding used between entry boxes
ENTRY_ROW_PADDING = 5 # Standard padding for a entry box

# Entry placeholders
ID_PLACEHOLDER = 'ID'
CODENAME_PLACEHOLDER = 'Codename'
HARDWARE_ID_PLACEHOLDER = 'Hardware ID'
MAX_PLAYERS = 20 # max supported players on a team
ENTRY_SPAN = 2

# Orientation
COLUMN_SHIFT = 7
ID_ENTRY_COLUMN = 1
CODENAME_ENTRY_COLUMN = 3

# Game window
GAME_WINDOW_WIDTH = 586    # Dont touch unless necessary
GAME_WINDOW_HEIGHT = 445   # Dont touch unless necessary
GAME_WINDOW_NAME = "Photon Game Window"


# App Class
class PhotonGUI():
   # The layout of the window will be written
   # in the init function itself
   def __init__(self, window, *args, **kwargs):
       super().__init__(*args, **kwargs)

       # Creates splash screen that lasts the duration of the loading time
       logo_image = create_image(window, SPLASH_SCREEN_LOCATION, window.winfo_width(), window.winfo_height(), 0, 0) # Create the splash screen
       window.update() # Updates window
       
       # Stored data for red team
       self.id_entry_red = ['null'] * MAX_PLAYERS
       self.codename_entry_red = ['null'] * MAX_PLAYERS
       self.hardware_id_entry_red = ['null'] * MAX_PLAYERS
   
       # Stored data for green team
       self.id_entry_green = ['null'] * MAX_PLAYERS
       self.codename_entry_green = ['null'] * MAX_PLAYERS
       self.hardware_id_entry_green = ['null'] * MAX_PLAYERS

       create_entry_terminal(self, window)

       # create_game_action(self,window)

       logo_image.destroy()  # Delete the splash screen when ui is finished loading

# --- Functions ---
def create_entry_window(width, height, title):
   window = ctk.CTk()  # creates customtkinter object

   window.geometry(str(width) + "x" + str(height))   # sets pixel size of window to width x height
   window.title(title) # sets title of window to title

   center_window(window) # center the window

   return window

def submit(window):
   db.refreshDatabase(window, MAX_PLAYERS)

def create_image(window ,image_location, image_width, image_height, image_x, image_y):
   # Creates an image label object then displays image of size on window at location.
   # Inputs: window - customtkinter window object to display image on
   #         image_location - file location of image to be displayed
   #         image_width - width in pixels of the image
   #         image_height - height in pixels of the image
   #         image_x - x coordinate (in pixels) where upper left corner of image will be displayed relative to (0,0). Positive is right
   #         image_y - y coordinate (in pixels) where upper left corner of image will be displayed relative to (0,0). Positive is down
   # Outputs: label - CTkLabel object containing image and supporting info such as size and location
   
   image = ctk.CTkImage(light_image = Image.open(image_location), size = (image_width, image_height))  # Creates CTkImage object called "i" containing image file at location and size tuple
   label = ctk.CTkLabel(master = window, image = image, text = "") # Creates a label object used to display the image in the given window
   label.place(x = image_x, y = image_y)   # Moves the image to the x and y coordinates

   return label

def create_game_window(width, height, title):
   window = ctk.CTkToplevel()

   window.geometry(str(width) + "x" + str(height))   # sets pixel size of window to width x height
   window.title(title) # sets title of window to title

   center_window(window) # center the window

   background_image = create_image(window, "Images/background.tif", width, height, 0, 0)
   window.update() # Updates window

   for x in range(5, -1, -1):
      image = create_image(window, "Images/" + str(x) + ".tif", 246, 111, 171, 204)
      window.update() # Updates window

      time.sleep(1)

      image.destroy()

   background_image.destroy()

   # _________________________
   # countdown is over, so put the ui stuff here or the call to it

def create_entry_terminal(self, window):
   # allows for the dynamic scaling of all the rows as the window size is being changed
   # the plus 2 is needed to account for the submit button at the bottom of the screen
   for row in range(0, MAX_PLAYERS + 2):
       window.rowconfigure(row, weight=1)

   # allows for the dynamic scaling of all the columns as the window size is being changed
   for column in range(0, COLUMN_SHIFT+CODENAME_ENTRY_COLUMN+ENTRY_SPAN+2):
       window.columnconfigure(column, weight=1)

   # Red team title
   self.textbox = ctk.CTkLabel(window, text="Red Team", fg_color="transparent")
   self.textbox.grid(row=0, column=2, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

   # Green Team title
   self.textbox = ctk.CTkLabel(window, text="Green Team", fg_color="transparent")
   self.textbox.grid(row=0, column=2 + COLUMN_SHIFT, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

   # Loop through and create all entry points for the red team
   row = 0
   for row in range(MAX_PLAYERS):
       self.textbox = ctk.CTkLabel(window, text=row, fg_color="transparent")
       self.textbox.grid(row=row + 1, column=0, padx=ROW_PADDING, pady=COLUMN_PADDING , sticky="ew")

       # Displays the ID entry box
       self.id_entry_red[row] = ctk.CTkEntry(window, placeholder_text=ID_PLACEHOLDER)
       # Positions element in a grid
       self.id_entry_red[row].grid(row=row + 1, column=ID_ENTRY_COLUMN, columnspan=ENTRY_SPAN, padx=ENTRY_ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

       # Displays the Codename entry box              
       self.codename_entry_red[row] = ctk.CTkEntry(window, placeholder_text=CODENAME_PLACEHOLDER)
       # Positions element in a grid
       self.codename_entry_red[row].grid(row=row + 1, column=CODENAME_ENTRY_COLUMN, columnspan=ENTRY_SPAN, padx=ENTRY_ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

       # Displays the Hardware ID entry box
       self.hardware_id_entry_red[row] = ctk.CTkEntry(window, placeholder_text=HARDWARE_ID_PLACEHOLDER)
       # Positions element in a grid
       self.hardware_id_entry_red[row].grid(row=row + 1, column=CODENAME_ENTRY_COLUMN + 2, columnspan=ENTRY_SPAN, padx=ENTRY_ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")


   # Loop through and create all entry points for the green team
   row = 0
   for row in range(MAX_PLAYERS):
       self.textbox = ctk.CTkLabel(window, text=row, fg_color="transparent")
       self.textbox.grid(row=row + 1, column=COLUMN_SHIFT, padx=ROW_PADDING, pady=COLUMN_PADDING , sticky="ew")

       # Displays the ID entry box
       self.id_entry_green[row] = ctk.CTkEntry(window, placeholder_text=ID_PLACEHOLDER)
       # Positions element in a grid
       self.id_entry_green[row].grid(row=row + 1, column=ID_ENTRY_COLUMN + COLUMN_SHIFT, columnspan=ENTRY_SPAN, padx=ENTRY_ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

       # Displays the Codename entry box              
       self.codename_entry_green[row] = ctk.CTkEntry(window, placeholder_text=CODENAME_PLACEHOLDER)
       # Positions element in a grid
       self.codename_entry_green[row].grid(row=row + 1, column=CODENAME_ENTRY_COLUMN + COLUMN_SHIFT, columnspan=ENTRY_SPAN, padx=ENTRY_ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

       # Displays the Hardware ID entry box
       self.hardware_id_entry_green[row] = ctk.CTkEntry(window, placeholder_text=HARDWARE_ID_PLACEHOLDER)
       self.hardware_id_entry_green[row].grid(row=row + 1, column=CODENAME_ENTRY_COLUMN + 2 + COLUMN_SHIFT, columnspan=ENTRY_SPAN, padx=ENTRY_ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

   # Submit Button
   self.submit_button = ctk.CTkButton(window, text="Submit", command=lambda: submit(self))
   # Positions element in a grid, the submit button now goes across the entire bottom portion
   self.submit_button.grid(row=row + 2, column=0, columnspan=COLUMN_SHIFT+CODENAME_ENTRY_COLUMN+ENTRY_SPAN, padx=ROW_PADDING, pady=ROW_PADDING, sticky="ew")
   
   self.instructions = ctk.CTkLabel(window, text="Click the button or press 's' or 'S' when you are ready to start the game")
   self.instructions.grid(row=row + 3, column=0, columnspan=COLUMN_SHIFT+CODENAME_ENTRY_COLUMN+ENTRY_SPAN, padx=ROW_PADDING, pady=0, sticky="ew")
   
   # Start Button
   # IMPORTANT: Andrew, when you are putting your UI changes in below, all you will likely need to do is either modify the create_window function or create a new one with your code inside and call it below
   #            The below code is using an existing function to demonstrate that the code actually does work and currently serves as a placeholder for your code; feel free to modify the dimensions of the
   #            new play action display as it suits your specific UI
   self.start_button = ctk.CTkButton(window, text="Start Game!", command=lambda: create_game_window(GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT, GAME_WINDOW_NAME), fg_color="green", hover_color = "dark green")
   self.start_button.grid(row=row + 4, column=0, columnspan=COLUMN_SHIFT+CODENAME_ENTRY_COLUMN+ENTRY_SPAN, padx=ROW_PADDING, pady=ROW_PADDING, sticky="ew")
   # Also creating binds for the key presses to increase convenience and accessibility
   window.bind("<s>", lambda event: create_game_window(GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT, GAME_WINDOW_NAME))
   window.bind("<S>", lambda event: create_game_window(GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT, GAME_WINDOW_NAME))

   # Bind F12 key to clear all entries
   window.bind("<F12>", lambda event: self.clear_entries())

def create_game_action(self, window):
    # allows for the dynamic scaling of all the rows as the window size is being changed
    # the plus 2 is needed to account for the submit button at the bottom of the screen
    for row in range(0, MAX_PLAYERS + 2):
        window.rowconfigure(row, weight=1)

    # allows for the dynamic scaling of all the columns as the window size is being changed
    for column in range(0, COLUMN_SHIFT+CODENAME_ENTRY_COLUMN+ENTRY_SPAN):
        window.columnconfigure(column, weight=1)

    # Red team title
    self.textbox = ctk.CTkLabel(window, text="Red Team", fg_color="transparent")
    self.textbox.grid(row=0, column=2, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

    # Green Team title
    self.textbox = ctk.CTkLabel(window, text="Green Team", fg_color="transparent")
    self.textbox.grid(row=0, column=2 + COLUMN_SHIFT, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

    self.console = ctk.CTkTextbox(master=self, width=400, corner_radius=0)
    self.console.grid(row=0, column=0, sticky="ew")
    self.console.insert("0.0", "Some example text!\n" * 50)


def center_window(window):
   # Center any window
   window.update_idletasks()
   width = window.winfo_width()
   height = window.winfo_height()
   screen_width = window.winfo_screenwidth()
   screen_height = window.winfo_screenheight()
   x = (screen_width - width) // 2
   y = (screen_height - height) // 2

   window.geometry(f"{width}x{height}+{x}+{y}")

def transmit_equipment_codes(self, team, player_id, codename):
    message = f"Team: {team}, ID: {player_id}, Codename: {codename}"
    response = send_udp_message(message)
    if response:
        print(f"Server response: {response}")
    else :
        print("Failed to transmit equipment.")

#######################################
def clear_entries(self) :
    for entry in self.id_entry_red:
        if isinstance(entry, ctk.CTkEntry):
            entry.delete(0, ctk.END)
    for entry in self.codename_entry_red:
        if isinstance(entry, ctk.CTkEntry):
            entry.delete(0, ctk.END)
    for entry in self.id_entry_green:
        if isinstance(entry, ctk.CTkEntry):
            entry.delete(0, ctk.END)
    for entry in self.codename_entry_green:
        if isinstance(entry, ctk.CTkEntry):
            entry.delete(0, ctk.END)
 #######################################  