import customtkinter as ctk
from PIL import Image
import time
import psycopg2

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

# Splash screen
SPLASH_SCREEN_DURATION = 5  # In seconds
SPLASH_SCREEN_LOCATION = "Images/logo.jpg"

# padding
COLUMN_PADDING = 0 # Standard padding used between entry boxes
ROW_PADDING = 20 # Standard padding used between entry boxes
ENTRY_ROW_PADDING = 5 # Standard padding for a entry box

# Entry placeholders
ID_PLACEHOLDER = 'ID'
CODENAME_PLACEHOLDER = 'Codename'
MAX_PLAYERS = 20 # max supported players on a team
ENTRY_SPAN = 2

# Orientation
COUMN_SHIFT = 7
ID_ENTRY_COLUMN = 1
CODENAME_ENTRY_COLUMN = 3
 
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

# App Class
class PhotonGUI():
    # The layout of the window will be written
    # in the init function itself
    def __init__(self, window, app_width, app_height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Stored data for red team
        self.id_entry_red = ['null'] * MAX_PLAYERS
        self.codename_entry_red = ['null'] * MAX_PLAYERS

        # Stored data for green team
        self.id_entry_green = ['null'] * MAX_PLAYERS
        self.codename_entry_green = ['null'] * MAX_PLAYERS

        # allows for the dynamic scaling of all the rows as the window size is being changed
        # the plus 2 is needed to account for the submit button at the bottom of the screen
        for row in range(0, MAX_PLAYERS + 2):
            window.rowconfigure(row, weight=1)

        # allows for the dynamic scaling of all the columns as the window size is being changed
        for column in range(0, COUMN_SHIFT+CODENAME_ENTRY_COLUMN+ENTRY_SPAN):
            window.columnconfigure(column, weight=1)

        # Red team title
        self.textbox = ctk.CTkLabel(window, text="Red Team", fg_color="transparent")
        self.textbox.grid(row=0, column=2, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

        # Green Team title
        self.textbox = ctk.CTkLabel(window, text="Green Team", fg_color="transparent")
        self.textbox.grid(row=0, column=2 + COUMN_SHIFT, padx=ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

        # Loop through and create all entry points for the red team
        row = 0
        for row in range(MAX_PLAYERS):
            self.textbox = ctk.CTkLabel(window, text=row, fg_color="transparent")
            self.textbox.grid(row=row + 1, column=0, padx=ROW_PADDING, pady=COLUMN_PADDING , sticky="ew")

            # Displays the ID entry box
            self.id_entry_red[row] = ctk.CTkEntry(window, placeholder_text=ID_PLACEHOLDER)
            # Positions element in a grid
            self.id_entry_red[row].grid(row=row + 1, column=ID_ENTRY_COLUMN, columnspan=ENTRY_SPAN, padx=ENTRY_ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

            # Displays the Codename entry box              
            self.codename_entry_red[row] = ctk.CTkEntry(window, placeholder_text=CODENAME_PLACEHOLDER)
            # Positions element in a grid
            self.codename_entry_red[row].grid(row=row + 1, column=CODENAME_ENTRY_COLUMN, columnspan=ENTRY_SPAN, padx=ENTRY_ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

        # Loop through and create all entry points for the green team
        row = 0
        for row in range(MAX_PLAYERS):
            self.textbox = ctk.CTkLabel(window, text=row, fg_color="transparent")
            self.textbox.grid(row=row + 1, column=COUMN_SHIFT, padx=ROW_PADDING, pady=COLUMN_PADDING , sticky="ew")

            # Displays the ID entry box
            self.id_entry_green[row] = ctk.CTkEntry(window, placeholder_text=ID_PLACEHOLDER)
            # Positions element in a grid
            self.id_entry_green[row].grid(row=row + 1, column=ID_ENTRY_COLUMN + COUMN_SHIFT, columnspan=ENTRY_SPAN, padx=ENTRY_ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

            # Displays the Codename entry box              
            self.codename_entry_green[row] = ctk.CTkEntry(window, placeholder_text=CODENAME_PLACEHOLDER)
            # Positions element in a grid
            self.codename_entry_green[row].grid(row=row + 1, column=CODENAME_ENTRY_COLUMN + COUMN_SHIFT, columnspan=ENTRY_SPAN, padx=ENTRY_ROW_PADDING, pady=COLUMN_PADDING, sticky="ew")

        # Submit Button
        self.submit_button = ctk.CTkButton(window, text="Submit", command=self.submit)
        # Positions element in a grid, the submit button now goes across the entire bottom portion
        self.submit_button.grid(row=row + 2, column=0, columnspan=COUMN_SHIFT+CODENAME_ENTRY_COLUMN+ENTRY_SPAN, padx=ROW_PADDING, pady=ROW_PADDING, sticky="ew")
 
    
    # function used to check if there are duplicate player Ids and codenames being added to the database, returns true if there is
    def duplicateChecker(self, player_id, codename):
        cursor.execute("SELECT * FROM players WHERE id = %s OR codename = %s", (player_id, codename))
        result = cursor.fetchall()
        if result:
            return True
        return False

    # This function is used to insert the data into the varibles below
    def submit(self):
        # TODO: add the functionality here for database access
        # deleting players from the last time the submit button was clicked
        for player in range(MAX_PLAYERS):
            cursor.execute(f"DELETE FROM players") 

        # INSERT RED PLAYERS INTO DATABASE
        for player in range(MAX_PLAYERS):
            player_id = self.id_entry_red[player].get()
            codename = self.codename_entry_red[player].get()
            if player_id and codename:
                # checking if the added codename and player_id is a duplicate of one that already exists
                if not self.duplicateChecker(player_id, codename):
                    # Inserts all players from red team into table
                    cursor.execute(f"INSERT INTO players VALUES('{player_id}', '{codename}')")
                else:
                    continue
                    # print message included here in case we will need for future implementation - print("Player ID or Codename has already been entered, please try again with different inputs")

        # INSERT GREEN PLAYERS INTO DATABASE
        for player in range(MAX_PLAYERS): 
            player_id = self.id_entry_green[player].get()
            codename = self.codename_entry_green[player].get()
            if player_id and codename:
                # checking if the added codename and player_id is a duplicate of one that already exists
                if not self.duplicateChecker(player_id, codename):
                    # Inserts all players from green team into table
                    cursor.execute(f"INSERT INTO players VALUES('{player_id}', '{codename}')")
                else:
                    continue
                    # print message included here in case we will need for future implementation - print("Player ID or Codename has already been entered, please try again with different inputs")
        
        #this is being used to remove whatever is currently in the input boxes for the codename and player ID
        for player in range(MAX_PLAYERS):
            self.id_entry_red[player].delete(0, 'end')
            self.codename_entry_red[player].delete(0, 'end') 
            self.id_entry_green[player].delete(0, 'end')
            self.codename_entry_green[player].delete(0, 'end')

        # gets very first row for ID and codename of the red team
        # use [#] to access the row you want
        self.player_id = self.id_entry_red[0].get()
        self.codename = self.codename_entry_red[0].get()

        # print ID and Codename to the console for debug
        # TODO: Remove when finished debugging
        cursor.execute("SELECT * FROM players;")
        players = cursor.fetchall()
        for player in players:
            print(f"ID: {player[0]}, Codename: {player[1]}")

        # Closes PostgreSQL Connection
        connection.commit()
        # connection.close()


# --- Functions ---
def create_window(width, height, title):
    window = ctk.CTk()  # creates customtkinter object

    window.geometry(str(width) + "x" + str(height))   # sets pixel size of window to widthxheight
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

def create_splash_screen(window, window_width, window_height):
    # --- Display Splash Screen ---
    # removed "label image =" since no return was used
    logo_image = create_image(window, SPLASH_SCREEN_LOCATION, window_width, window_height, 0, 0) # Create the splash screen

    window.update() # Updates window

    time.sleep(SPLASH_SCREEN_DURATION)  # Program will sleep for given seconds to show splash screen

    # No longer needed
    logo_image.destroy()  # Delete the splash screen

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