import customtkinter as ctk
from PIL import Image
import time
# import numpy as np
import player as player

'''
The intention of this file is to serve as the ui library for Photon
Lazer Tag software.

As of 9/13/2024 this module will run a simple splash screen and
display a entry terminal for use in setting up your game of lazer
tag.
'''
 
# Sets the appearance of the window
# Supported modes : Light, Dark, System
ctk.set_appearance_mode("Dark")   
 
# Sets the color of the widgets in the window
# Supported themes : green, dark-blue, blue    
ctk.set_default_color_theme("dark-blue")    

# Splash screen
SPLASH_SCREEN_DURATION = 5	# In seconds
SPLASH_SCREEN_LOCATION = "Images/logo.jpg"

# App title
TITLE = "Photon Control Panel" # Title for window

# padding
COLUMN_PADDING = 0 # Standard padding used between entry boxes
ROW_PADDING = 20 # Standard padding used between entry boxes
ENTRY_ROW_PADDING = 5 # Standard padding for a entry box

# Entry placeholders
ID_PLACEHOLDER = 'ID'
CODENAME_PLACEHOLDER = 'Codename'
MAX_PLAYERS = 20 # max supported players on a team
ENTRY_SPAN = 2

# Orientation
COUMN_SHIFT = 7
ID_ENTRY_COLUMN = 1
CODENAME_ENTRY_COLUMN = 3
 
# App Class
class PhotonGUI(ctk.CTk):
    # The layout of the window will be written
    # in the init function itself
    def __init__(self, app_width, app_height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Stored data for red team
        self.id_entry_red = ['null'] * MAX_PLAYERS
        self.codename_entry_red = ['null'] * MAX_PLAYERS

        # Stored data for green team
        self.id_entry_green = ['null'] * MAX_PLAYERS
        self.codename_entry_green = ['null'] * MAX_PLAYERS

        # Sets the title of the window to "App"
        self.title(TITLE)

        # Sets the dimensions of the window
        self.geometry(f"{app_width}x{app_height}") 
        
        # Red team title
        self.textbox = ctk.CTkLabel(self, text="Red Team", fg_color="transparent")
        self.textbox.grid(row=0, column=2, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

        # Green Team title
        self.textbox = ctk.CTkLabel(self, text="Green Team", fg_color="transparent")
        self.textbox.grid(row=0, column=2 + COUMN_SHIFT, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

        # Loop though and create all entry points for the red team
        row = 0
        for row in range(MAX_PLAYERS):
            self.textbox = ctk.CTkLabel(self, text=row, fg_color="transparent")
            self.textbox.grid(row=row + 1, column=0, padx=ROW_PADDING, pady=COLUMN_PADDING , sticky="ew")

            # Displays the ID entry box
            self.id_entry_red[row] = ctk.CTkEntry(self, placeholder_text=ID_PLACEHOLDER)
            # Positions element in a grid
            self.id_entry_red[row].grid(row=row + 1, column=ID_ENTRY_COLUMN, columnspan=ENTRY_SPAN, padx=ENTRY_ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

            # Displays the Codename entry box              
            self.codename_entry_red[row] = ctk.CTkEntry(self, placeholder_text=CODENAME_PLACEHOLDER)
            # Positions element in a grid
            self.codename_entry_red[row].grid(row=row + 1, column=CODENAME_ENTRY_COLUMN, columnspan=ENTRY_SPAN, padx=ENTRY_ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

        # Loop though and create all entry points for the green team
        row = 0
        for row in range(MAX_PLAYERS):
            self.textbox = ctk.CTkLabel(self, text=row, fg_color="transparent")
            self.textbox.grid(row=row + 1, column=COUMN_SHIFT, padx=ROW_PADDING, pady=COLUMN_PADDING , sticky="ew")

            # Displays the ID entry box
            self.id_entry_green[row] = ctk.CTkEntry(self, placeholder_text=ID_PLACEHOLDER)
            # Positions element in a grid
            self.id_entry_green[row].grid(row=row + 1, column=ID_ENTRY_COLUMN + COUMN_SHIFT, columnspan=ENTRY_SPAN, padx=ENTRY_ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

            # Displays the Codename entry box              
            self.codename_entry_green[row] = ctk.CTkEntry(self, placeholder_text=CODENAME_PLACEHOLDER)
            # Positions element in a grid
            self.codename_entry_green[row].grid(row=row + 1, column=CODENAME_ENTRY_COLUMN + COUMN_SHIFT, columnspan=ENTRY_SPAN, padx=ENTRY_ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

        # Submit Button
        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit)
        # Positions element in a grid
        self.submit_button.grid(row=row + 2, column=1, columnspan=2, padx=ROW_PADDING, pady=ROW_PADDING, sticky="ew")
 
 
    # This function is used to insert the data into the varibles below
    def submit(self):
        # TODO: add the functinallity here for database access

        # gets very first row for ID and codename of the red team
        # use [#] to access the row you want
        self.player_id = self.id_entry_red[0].get()
        self.codename = self.codename_entry_red[0].get()

        # print ID and Codename to the console for debug
        # TODO: Remove when finished debugging
        print(f'ID: {self.player_id} Codename: {self.codename}')


# --- Functions ---
def create_image(app_window ,image_location, image_width, image_height, image_x, image_y):
	# Creates an image label object then displays image of size on window at location.
	# Inputs: window - customtkinter window object to display image on
	#		  image_location - file location of image to be displayed
	#		  image_width - width in pixels of the image
	#		  image_height - height in pixels of the image
	#		  image_x - x coordinate (in pixels) where upper left corner of image will be displayed relative to (0,0). Positive is right
	#		  image_y - y coordinate (in pixels) where upper left corner of image will be displayed relative to (0,0). Positive is down
	# Outputs: label - CTkLabel object containing image and supporting info such as size and location
    
    image = ctk.CTkImage(light_image = Image.open(image_location), size = (image_width, image_height))	# Creates CTkImage object called "i" containing image file at location and size tuple
    label = ctk.CTkLabel(master = app_window, image = image, text = "")	# Creates a label object used to display the image in the given window
    label.place(x = image_x, y = image_y)	# Moves the image to the x and y coordinates
    # return label

def create_splash_screen( window_width, window_height):
    app_window = ctk.CTk()	# creates customtkinter object

    app_window.geometry(str(window_width) + "x" + str(window_height))	# sets pixel size of window to WINDOW_WIDTHxWINDOW_HEIGHT
    app_window.title(TITLE)	# sets titls of window to "Photon Control Panel"

    center_window(app_window) # center the window

    # --- Display Splash Screen ---
    # removed "label image =" since no return was used
    create_image(app_window, SPLASH_SCREEN_LOCATION, window_width, window_height, 0, 0)	# Create the splash screen

    app_window.update()	# Updates window

    time.sleep(SPLASH_SCREEN_DURATION)	# Program will sleep for given seconds to show splash screen

    # No longer needed
    # logo_image.destroy()	# Delete the splash screen

    # TODO: Fix this issue:
    # Behavior: Splash screen will kill itself and entry window will replace it.
    # Expexted behavuior: window will transition to entry screen.
    app_window.destroy() # kills the window

    return app_window

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

