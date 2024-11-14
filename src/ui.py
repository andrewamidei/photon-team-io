'''
The intention of this file is to serve as the ui library for Photon
Laser Tag software.

As of 9/13/2024 this module will run a simple splash screen and
display a entry terminal for use in setting up your game of laser
tag.
'''

import customtkinter as ctk
from playsound import playsound
import random
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
COLUMN_PADDING = 1 # Standard padding used between entry boxes
ROW_PADDING = 1 # Standard padding for a entry box
BUTTON_PADDING = 10 # Standard Padding for a button

# Entry placeholders
ID_PLACEHOLDER = 'ID'
CODENAME_PLACEHOLDER = 'Codename'
HARDWARE_ID_PLACEHOLDER = 'Hardware ID'
MAX_PLAYERS = 20 # max supported players on a team

# Orientation
ID_ENTRY_COLUMN = 1
CODENAME_ENTRY_COLUMN = 3
HARDWARE_ID_ENTRY_COLUMN = 5
GREEN_TEAM_COLUMN_SHIFT = 7

# Span
ENTRY_SPAN = 2
TOTAL_SPAN = GREEN_TEAM_COLUMN_SHIFT+CODENAME_ENTRY_COLUMN+ENTRY_SPAN+HARDWARE_ID_ENTRY_COLUMN

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

        self.create_entry_terminal(window)

        logo_image.destroy()  # Delete the splash screen when ui is finished loading

    
    def create_entry_terminal(self, window):
        # allows for the dynamic scaling of all the rows as the window size is being changed
        # the plus 2 is needed to account for the submit button at the bottom of the screen
        for row in range(0, MAX_PLAYERS + 2):
            window.rowconfigure(row, weight=1)

        # allows for the dynamic scaling of all the columns as the window size is being changed
        for column in range(0, GREEN_TEAM_COLUMN_SHIFT+CODENAME_ENTRY_COLUMN+ENTRY_SPAN+2):
            window.columnconfigure(column, weight=1)

        # Red team title
        self.textbox = ctk.CTkLabel(window, text="Red Team", fg_color="transparent")
        self.textbox.grid(row=0, column=2, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

        # Green Team title
        self.textbox = ctk.CTkLabel(window, text="Green Team", fg_color="transparent")
        self.textbox.grid(row=0, column=2 + GREEN_TEAM_COLUMN_SHIFT, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

        self.display_entries(window)

        row += 2 # go to next row

        # Submit Button
        self.submit_button = ctk.CTkButton(window, text="Submit", command=lambda: self.submit())
        # Positions element in a grid, the submit button now goes across the entire bottom portion
        self.submit_button.grid(row=row, column=0, columnspan=TOTAL_SPAN, padx=BUTTON_PADDING, pady=BUTTON_PADDING, sticky="ew")
        row += 1 # go to next row

        self.instructions = ctk.CTkLabel(window, text="Click the button or press 'F5' when you are ready to start the game")
        self.instructions.grid(row=row, column=0, columnspan=TOTAL_SPAN, padx=BUTTON_PADDING, pady=4, sticky="ew")
        row += 1 # go to next row

        self.instructions = ctk.CTkLabel(window, text="Press 'F12' To clear Player entries")
        self.instructions.grid(row=row, column=0, columnspan=TOTAL_SPAN, padx=BUTTON_PADDING, pady=4, sticky="ew")
        row += 1 # go to next row

        # Start Button
        self.start_button = ctk.CTkButton(window, text="Start Game!", command=lambda: self.create_game_action(GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT, GAME_WINDOW_NAME), fg_color="green", hover_color = "dark green")
        self.start_button.grid(row=row, column=0, columnspan=TOTAL_SPAN, padx=BUTTON_PADDING, pady=BUTTON_PADDING, sticky="ew")
        # Also creating binds for the key presses to increase convenience and accessibility
        window.bind("<F5>", lambda event: self.create_game_action(GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT, GAME_WINDOW_NAME))
        window.bind("<F5>", lambda event: self.create_game_action(GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT, GAME_WINDOW_NAME))

        # Bind F12 key to clear all entries
        window.bind("<F12>", lambda event: self.clear_entries())

    def display_entries(self, window):
        # Loop through and create all entry points for both teams

        row = 0
        for row in range(MAX_PLAYERS):
            # Create row numbers for the red team
            self.textbox = ctk.CTkLabel(window, text=row, fg_color="transparent")
            self.textbox.grid(row=row + 1, column=0, padx=ROW_PADDING, pady=COLUMN_PADDING , sticky="ew")
            # Create row numbers for the green team
            self.textbox = ctk.CTkLabel(window, text=row, fg_color="transparent")
            self.textbox.grid(row=row + 1, column=GREEN_TEAM_COLUMN_SHIFT, padx=ROW_PADDING, pady=COLUMN_PADDING , sticky="ew")

            # Displays the ID entry box for the red team
            self.id_entry_red[row] = ctk.CTkEntry(window, placeholder_text=ID_PLACEHOLDER) # Creates the entry
            self.id_entry_red[row].grid(row=row + 1, column=ID_ENTRY_COLUMN, columnspan=ENTRY_SPAN, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew") # Positions the entry
            # Displays the ID entry box for the green team
            self.id_entry_green[row] = ctk.CTkEntry(window, placeholder_text=ID_PLACEHOLDER) # Creates the entry
            self.id_entry_green[row].grid(row=row + 1, column=ID_ENTRY_COLUMN + GREEN_TEAM_COLUMN_SHIFT, columnspan=ENTRY_SPAN, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew") # Positions the entry

            # Displays the Codename entry box for the red team            
            self.codename_entry_red[row] = ctk.CTkEntry(window, placeholder_text=CODENAME_PLACEHOLDER) # Creates the entry
            self.codename_entry_red[row].grid(row=row + 1, column=CODENAME_ENTRY_COLUMN, columnspan=ENTRY_SPAN, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew") # Positions the entry
            # Displays the Codename entry box for the green team         
            self.codename_entry_green[row] = ctk.CTkEntry(window, placeholder_text=CODENAME_PLACEHOLDER) # Creates the entry
            self.codename_entry_green[row].grid(row=row + 1, column=CODENAME_ENTRY_COLUMN + GREEN_TEAM_COLUMN_SHIFT, columnspan=ENTRY_SPAN, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew") # Positions the entry

            # Displays the Hardware ID entry box for the red team
            self.hardware_id_entry_red[row] = ctk.CTkEntry(window, placeholder_text=HARDWARE_ID_PLACEHOLDER) # Creates the entry
            self.hardware_id_entry_red[row].grid(row=row + 1, column=HARDWARE_ID_ENTRY_COLUMN, columnspan=ENTRY_SPAN, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew") # Positions the entry
            # Displays the Hardware ID entry box for the green team
            self.hardware_id_entry_green[row] = ctk.CTkEntry(window, placeholder_text=HARDWARE_ID_PLACEHOLDER) # Creates the entry
            self.hardware_id_entry_green[row].grid(row=row + 1, column=HARDWARE_ID_ENTRY_COLUMN + GREEN_TEAM_COLUMN_SHIFT, columnspan=ENTRY_SPAN, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew") # Positions the entry

    def submit(self):
        db.refreshDatabase(self, MAX_PLAYERS)

    def create_game_action(self, width, height, title):
        window = ctk.CTkToplevel()

        window.geometry(str(width) + "x" + str(height))   # sets pixel size of window to width x height
        window.title(title) # sets title of window to title

        center_window(window) # center the window

        play_track()

        background_image = create_image(window, "Images/background.tif", width, height, 0, 0)
        window.update() # Updates window

        for x in range(13, -1, -1):
            image = create_image(window, "Images/" + str(x) + ".tif", 246, 111, 171, 204)
            window.update() # Updates window

            time.sleep(1)

            image.destroy()

        background_image.destroy()

        # allows for the dynamic scaling of all the rows as the window size is being changed
        for row in range(0, MAX_PLAYERS + 2):
            window.rowconfigure(row, weight=1)

        # allows for the dynamic scaling of all the columns as the window size is being changed
        for column in range(0, 6): # TODO: change from had coded 6 to calculation of span for each column below
            window.columnconfigure(column, weight=1)

        row = 0 # to keep track of what row we are on

         # Red team title
        self.textbox = ctk.CTkLabel(window, text="Red Team", fg_color="dark red", text_color = "white")
        self.textbox.grid(row=row, column=0, columnspan = 3, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

        # Green Team title
        self.textbox = ctk.CTkLabel(window, text="Green Team", fg_color="dark green", text_color = "white")
        self.textbox.grid(row=row, column=3, columnspan = 3, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")
        row += 1 # go to next row

        # Red team codename and score titles
        ctk.CTkLabel(window ,text="Codename").grid(row=row, column=0, columnspan=2, padx=5, pady=0, sticky="ew")
        ctk.CTkLabel(window ,text="Score").grid(row=row, column=2, columnspan=1, padx=5, pady=0, sticky="ew")

        # Green team codename and score titles
        ctk.CTkLabel(window ,text="Codename").grid(row=row, column=3 , columnspan=2, padx=5, pady=0, sticky="ew")
        ctk.CTkLabel(window ,text="Score").grid(row=row, column=5, columnspan=1, padx=5, pady=0, sticky="ew")
        row += 1 # go to next row

        # TODO: Temp value storing scores
        player_score_red = [0] * MAX_PLAYERS
        player_score_green = [0] * MAX_PLAYERS

        # Display player data in a loop
        for player in range(MAX_PLAYERS):
            red_id = self.id_entry_red[player].get()
            green_id = self.id_entry_green[player].get()

            # Check if there is data for the red team
            if red_id != '' and self.codename_entry_red[player].get() != '':
                # Display red team codename and score
                red_team_codename = ctk.CTkLabel(window, text=self.codename_entry_red[player].get())
                red_team_codename.grid(row=row, column=0, columnspan=2, padx=5, pady=0, sticky="ew")
                red_team_score = ctk.CTkLabel(window, text=player_score_red[player])
                red_team_score.grid(row=row, column=2, columnspan=1, padx=5, pady=0, sticky="ew")

            # Check if there is data for the green team
            if green_id != '' and self.codename_entry_green[player].get() != '':
                # Display green team codename and score
                green_team_codename = ctk.CTkLabel(window, text=self.codename_entry_green[player].get())
                green_team_codename.grid(row=row, column=3, columnspan=2, padx=5, pady=0, sticky="ew")
                green_team_score = ctk.CTkLabel(window, text=player_score_green[player])
                green_team_score.grid(row=row, column=5, columnspan=1, padx=5, pady=0, sticky="ew")

            row += 1  # go to next row

        # Total score for red team
        red_total_score = 0
        for i in range(0, len(player_score_red)):
            red_total_score += player_score_red[i]
        ctk.CTkLabel(window ,text=red_total_score).grid(row=row, column=2, columnspan=1, padx=5, pady=5, sticky="ew")
        # Total score for green team
        green_total_score = 0
        for i in range(0, len(player_score_green)):
            green_total_score += player_score_green[i]
        ctk.CTkLabel(window ,text=green_total_score).grid(row=row, column=5, columnspan=1, padx=5, pady=5, sticky="ew")
        row += 1 # go to next row
        
        console = ctk.CTkTextbox(window)
        console.grid(row=row, column=0, columnspan=6, padx=BUTTON_PADDING, pady=BUTTON_PADDING, sticky="ew")
        console.insert("0.0", "Active!")
        row += 1 # go to next row

        ctk.CTkLabel(window ,text="Time Remaining: 0:00").grid(row=row, column=4 , columnspan=2, padx=5, pady=0, sticky="ew")

    def transmit_equipment_codes(self, team, player_id, codename): # Should this be in a udp file?
        message = f"Team: {team}, ID: {player_id}, Codename: {codename}"
        response = send_udp_message(message)
        if response:
            print(f"Server response: {response}")
        else :
            print("Failed to transmit equipment.")

    def clear_entries(self) : # TODO: Add comments here so other know what this is doing
        for entry in self.id_entry_red:
            if isinstance(entry, ctk.CTkEntry):
                entry.delete(0, ctk.END)
        for entry in self.codename_entry_red:
            if isinstance(entry, ctk.CTkEntry):
                entry.delete(0, ctk.END)
        for entry in self.hardware_id_entry_red:
            if isinstance(entry, ctk.CTkEntry):
                entry.delete(0, ctk.END)

        for entry in self.id_entry_green:
            if isinstance(entry, ctk.CTkEntry):
                entry.delete(0, ctk.END)
        for entry in self.codename_entry_green:
            if isinstance(entry, ctk.CTkEntry):
                entry.delete(0, ctk.END)
        for entry in self.hardware_id_entry_green:
            if isinstance(entry, ctk.CTkEntry):
                entry.delete(0, ctk.END)
                


################# Functions #################
def create_entry_window(width, height, title): # used in the main function
   window = ctk.CTk()  # creates customtkinter object

   window.geometry(str(width) + "x" + str(height))   # sets pixel size of window to width x height
   window.title(title) # sets title of window to title

   center_window(window) # center the window

   return window

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

def play_track():
        random.seed(157836961)
        track_num = random.randrange(1, 8, 1)
        playsound("tracks/Track0" + str(track_num) + ".mp3", False)