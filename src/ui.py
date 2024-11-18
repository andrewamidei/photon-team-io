'''
The intention of this file is to serve as the ui library for Photon
Laser Tag software.

As of 9/13/2024 this module will run a simple splash screen and
display a entry terminal for use in setting up your game of laser
tag.
'''

import customtkinter as ctk
from PIL import Image
import udp_server
import time
import threading
import random
from playsound import playsound


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

        self.game_stop = False
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

        # Team total scores
        self.total_score_red = 0
        self.total_score_green = 0


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
        self.instructions.grid(row=row, column=0, columnspan=TOTAL_SPAN, padx=BUTTON_PADDING, pady=BUTTON_PADDING, sticky="ew")
        row += 1 # go to next row

        self.instructions = ctk.CTkLabel(window, text="Press 'F12' To clear Player entries")
        self.instructions.grid(row=row, column=0, columnspan=TOTAL_SPAN, padx=BUTTON_PADDING, pady=BUTTON_PADDING, sticky="ew")
        row += 1 # go to next row

        # Start Button
        self.start_button = ctk.CTkButton(window, text="Start Game!", command=lambda: self.create_game_action(GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT, GAME_WINDOW_NAME), fg_color="green", hover_color = "dark green")
        self.start_button.grid(row=row, column=0, columnspan=TOTAL_SPAN, padx=BUTTON_PADDING, pady=BUTTON_PADDING, sticky="ew")
        # Also creating binds for the key presses to increase convenience and accessibility
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

        window.geometry(f"{width}x{height}") # sets pixel size of window to width x height
        window.title(title) # sets title of window to title

        center_window(window) # center the window

        background_image = create_image(window, "Images/background.tif", width, height, 0, 0)
        window.update() # Updates window

        for x in range(30, -1, -1):
            image = create_image(window, "Images/" + str(x) + ".tif", 246, 111, 171, 204)
            window.update() # Updates window

            if x == 15:
                play_track()

            time.sleep(1)

            image.destroy()

        background_image.destroy()

        s1 = threading.Thread(target=self.setup_action_screen, args=(window,), daemon=True)
        s1.start()

        s2 = threading.Thread(target=self.send_start_signal, daemon=True)
        s2.start()
        





    def setup_action_screen(self, window):
        for row in range(0, MAX_PLAYERS + 2):
            window.rowconfigure(row, weight=1)
        for column in range(0, 6):
            window.columnconfigure(column, weight=1)

        row = 0
        ctk.CTkLabel(window, text="Red Team", fg_color="dark red", text_color = "white").grid(row=row, column=0,columnspan = 3, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")
        ctk.CTkLabel(window, text="Green Team", fg_color="dark green", text_color = "white").grid(row=row, column=3,columnspan = 3, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")
        row += 1

        ctk.CTkLabel(window, text="Codename").grid(row=row, column=0, columnspan=2, padx=5, pady=0, sticky="ew")
        ctk.CTkLabel(window, text="Score").grid(row=row, column=2, columnspan=1, padx=5, pady=0, sticky="ew")
        ctk.CTkLabel(window, text="Codename").grid(row=row, column=3, columnspan=2, padx=5, pady=0, sticky="ew")
        ctk.CTkLabel(window, text="Score").grid(row=row, column=5, columnspan=1, padx=5, pady=0, sticky="ew")
        row += 1

        self.player_score_red = [0] * MAX_PLAYERS
        self.player_score_green = [0] * MAX_PLAYERS
        self.codename_labels_red = []
        self.score_labels_red = []
        self.codename_labels_green = []
        self.score_labels_green = []
        self.base_hit_labels_red = []
        self.base_hit_labels_green = []

        for player in range(MAX_PLAYERS):
            red_id = self.id_entry_red[player].get()
            green_id = self.id_entry_green[player].get()

            # Red team setup
            if red_id and self.codename_entry_red[player].get():
                # Add the 🅱️ label in a dedicated small column (column 0)
                base_hit_label = ctk.CTkLabel(window, text="       ", fg_color="transparent")
                base_hit_label.grid(row=row, column=0, padx=1, pady=0, sticky="ew")

                # Place the codename label in the next column (column 1) without using extra padding
                codename_red = self.codename_entry_red[player].get()
                codename_label = ctk.CTkLabel(window, text= codename_red)
                codename_label.grid(row=row, column=1, padx=5, pady=0, sticky="w")  # Align to the left

                score_label = ctk.CTkLabel(window, text="0")
                score_label.grid(row=row, column=2, padx=5, pady=0, sticky="ew")

                self.base_hit_labels_red.append(base_hit_label)
                self.codename_labels_red.append(codename_label)
                self.score_labels_red.append(score_label)


            # Green team setup
            if green_id and self.codename_entry_green[player].get():
                # Add the 🅱️ label in a dedicated small column (column 3)
                base_hit_label = ctk.CTkLabel(window, text="       ", fg_color="transparent")
                base_hit_label.grid(row=row, column=3, padx=1, pady=0, sticky="ew")

                # Place the codename label in the next column (column 4) without using extra padding
                codename_green = self.codename_entry_green[player].get()
                codename_label = ctk.CTkLabel(window, text="    " + codename_green)
                codename_label.grid(row=row, column=4, padx=5, pady=0, sticky="w")  # Align to the left

                score_label = ctk.CTkLabel(window, text="0")
                score_label.grid(row=row, column=5, padx=5, pady=0, sticky="ew")

                self.base_hit_labels_green.append(base_hit_label)
                self.codename_labels_green.append(codename_label)
                self.score_labels_green.append(score_label)


            row += 1


        row += 1
        self.total_score_label_red = ctk.CTkLabel(window, text="Red Team Total Score: 0", fg_color="dark red", text_color="white")
        self.total_score_label_red.grid(row=row, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.total_score_label_green = ctk.CTkLabel(window, text="Green Team Total Score: 0", fg_color="dark green", text_color="white")
        self.total_score_label_green.grid(row=row, column=3, columnspan=3, padx=5, pady=5, sticky="ew")

        row += 1

        self.console = ctk.CTkTextbox(window)
        self.console.grid(row=row, column=0, columnspan=6, padx=BUTTON_PADDING, pady=BUTTON_PADDING, sticky="ew")
        self.console.insert("end", "GAME START!\n")

        # Start listening for game messages
        self.console.after(100, self.listen_for_game_messages)

        row += 1
        time_in_seconds = 360
        
        for game_time in range(time_in_seconds, -1, -1):
            ctk.CTkLabel(window ,text=f"Time Remaining: {str(int(game_time/60)):0>2}:{str(game_time % 60):0>2}").grid(row=row, column=4 , columnspan=2, padx=5, pady=0, sticky="ew")
            # print(f"Time Remaining: {str(int(game_time/60)):0>2}:{str(game_time % 60):0>2}")
            window.update() # Updates window
            time.sleep(1)
        
        self.game_stop = True
        # Exit Button
        ctk.CTkButton(window, text="Finish", command=lambda: window.destroy(), fg_color="green", hover_color = "dark green").grid(row=row, column=0 , columnspan=2, padx=5, pady=0, sticky="ew")



    def send_start_signal(self):
        start_signal = "202"
        response = send_udp_message(start_signal, server_address=('127.0.0.1', 7500))
        if response:
            print("Game start signal sent successfully.")
        else:
            print("Failed to send game start signal.")

    def listen_for_game_messages(self):
        if self.game_stop:
            return
        try:
            # Check the message queue for new messages
            while not udp_server.message_queue.empty():
                game_message = udp_server.message_queue.get()
                print(f"Received game message: {game_message}")
                self.process_game_message(game_message)
        except Exception as e:
            print(f"Error receiving game message: {e}")

        # Schedule the next check in 100 milliseconds
        self.console.after(100, self.listen_for_game_messages)



    def process_game_message(self, message):

        if ":" not in message:
            print(f"Invalid message format: {message}")
            return

        shooter_hardware_id, target_hardware_id = message.split(":")
        shooter_codename, target_codename = "", ""

        # Update scores for red team
        for player in range(MAX_PLAYERS):

            if "43" in message or "53" in message:
                score = 1000
            else:
                score = 100

            if self.hardware_id_entry_red[player].get() == shooter_hardware_id:
                self.player_score_red[player] += score
                self.score_labels_red[player].configure(text=str(self.player_score_red[player]))

                # Update total score for Red Team
                self.total_score_red += score
                self.total_score_label_red.configure(text=f"Red Team Total Score: {self.total_score_red}")

                shooter_codename = self.codename_entry_red[player].get()
                # Check for base hit
                if "43" in message:
                    self.base_hit_labels_red[player].configure(text="🅱️")
                


            if self.hardware_id_entry_green[player].get() == shooter_hardware_id:
                self.player_score_green[player] += score
                self.score_labels_green[player].configure(text=str(self.player_score_green[player]))

                # Update total score for Green Team
                self.total_score_green += score
                self.total_score_label_green.configure(text=f"Green Team Total Score: {self.total_score_green}")

                shooter_codename = self.codename_entry_green[player].get()
                # Check for base hit
                if "53" in message:
                    self.base_hit_labels_green[player].configure(text="🅱️")
                
            if self.hardware_id_entry_red[player].get() == target_hardware_id:
                target_codename = self.codename_entry_red[player].get()

            if self.hardware_id_entry_green[player].get() == target_hardware_id:
                target_codename = self.codename_entry_green[player].get()

        if shooter_codename and target_codename:
            shot_message = f"{shooter_codename} shot {target_codename}\n"
            print(shot_message)  # Debugging output
            self.console.insert("end", shot_message)
            self.console.see("end")
        elif shooter_codename and "43" in message:
            shot_message = f"{shooter_codename} shot Green Base\n"
            print(shot_message)
            self.console.insert("end", shot_message)
            self.console.see("end")
        elif shooter_codename and "53" in message:
            shot_message = f"{shooter_codename} shot Red Base\n"
            print(shot_message)
            self.console.insert("end", shot_message)
            self.console.see("end")


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