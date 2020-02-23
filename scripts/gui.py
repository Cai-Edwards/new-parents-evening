from tkinter import Tk, Frame, StringVar, IntVar, OptionMenu, Checkbutton, Button, Label
from initialise_algorithms import first_fit, skip_few, first_few, shake_first_fit, variable_first_fit, randomise
from dict_manipulation import order_by_length, order_by_double
from database import get_appointments, connection, clear_relationships, data_to_pe, remove_general
from analysis import analysis
from output import write, visualise
from list_manipulation import swap
import os.path as path
from os import curdir, mkdir, chdir
from datetime import datetime
import matplotlib.pyplot as plt

def show_visualise():
    global analyse_data

    if analyse_data.get() == 1:
        w.grid(row = 3, column = 3)
        v.grid(row = 2, column = 3)
    else:
        v.deselect()
        v.grid_remove()

        w.deselect()
        w.grid_remove()

        
def run_program():
    al = {"First fit": first_fit, "Skip few": skip_few, "First few": first_few,
          "Shake first fit": shake_first_fit, "Variable first fit": variable_first_fit,
          "Randomise": randomise}

    print("Connecting to DB")
    db = connection("pe")

    print("Clearing the DB")
    clear_relationships(db)

    print("Converting Data")
    data_to_pe(db, year_group.get())

    print("Removing unnecesary values")
    remove_general(db)

    base = base_person.get()

    if base == "Pupil": p = "Teacher"
    else: p = "Pupil"

    print("Grabbing appointments")
    appointments = get_appointments(db, p)

    o = {"None": appointments, "Longest": order_by_length(appointments, True), "Shortest": order_by_length(appointments, False),
         "Double shortest": order_by_double(db, base, appointments, True),
         "Double longest": order_by_double(db, base, appointments, False)}

    print("Ordering appointments")
    apps = o[order.get()]

    print("Calculating timetable")
    data = al[algo_choice.get()](db, base, apps)

    if analyse_data.get()== 1:
        print("Analysing timetable")
        analyse = analysis(data)

    date = datetime.today().strftime('%Y%m%d%H%M%S')

    chdir("..")
    filepath = path.abspath(curdir)

    pat = path.normpath(filepath + "/output/" + date)

    mkdir(pat)

    print("Writing data to " + pat)
    wr = write_data.get()
    if wr == "Both":
        write(data, path.normpath(pat + "/" + base + ".csv"))
        data = swap(db, data, p)
        write(data, path.normpath(pat + "/" + p + ".csv"))
        
    elif wr == "Pupils":
        if base == "Pupil":
            pass
        else:
            data = swap(db, data, p)
            
        write(data, path.normpath(pat + "/pupil.csv"))

    elif wr == "Teachers":
        if base == "Teacher":
            pass
        else:
            data = swap(db, data, p)
            
        write(data, path.normpath(pat + "/teacher.csv"))
        
    if write_stats.get() == 1:
        visualise(analyse, save = True, filepath = pat)

    if visualise_data.get() == 1:
        print("Visualising timetable")
        if write_stats.get() == 1:
            plt.show()
        else:
            visualise(analyse)
    
    print("Done")

    root.quit()
    
root = Tk()
root.title("Parents evening")

frame = Frame(root)
frame.grid(column=0,row=0)
frame.columnconfigure(0, weight = 1)
frame.rowconfigure(0, weight = 1)
frame.pack(pady = 50, padx = 50)

algo_choice = StringVar()
algo_choice.set('First fit')

algo_choices = {"First fit", "Skip few", "First few", "Shake first fit",
           "Variable first fit", "Randomise"}

base_person = StringVar()
base_person.set("Teacher")

base_person_choices = {"Teacher", "Pupil"}

order = StringVar()
order.set("Shortest")

orders = {"None", "Longest", "Shortest", "Double shortest", "Double longest"}

write_data = StringVar()
write_data.set("Both")

write_options = {"None", "Both", "Pupils", "Teachers"}

year_group = IntVar()
year_group.set(7)

year_options = {6, 7, 8, 9, 10, 11, 12, 13}

analyse_data = IntVar()
visualise_data = IntVar()
write_stats = IntVar()

year_popup = OptionMenu(frame, year_group, *year_options)
Label(frame, text="Which year groups data: ").grid(row = 0, column = 0)
year_popup.grid(row = 0, column = 1)

algo_popup = OptionMenu(frame, algo_choice, *algo_choices)
Label(frame, text="Choose an algorithm: ").grid(row = 1, column = 0)
algo_popup.grid(row = 1, column = 1)

person_popup = OptionMenu(frame, base_person, *base_person_choices)
Label(frame, text="Chose whose timetable it will be: ").grid(row = 2, column = 0)
person_popup.grid(row = 2, column = 1)

order_popup = OptionMenu(frame, order, *orders)
Label(frame, text="What order is the appointments needed in: ").grid(row = 3, column = 0)
order_popup.grid(row = 3, column = 1)

write_popup = OptionMenu(frame, write_data, *write_options)
Label(frame, text="Write the timetable data: ").grid(row = 1, column = 4)
write_popup.grid(row = 1, column = 5)

v = Checkbutton(frame, text="Visualise statistics", variable = visualise_data)
w = Checkbutton(frame, text="Write statistics", variable = write_stats)

Checkbutton(frame, text="Analyse timetable", variable = analyse_data, command = show_visualise).grid(row = 1, column = 3)

Button(frame, text="Run", command = run_program).grid(row = 4, column = 2)

root.mainloop()
