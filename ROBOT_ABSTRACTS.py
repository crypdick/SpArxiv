import markovify
#import easygui

#path = easygui.fileopenbox()

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

print("PICK A MODEL from models folder")
file_path = filedialog.askopenfilename()


#with open("./models/all_abstracts-RICHARD.csv") as abstracts: