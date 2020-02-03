from tkinter import *

root = Tk()
root.title("Parents evening")

# Add a grid
frame = Frame(root)
frame.grid(column=0,row=0)
frame.columnconfigure(0, weight = 1)
frame.rowconfigure(0, weight = 1)
frame.pack(pady = 100, padx = 100)

# Create a Tkinter variable
algo_choice = StringVar(root)

choices = {"first_fit", "skip_few", "first_few", "shake_first_fit",
           "variable_first_fit", "randomise"}

algo_choice.set('first_fit')

popupMenu = OptionMenu(frame, algo_choice, *choices)
Label(frame, text="Choose an algorithm: ").grid(row = 0, column = 0)
popupMenu.grid(row = 0, column =1)

# on change dropdown value
def change_algo(*args):
    print(algo_choice.get())

algo_choice.trace('w', change_algo)

root.mainloop()
