"""
open a saved Markov model and generate sentences
"""

import markovify
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()

print("PICK A MODEL from models folder")
saved_model_path = filedialog.askopenfilename()
print(saved_model_path)
NUMBER_SENTENCES_TO_GENERATE = 5

with open(saved_model_path, 'r') as f:
    model_json = f.read()
    reconstituted_model = markovify.Text.from_json(model_json)

    for i in range(NUMBER_SENTENCES_TO_GENERATE):
        print(reconstituted_model.make_sentence())




#with open("./models/all_abstracts-RICHARD.csv") as abstracts: