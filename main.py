# Andrew Amidei, Tyler Brandon, Doncan Conly, Evan Meyers, Pranav Polavarapu
# Created 9/11/2024
# Temporary main file for all code
# Split code up before Sprint 2 turn-in

# --- Import ---
import customtkinter as ctk
from PIL import Image
import time
import psycopg2

# --- Modules ---
from ui import PhotonGUI

# --- Global Definitions ---
WINDOW_WIDTH = 900	# In pixels
WINDOW_HEIGHT = 550	# In pixels
SPLASH_SCREEN_DURATION = 5	# In seconds
SPLASH_SCREEN_LOCATION = "Images/logo.jpg"

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

	i = ctk.CTkImage(light_image = Image.open(image_location), size = (image_width, image_height))	# Creates CTkImage object called "i" containing image file at location and size tuple
	label = ctk.CTkLabel(master = app_window, image = i, text = "")	# Creates a label object used to display the image in the given window
	label.place(x = image_x, y = image_y)	# Moves the image to the x and y coordinates
	# return label

def create_splash_screen(app_window):
	app_window.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))	# sets pixel size of window to WINDOW_WIDTHxWINDOW_HEIGHT
	app_window.title("Photon Control Panel")	# sets titls of window to "Photon Control Panel"

	center_window(app) # center the window

	# --- Display Splash Screen ---
	# removed "label image =" since no return was used
	create_image(app, SPLASH_SCREEN_LOCATION, WINDOW_WIDTH, WINDOW_HEIGHT, 0, 0)	# Create the splash screen

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


# --- Main function ---
if __name__ == "__main__":
	# --- Create Window ---

	app = ctk.CTk()	# creates customtkinter object

	app = create_splash_screen(app)

	app.destroy() # kills the window

	app = PhotonGUI(WINDOW_WIDTH, WINDOW_HEIGHT) # Opens entry terminal

	center_window(app) # center the window

	app.mainloop() # pauses the code


# --- Database Configuration ---
# Connects Python to Postgre database
connection = psycopg2.connect(
	dbname="photon",
	user="student",
	password="student",
	host="localhost",
	port="5432"
)

# Create a cursor to execute SQL queries
cursor = connection.cursor()

# TEMPORARY add Test player each run.
# Uncomment below line to watch as player gets inserted into Database
# cursor.execute("INSERT INTO player values('2', 'EvanTest');")

# Query the player table to retrieve data
# Uncomment below line to retrieve all players from player table
# cursor.execute("SELECT * FROM player;")

# Fetch and print the result
# Following lines print out all players from player table. Above execute line must be uncommented to work.
# players = cursor.fetchall()
# for player in players:
#	print(f"ID: {player[0]}, Codename: {player[1]}")

# Closes PostgreSQL Connection
connection.commit()
connection.close()

