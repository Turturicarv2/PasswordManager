from PIL import ImageTk
import string
import random

FONT = 'Ubuntu'
TITLE_SIZE = 20
TEXT_SIZE = 12

def stretch_image(image, image_ratio, canvas, event):
    global resized_tk
    canvas_ratio = int(event.width / event.height)

    if canvas_ratio > image_ratio:
        height = int(event.height)
        width = int(height * image_ratio)
    else:
        width = int(event.width)
        height = int(width / image_ratio)

    resized_image = image.resize((width, height))
    resized_tk = ImageTk.PhotoImage(resized_image)
    canvas.create_image(
        int(event.width / 2), 
        int(event.height / 2), 
        image=resized_tk, 
        anchor = 'center'
    )

def fill_image(image, image_ratio, canvas, event):
    global resized_tk

    canvas_ratio = event.width / event.height

    if canvas_ratio > image_ratio:
        width = int(event.width)
        height = int(width / image_ratio)
    else:
        height = int(event.height)
        width = int(height * image_ratio)

    resized_image = image.resize((width, height))
    resized_tk = ImageTk.PhotoImage(resized_image)
    canvas.create_image(
        int(event.width / 2), 
        int(event.height / 2), 
        image=resized_tk, 
        anchor = 'center'
    )

def generate_password(length):
    symbols = "@$!%*?&"
    password = ''

    while not (any(c in string.ascii_lowercase for c in password) and
               any(c in string.ascii_uppercase for c in password) and
               any(c in string.digits for c in password) and
               any(c in symbols for c in password) and
               len(password) == length):
        password = ''.join(random.choices(string.ascii_letters + string.digits + symbols, k=length))

    return password