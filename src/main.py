# Andrew Amidei, Tyler Brandon, Duncan Conly, Evan Meyers, Pranav Polavarapu
# Created 9/11/2024
# Temporary main file for all code


# --- Import ---
import customtkinter as ctk
import threading

# --- Modules ---
import ui as ui

# --- UDP ---
import udp_client as udp_client
import udp_server as udp_server


# --- Global Definitions ---
WINDOW_WIDTH = 900	# In pixels
WINDOW_HEIGHT = 650	# In pixels
TITLE = "Photon Control Panel" # Title for window

def start_udp_server():
	udp_server.udp_server()

# --- Main function ---
if __name__ == "__main__":
	# start UDP in separate thread so that it can run in the same terminal while the other code runs
	server_thread = threading.Thread(target=start_udp_server) # creating the new thread
	server_thread.start() # starting the new thread

	app_window = ui.create_entry_window(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE)

	ui.PhotonGUI(app_window) # Opens entry terminal

	app_window.mainloop() # pauses the code
