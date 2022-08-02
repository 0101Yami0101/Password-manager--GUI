# Passedword Manager

from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# Constants
FONT_NAME = "Courier"
BG_COLOR = 'aqua'


# Generate Password
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
               'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = "".join(password_list)

    # Insert into the password entry field automatically after generating
    entry_Password.insert(0, password)

    # Gets automatically copied to clipboard and can be pasted instantly
    pyperclip.copy(password)


# Save Password
def save_password():
    website_name = entry_Website.get()
    email_username = entry_Email_username.get()
    password = entry_Password.get()

    new_data = {
        website_name: {
            "email" : email_username,
            "password" : password
        }
    }


    if len(website_name) == 0 or len(password) == 0 or len(email_username) == 0:
        messagebox.showinfo(
            title="Oops", message="Make sure no field is empty")
    else:
        try: #reading old data
            with open('data.json', 'r') as datafile:               
                data = json.load(datafile)
        except FileNotFoundError:  #if no old data exists create new file and dump data
            with open('data.json', 'w') as datafile:
                json.dump(new_data, datafile, indent=4)
        else: # if 'try' sucess, update old data with new data            
            data.update(new_data) 

            with open('data.json', 'w') as datafile: #saving updated data to datafile
                json.dump(data, datafile, indent=4)
        finally: # clear entries 
            entry_Website.delete(0, 'end')
            entry_Email_username.delete(0, 'end')
            entry_Password.delete(0, 'end')

#Find a password 
def find_password():
    website = entry_Website.get()
    try:
        with open('data.json') as datafile:
            data = json.load(datafile)
    except FileNotFoundError:#might happen when program runs for first time and search is triggered
        messagebox.showinfo(title = "Error", message = "No data in Data File")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title = 'Website', message= f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showerror(title = "Error", message = f"No entry named '{website}' found")



# GUI setup
window = Tk()
window.title("Password Manager by Yami")
window.config(padx=30, pady=30, bg="aqua")

# canvas
canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(130, 100, image=logo_image)
canvas.grid(column=1, row=0)

# labels
label1 = Label(text="Website: ", bg=BG_COLOR)
label1.grid(column=0, row=1)

label2 = Label(text="Email/Username: ", bg=BG_COLOR)
label2.grid(column=0, row=2)

label3 = Label(text="Password: ", bg=BG_COLOR)
label3.grid(column=0, row=3)

# entries
entry_Website = Entry(width=40)
entry_Website.focus()
entry_Website.grid(column=1, row=1)

entry_Email_username = Entry(width=40)
entry_Email_username.grid(column=1, row=2)

entry_Password = Entry(width=30)
entry_Password.grid(column=1, row=3)

# buttons

button_search = Button(text="Search", width=22, height=1, bg="grey", fg= "black", command= find_password)
button_search.grid(column=2, row=1)

button_generatePass = Button(text="Generate Password", padx=10, bg="grey", font=(
    FONT_NAME, 10, 'bold'), command=generate_password)
button_generatePass.grid(column=2, row=3)

button_add = Button(text="Add", width=20, bg="lime", font=(
    FONT_NAME, 11, 'bold'), command=save_password)
button_add.grid(column=1, row=4)







window.mainloop()