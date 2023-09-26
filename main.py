from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbol = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_numbers + password_symbol + password_letters
    shuffle(password_list)
    password = "".join(password_list)
    pswd_entry.insert(0, f"{password}")
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_input = website_entry.get()
    email_input = email_entry.get()
    pswd_input = pswd_entry.get()
    new_data = {
        website_input: {
            "email": email_input,
            "password": pswd_input,
        }
    }
    if website_input == "" or pswd_input == "":
        alert_error = messagebox.showinfo(message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            pswd_entry.delete(0, END)


def search_pass():
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(message="No data file found")
    else:
        if website_entry.get() in data.keys():
            password = data[website_entry.get()]["password"]
            message_pass = messagebox.showinfo(message=f"Website = {website_entry.get()}, Password = {password}")
        else:
            messagebox.showinfo(message="No data for the website exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

logo_image = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = Entry(width=19)
website_entry.focus()
website_entry.grid(column=1, row=1)

search_button = Button(text="Search", width=12, command=search_pass)
search_button.grid(column=2, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

email_entry = Entry(width=35)
email_entry.insert(0, "gh.adithya@gmail.com")
email_entry.grid(column=1, row=2, columnspan=2)

pswd_label = Label(text="Password:")
pswd_label.grid(column=0, row=3)

pswd_entry = Entry(width=19)
pswd_entry.grid(column=1, row=3)

generate_pswd = Button(text="Generate Password", width=12, command=generate_password)
generate_pswd.grid(column=2, row=3)

add = Button(text="Add", width=34, command=save)
add.grid(column=1, row=4, columnspan=2)

window.mainloop()
