import customtkinter as ctk
from PIL import Image
import time

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

SPLASH_SCREEN_DURATION = 5	# In seconds
SPLASH_SCREEN_LOCATION = "Images/logo.jpg"
TITLE = "Photon Control Panel"
 
# App Class
class PhotonGUI(ctk.CTk):
    # The layout of the window will be written
    # in the init function itself
    def __init__(self, app_width, app_height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.player_id = "ID"
        self.codename = "Codename"
 
        # Sets the title of the window to "App"
        self.title(TITLE)
        
        # Sets the dimensions of the window
        self.geometry(f"{app_width}x{app_height}")    

        # Displays the ID entry box
        self.id_entry = ctk.CTkEntry(self, placeholder_text=self.player_id)
        # Positions element in a grid
        self.id_entry.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="ew")

        # Displays the Codename entry box              
        self.codename_entry = ctk.CTkEntry(self, placeholder_text=self.codename)
        # Positions element in a grid
        self.codename_entry.grid(row=0, column=3, columnspan=2, padx=20, pady=20, sticky="ew")
                                  
        # Generate Button
        self.generate_results_button = ctk.CTkButton(self, text="Submit", command=self.generateResults)
        # Positions element in a grid
        self.generate_results_button.grid(row=2, column=1, columnspan=2, padx=20, pady=20, sticky="ew")
 
 
    # This function is used to insert the data into the varibles below
    def generateResults(self):
        self.player_id = self.id_entry.get()
        self.codename = self.codename_entry.get()

        # print ID and Codename to the console for debug
        # TODO: Remove when finished debugging
        print(f'ID:  {self.player_id} Codename: {self.codename}')


# --- Functions ---
def create_image(app_window, image_location, image_width, image_height, image_x, image_y):
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

def create_splash_screen(app_window, window_width, window_height):
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

