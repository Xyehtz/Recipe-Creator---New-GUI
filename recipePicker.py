# Import the necessary libraries

# For GUI cretion

import customtkinter
from PIL import Image

# Database

import sqlite3

# Random selection from the database

from numpy import random

# Creation of the .exe file

import sys
import os

# Addition of custom fonts

import pyglet

""" This function will do:
    1. Obtain the relative file of the different media used on the project
    2. Obtain the path of the executable file if theres one
    3. Capture any error that could happen
    4. Obtain the new file path of the executable"""

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)

# Background color

bg_color = "#9b5dc7"

# Load the fonts used on the project

pyglet.font.add_file(resource_path("fonts\\Ubuntu-Bold.ttf"))
pyglet.font.add_file(resource_path("fonts\\Shanti-Regular.ttf"))

# Destroy any frame when the user is on another one


def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()
        

""" Connect to the SQLite database and obtain:
        1. Obtain the title of the recipes
        2. Obtain the name, quantity and unit of the recipe depending of the randomly obtain recipe title
        3. Close the connection and retunr the recipe name and the recipe ingredients"""

def fetch_db():
    connection = sqlite3.connect(resource_path("data\\recipes.db"))
    cursor = connection.cursor()
    cursor.execute("SELECT title, primary_key FROM recipes")
    all_titles = cursor.fetchall()
    
    idx = random.randint(0, len(all_titles) -1)
    
    recipe_name = all_titles[idx]
    cursor.execute("SELECT name, qty, unit FROM ingredients WHERE recipe_key=:k;", {"k": idx})
    table_records = cursor.fetchall()
    
    connection.close()
    return recipe_name, table_records


# Define a new function where all the information will be pre processed

def pre_process(recipe_name, table_records):
    title = recipe_name[0]
    
    # Create an array for the ingredients to be stored

    ingredients = []
    
    for i in table_records:

        # Obtain the name and unit, quantity of the ingredients

        name = i[0]
        qty = i[1]
        unit = i[2]

        # Append the ingredients depending on the information that is avialable

        if qty == None:
            ingredients.append(name)
        elif unit == None:
            ingredients.append(str(qty) + " " + name)
        else:
            ingredients.append(f"{str(qty)} {str(unit)} of {name}")

    # Return the title and the array of ingredients

    return title, ingredients

# Create and load the first frame when the user opens the app

def load_frame1():

    # Delete the frame2 if it was open

    clear_widgets(frame2)

    # Load frame1 and put it above every other frame

    frame1.tkraise()
    frame1.pack_propagate(False)

    # Create the widgets of frame1
    # Create the widget with the logo image of the first frame

    logo_img = customtkinter.CTkImage(
        dark_image=Image.open("assets\\RRecipe_logo.png"),
        size=(300, 300)
    )
    logo_widget = customtkinter.CTkLabel(
        frame1,
        image=logo_img,
        text=""
    )
    logo_widget.image = logo_img
    logo_widget.pack()
    
    # Create a widget with a custom label

    customtkinter.CTkLabel(
        frame1,
        text="Ready for your random recipe?",
        font=("Ubuntu", 18)
    ).pack()
    
    # Create a button that will load frame2

    customtkinter.CTkButton(
        frame1,
        text="SHUFFLE",
        font=("Ubuntu", 20),
        command=lambda: load_frame2()
    ).pack(pady=20)
    
# Create and load frame2

def load_frame2():

    # Delete frame1 if previously open

    clear_widgets(frame1)

    # Load frame2 and put every widget on top of frame2

    frame.tkraise()

    # Obtain the name of the recipe and the ingredients from the database

    recipe_name, table_records = fetch_db()
    title, ingredients = pre_process(recipe_name, table_records)
    
    # Create a widget with a new image

    logo_img = customtkinter.CTkImage(
        dark_image=Image.open(resource_path("assets\\RRecipe_logo_bottom.png")),
        size=(125, 125))
    logo_widget = customtkinter.CTkLabel(
        frame2,
        image=logo_img,
        text=" ")
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)
    
    # Create a label for the title of the recipe

    customtkinter.CTkLabel(
        frame2,
        text=title,
        font=("Ubuntu", 20),
    ).pack(pady=25)
    
    # Create a label with all the ingredients of the recipe

    for i in ingredients:
        customtkinter.CTkLabel(
            frame,
            text=i,
            font=("Ubuntu", 16),
        ).pack(fill="both")
        
    # Create a button to load frame1

    customtkinter.CTkButton(
        frame2,
        text="BACK",
        font=("Ubuntu", 20),
        cursor="hand2",
        command=lambda: load_frame1()
    ).pack(pady=20)
    
# Set the appearance theme of the GUI

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme(resource_path("newTheme.json"))

# Set the title and size of thw window

root = customtkinter.CTk()
root.title("Recipe Picker")
root.eval("tk::PlaceWindow . center")

frame1 = customtkinter.CTkFrame(root, width=500, height=600)
frame2 = customtkinter.CTkFrame(root)

# Create the grid of frame 1 and 2

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")
    
# Start the program by loading frame1, the app wont close until the user closes it

load_frame1()

root.mainloop()