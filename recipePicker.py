import customtkinter
from PIL import Image
import sqlite3
from numpy import random
import sys
import os
import pyglet


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)


bg_color = "#9b5dc7"

pyglet.font.add_file(resource_path("fonts\\Ubuntu-Bold.ttf"))
pyglet.font.add_file(resource_path("fonts\\Shanti-Regular.ttf"))


def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()
        

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


def pre_process(recipe_name, table_records):
    title = recipe_name[0]
    
    ingredients = []
    
    for i in table_records:
        name = i[0]
        unit = i[2]
        
        if type(i[2] == float):
            qty = i[1]
        else:
            qty = i[1]
        
        if qty == None:
            ingredients.append(name)
        elif unit == None:
            ingredients.append(str(qty) + " " + name)
        else:
            ingredients.append(f"{str(qty)} {str(unit)} of {name}")
    
    return title, ingredients


def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)

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
    
    customtkinter.CTkLabel(
        frame1,
        text="Ready for your random recipe?",
        font=("Ubuntu", 18)
    ).pack()
    
    customtkinter.CTkButton(
        frame1,
        text="SHUFFLE",
        font=("Ubuntu", 20),
        command=lambda: load_frame2()
    ).pack(pady=20)
    
    
def load_frame2():
    clear_widgets(frame1)
    frame.tkraise()
    recipe_name, table_records = fetch_db()
    title, ingredients = pre_process(recipe_name, table_records)
    
    logo_img = customtkinter.CTkImage(
        dark_image=Image.open(resource_path("assets\\RRecipe_logo_bottom.png")),
        size=(125, 125))
    logo_widget = customtkinter.CTkLabel(
        frame2,
        image=logo_img,
        text=" ")
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)
    
    customtkinter.CTkLabel(
        frame2,
        text=title,
        font=("Ubuntu", 20),
    ).pack(pady=25)
    
    for i in ingredients:
        customtkinter.CTkLabel(
            frame,
            text=i,
            font=("Ubuntu", 16),
        ).pack(fill="both")
        
    customtkinter.CTkButton(
        frame2,
        text="BACK",
        font=("Ubuntu", 20),
        cursor="hand2",
        command=lambda: load_frame1()
    ).pack(pady=20)
    
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme(resource_path("newTheme.json"))

root = customtkinter.CTk()
root.title("Recipe Picker")
root.eval("tk::PlaceWindow . center")

frame1 = customtkinter.CTkFrame(root, width=500, height=600)
frame2 = customtkinter.CTkFrame(root)

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")
    
load_frame1()

root.mainloop()