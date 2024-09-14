import customtkinter as ctk
import tkinter as tk
 
# Sets the appearance of the window
# Supported modes : Light, Dark, System
ctk.set_appearance_mode("Dark")   
 
# Sets the color of the widgets in the window
# Supported themes : green, dark-blue, blue    
ctk.set_default_color_theme("dark-blue")    

# Default dimensions of the window
# appWidth, appHeight = 500, 500
 
# App Class
class PhotonGUI(ctk.CTk):
    # The layout of the window will be written
    # in the init function itself
    def __init__(self, appWidth, appHeight, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.playerID = "ID"
        self.codename = "Codename"
 
        # Sets the title of the window to "App"
        self.title("Photon Lazer Tag Entry Terminal")
        
        # Sets the dimensions of the window
        self.geometry(f"{appWidth}x{appHeight}")    

        # Displays the ID entry box
        self.idEntry = ctk.CTkEntry(self, placeholder_text=self.playerID)
        # Positions element in a grid
        self.idEntry.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="ew")

        # Displays the Codename entry box              
        self.codenameEntry = ctk.CTkEntry(self, placeholder_text=self.codename)
        # Positions element in a grid
        self.codenameEntry.grid(row=0, column=3, columnspan=2, padx=20, pady=20, sticky="ew")
                                  
        # Generate Button
        self.generateResultsButton = ctk.CTkButton(self, text="Submit", command=self.generateResults)
        # Positions element in a grid
        self.generateResultsButton.grid(row=2, column=1, columnspan=2, padx=20, pady=20, sticky="ew")
 
 
    # This function is used to insert the data into the varibles below
    def generateResults(self):
        self.playerID = self.idEntry.get()
        self.codename = self.codenameEntry.get()

        # print ID and Codename to the console for debug
        # TODO: Remove when finished debugging
        print(f'ID:  {self.playerID} Codename: {self.codename}')

