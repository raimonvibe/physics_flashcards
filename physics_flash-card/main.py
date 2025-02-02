from tkinter import *
import pandas as pd
import random
import textwrap
from PIL import Image, ImageTk

# Constants
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# Reading data from CSV file
try:
    data = pd.read_csv("data/physics_translated.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/physics_translated.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# Functions
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Term", fill="black")
    canvas.itemconfig(card_word, text=current_card["Term"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    
    # Dynamic flip timing based on the length of the term
    flip_time = min(7000, max(3000, len(current_card["Term"]) * 200))
    flip_timer = window.after(flip_time, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="Meaning", fill="white")
    meaning_text = current_card["Meaning"]
    formatted_text = textwrap.fill(meaning_text, width=int(CARD_WIDTH // 20))  # Adjust width based on card size
    canvas.itemconfig(card_word, text=formatted_text, fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    pd.DataFrame(to_learn).to_csv("data/physics_translated.csv", index=False)
    next_card()

# Image loading function
def load_image(path, target_width, target_height):
    image = Image.open(path)
    image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

# Create window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Dynamically determine canvas size based on window size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
CARD_WIDTH = int(screen_width * 0.5)
CARD_HEIGHT = int(screen_height * 0.5)
window.geometry(f"{CARD_WIDTH + 100}x{CARD_HEIGHT + 100}")

# Set up the flip timer
flip_timer = window.after(5000 , func=flip_card)

# Load images dynamically
card_front_img = load_image("images/card_front.png", CARD_WIDTH, CARD_HEIGHT)
card_back_img = load_image("images/card_back.png", CARD_WIDTH, CARD_HEIGHT)

# Create canvas
canvas = Canvas(width=CARD_WIDTH, height=CARD_HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)
card_background = canvas.create_image(CARD_WIDTH // 2, CARD_HEIGHT // 2, image=card_front_img)
card_title = canvas.create_text(CARD_WIDTH // 2, CARD_HEIGHT * 0.2, text="", font=("Arial", int(CARD_HEIGHT * 0.05), "italic"))
card_word = canvas.create_text(CARD_WIDTH // 2, CARD_HEIGHT * 0.55, text="", font=("Arial", int(CARD_HEIGHT * 0.05), "bold"), width=CARD_WIDTH * 0.8, justify=CENTER)
canvas.grid(row=0, column=0, columnspan=2)

# Load button images and create buttons
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

# Start with the first flashcard
next_card()

# Run the application
window.mainloop()
