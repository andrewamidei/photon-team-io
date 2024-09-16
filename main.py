# Andrew Amidei, Tyler Brandon, Doncan Conly, Evan Meyers, Pranav Polavarapu
# Created 9/11/2024
# Temporary main file for all code


# --- Import ---
import customtkinter as ctk

# --- Modules ---
import ui as ui

# --- Global Definitions ---
WINDOW_WIDTH = 900	# In pixels
WINDOW_HEIGHT = 650	# In pixels


# --- Main function ---
if __name__ == "__main__":
	
	# Comment out the line below to skip the splash screen.
	app = ui.create_splash_screen(WINDOW_WIDTH, WINDOW_HEIGHT) # create start image

	app = ui.PhotonGUI(WINDOW_WIDTH, WINDOW_HEIGHT) # Opens entry terminal

	ui.center_window(app) # center the window

	app.mainloop() # pauses the code
