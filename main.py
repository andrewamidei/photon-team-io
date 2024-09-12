# Andrew Amidei, Tyler Brandon, Doncan Conly, Evan Meyers, Pranav Polavarapu
# Created 9/11/2024
# Temporary main file for all code
# Split code up before Sprint 2 turn-in

# --- Import ---
import customtkinter
from PIL import Image
import time

# --- Global Definitions ---
WINDOW_WIDTH = 800	# In pixels
WINDOW_HEIGHT = 800	# In pixels
SPLASH_SCREEN_DURATION = 5	# In seconds
SPLASH_SCREEN_LOCATION = "Images/logo.jpg"

# --- Create Window ---
app = customtkinter.CTk()	# creates customtkinter object called "app"
app.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))	# sets pixel size of window to WINDOW_WIDTHxWINDOW_HEIGHT
app.title("Photon Control Panel")	# sets titls of window to "Photon Control Panel"

def create_image(window, image_location, image_width, image_height, image_x, image_y):
	# Creates an image label object then displays image of size on window at location.
	# Inputs: window - customtkinter window object to display image on
	#		  image_location - file location of image to be displayed
	#		  image_width - width in pixels of the image
	#		  image_height - height in pixels of the image
	#		  image_x - x coordinate (in pixels) where upper left corner of image will be displayed relative to (0,0). Positive is right
	#		  image_y - y coordinate (in pixels) where upper left corner of image will be displayed relative to (0,0). Positive is down
	# Outputs: label - CTkLabel object containing image and supporting info such as size and location

	i = customtkinter.CTkImage(light_image = Image.open(image_location), size = (image_width, image_height))	# Creates CTkImage object called "i" containing image file at location and size tuple
	label = customtkinter.CTkLabel(master = window, image = i, text = "")	# Creates a label object used to display the image in the given window
	label.place(x = image_x, y = image_y)	# Moves the image to the x and y coordinates
	return label

# --- Display Splash Screen ---
logo_image = create_image(app, SPLASH_SCREEN_LOCATION, WINDOW_WIDTH, WINDOW_HEIGHT, 0, 0)	# Create the splash screen

app.update()	# Updates window

time.sleep(SPLASH_SCREEN_DURATION)	# Program will sleep for given seconds to show splash screen

logo_image.destroy()	# Delete the splash screen

app.mainloop()	# Updates and stops execution of code? IDK