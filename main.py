from pynput.keyboard import Key, KeyCode, Listener
import pyautogui as pgui
import pyperclip
from tkinter import Tk, Label, Button, messagebox, Text, END
# from PyQt5.QtWidgets import QApplication, QLabel


# /////////// functions
# clean up the keys and move changed string to the clipboard
def clean(txt):
    # clear written letter while pressing the hotkey
    pgui.press('backspace')

    currentKeys.clear()  # clear saved keys that were held down

    # move changed string to the clipboard
    pyperclip.copy(txt)
    pyperclip.paste()

    cpTxt.delete("1.0", END)
    cpTxt.insert(END, txt)


# reverses copied text || txet deipoc sesrever
def reverse_paste():
    clipboard = Tk().clipboard_get()
    reverse = clipboard[::-1]

    clean(reverse)


# sPoNgE PaStE cOpIeD TeXt
def sponge_paste():
    clipboard = Tk().clipboard_get()
    sponge = ''

    # spongify the string
    letter_counter = 0

    for i in range(0, len(clipboard)):
        if clipboard[i] != " ":
            letter_counter += 1
            if letter_counter % 2 == 0:
                sponge += clipboard[i].lower()
            else:
                sponge += clipboard[i].upper()
        else:
            sponge += " "

    clean(sponge)


# f u l l   w i d t h   p a s t e   t e x t
def wide_paste():
    clipboard = Tk().clipboard_get()
    wide = ''

    for i in range(0, len(clipboard)):
        wide += clipboard[i]
        wide += " "

    clean(wide)


# SHORTCUTS COMBINATIONS
# create mapping of keys to the function
combination = {
    frozenset([Key.shift, KeyCode(char='R')]): reverse_paste,
    frozenset([Key.shift, KeyCode(char='r')]): reverse_paste,

    frozenset([Key.shift, KeyCode(char='S')]): sponge_paste,
    frozenset([Key.shift, KeyCode(char='s')]): sponge_paste,

    frozenset([Key.shift, KeyCode(char='W')]): wide_paste,
    frozenset([Key.shift, KeyCode(char='w')]): wide_paste
}

# SETUP
# track and save currently pressed keys
currentKeys = set()
active = True  # checks if shortcuts should work
buttonTxt = "Deactivate"


# key is pressed, add it to the list
def pressed(key):
    # check if software is activated
    if active is True:
        currentKeys.add(key)  # add pressed keys to the set

        # check if pressed keys make an combination
        if frozenset(currentKeys) in combination:
            combination[frozenset(currentKeys)]()


# key is no longer pressed, remove it from the set
def released(key):
    currentKeys.discard(key)


# inverse bool
def activation(act):
    print(act)
    return not act


# ask if user really wants to quit after clicking x
def closing():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        window.destroy()


# create GUI
window = Tk()  # create Tk window
window.title("Text modifier")  # window title
window.geometry('330x170')
window.resizable(False, False)

# labels
# helper text
helper = "1. Copy text \n" \
         "2. Enter possible combination: \n" \
         "      shift + R = txet esrever \n" \
         "      shift + W = f u l l   w i d t h   t e x t \n" \
         "      shift + S = SpOnGiFy TeXt \n" \
         "3. Paste changed text \n"

lbl = Label(window,  anchor="w", text=helper, font=("Lato", 10), justify="left")
lbl.grid(column=0, row=0)

# copyable text
cpTxt = Text(window, height=1, width=36)
cpTxt.grid(column=0, row=1)

# exit
window.protocol("WM_DELETE_WINDOW", closing)

while True:
    if active is True:
        buttonTxt = "Deactivate"
    else:
        buttonTxt = "Activate"

    # deactivation button
    btn = Button(window, text=buttonTxt, command=lambda: activation(active))
    btn.grid(column=0, row=2)

    # listen to key presses
    with Listener(pressed, released) as listener:
        window.mainloop()
        listener.join()
