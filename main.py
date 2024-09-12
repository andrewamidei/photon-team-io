# Andrew Amidei, Tyler Brandon, Doncan Conly, Evan Meyers, Pranav Polavarapu
# Created 9/11/2024
# Temporary main file for all code
# Split code up before Sprint 2 turn-in

# --- Import ---
import customtkinter
from PIL import Image
import time
import psycopg2

# --- Global Definitions ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
LOGO_WIDTH = 800
LOGO_HEIGHT = 800
SPLASH_SCREEN_DURATION = 5	# In seconds

# --- Create Window ---
app = customtkinter.CTk()	# creates customtkinter object called "app"
app.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))	# sets pixel size of window to WINDOW_WIDTHxWINDOW_HEIGHT
app.title("Photon Control Panel")	# sets titls of window to "Photon Control Panel"

# --- Display Splash Screen ---
logo_image = customtkinter.CTkImage(dark_image = Image.open("Images/logo.jpg"), size = (LOGO_WIDTH, LOGO_HEIGHT))	# Creates CTkImage object called "logo_image" and adds the logo.jpg to it with size 800x800
logo_image_label = customtkinter.CTkLabel(master = app, image = logo_image, text = '')	# Displays image "logo_image" onto window "app"
logo_image_label.grid(column = 0, row = 0)	# Moves image to 0,0

app.update()	# Updates window

time.sleep(SPLASH_SCREEN_DURATION)	# Program will sleep for given seconds to show splash screen

logo_image_label.destroy()	# Removes the logo image label

app.mainloop()	# Updates and stops execution of code?


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
