import random
from tkinter import *
from PIL import ImageTk, Image
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():

    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    french_word = current_card["French"]
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=french_word, fill="black")
    canvas.itemconfig(canvas_image, image=new_card_front_pic)

    flip_timer = window.after(3000, flip_card)


def flip_card():

    english_word = current_card["English"]
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=english_word, fill="white")
    canvas.itemconfig(canvas_image, image=new_card_back_pic)


def remove_card():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/word_to_learn.csv")
    next_card()


window = Tk()

window.title("Flash Cards Vocabulary")
window.config(padx=20, pady=30, bg="#B1DDC6", bd=0, highlightthickness=0)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=600, height=380, bg="#B1DDC6", highlightthickness=0)
card_front_pic = Image.open("images/card_front.png")
resized_front_pic = card_front_pic.resize((500, 300), Image.ANTIALIAS)
new_card_front_pic = ImageTk.PhotoImage(resized_front_pic)
card_back_pic = Image.open("images/card_back.png")
resized_back_pic = card_back_pic.resize((500, 300), Image.ANTIALIAS)
new_card_back_pic = ImageTk.PhotoImage(resized_back_pic)

canvas_image = canvas.create_image(300, 200, image=new_card_front_pic)
card_title = canvas.create_text(300, 150, text="title", font=("Arial", 20, "italic"))
card_word = canvas.create_text(300, 220, text="Word", font=("Arial", 45, "bold"))


canvas.grid(column=0, row=0, columnspan=4)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, bd=0, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, bd=0, highlightthickness=0, command=remove_card)
right_button.grid(column=2, row=1)

next_card()

window.mainloop()
