# Andrew Amidei, Tyler Brandon, Doncan Conly, Evan Meyers, Pranav Polavarapu
# Created 9/11/2024
# Temporary main file for all code
# TODO: Listed below
# Split code up before Sprint 2 turn-in

# --- Import ---
import customtkinter as ctk
import psycopg2

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

