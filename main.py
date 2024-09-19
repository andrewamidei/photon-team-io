# Andrew Amidei, Tyler Brandon, Duncan Conly, Evan Meyers, Pranav Polavarapu
# Created 9/11/2024
# Temporary main file for all code


# --- Import ---
import customtkinter as ctk

# --- Modules ---
import ui as ui

# --- Global Definitions ---
WINDOW_WIDTH = 900	# In pixels
WINDOW_HEIGHT = 650	# In pixels
TITLE = "Photon Control Panel" # Title for window

# --- Main function ---
if __name__ == "__main__":
	app_window = ui.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE)
	
	# Comment out the line below to skip the splash screen.
	ui.create_splash_screen(app_window, WINDOW_WIDTH, WINDOW_HEIGHT) # create start image

	ui.PhotonGUI(app_window, WINDOW_WIDTH, WINDOW_HEIGHT) # Opens entry terminal

	app_window.mainloop() # pauses the code
