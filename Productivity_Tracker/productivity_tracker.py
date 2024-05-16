# Simple Productivity Tracker

# - Has a toggle button in a small window which you can use
#   to switch between 'work' and 'other' mode.
# - Generates graphs for each day?.
#   - Line plot + Pie chart

# Goals:
# - Get a ballpark figure of how long I work in a day on the computer.
# - 

# Enhancements:
# - Store a brief description of what you're working on/doing. Save/load 
#   them as necessary. Makes piechart more detailed.
# - 

# Issues:
# - How to catch getting side-tracked during work and vice-versa?.
# - How to catch inactive/idle mode.(i.e. when you forget to hit the button)
# - What exactly counts as work?
# - You may want to add new activities while still working on something else. This is
#   currently not supported(for simplicity).
# - 


from tkinter import Tk, Label, PhotoImage, Button, Frame, ttk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os


# As long as you stick with YYYY/mm/dd, HH:MM:SS format, you can compare 
# date strings.
def get_timestamp(for_filename=False):
    if for_filename:
        return datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    else:
        return datetime.now().strftime("%Y/%m/%d, %H:%M:%S")

def calculate_hours(data):
    hours = [0, 0]
    for i, d in enumerate(data):
        if i > 0:
            curr = datetime.strptime(data[i][0], "%Y/%m/%d, %H:%M:%S")
            prev = datetime.strptime(data[i-1][0], "%Y/%m/%d, %H:%M:%S")
            hours[data[i-1][1]] += (curr-prev).seconds
    return hours

def make_piechart(hours, f_prefix, show=False):
    y = hours
    p_labels = [f"idle/leisure({str(timedelta(seconds=hours[0]))})", f"work({str(timedelta(seconds=hours[1]))})"]
    
    plt.pie(y, labels=p_labels)
    plt.title(f"{get_timestamp()}")
    plt.xlabel('')
    plt.ylabel('')
    plt.savefig(f_prefix+"_piechart.png")
    
    if show:
        plt.show()
    print(f"Successfully made piechart.")

def make_graph(data, f_prefix, show=False):
    x = [datetime.strptime(d[0], "%Y/%m/%d, %H:%M:%S") for d in data]
    x.append(datetime.now())
    
    y = [d[1] for d in data]
    y.append(y[-1])
    
    plt.figure(figsize=(10, 5))
    plt.step(x, y, where='post')
    plt.title(f"{get_timestamp()}")
    plt.xlabel('Time')
    plt.ylabel('Activity')
    plt.xticks(x, rotation=90, fontsize=8)
    plt.yticks([0, 1], ['Idle', 'Work'])
    
    date_formatter = mdates.DateFormatter('%Y/%m/%d, %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(date_formatter)
    
    plt.tight_layout()
    plt.savefig(f_prefix+"_timeline.png")
   
    if show:
        plt.show()
    print(f"Successfully made timeline graph.")

def save_data(data):
    filename_prefix = f"data\\{get_timestamp(for_filename=True)}"
    with open(filename_prefix+"_data.txt", 'a') as data_file:
        for d in data:
            data_file.write(f"{d[0]} {str(d[1])}\n")
        print(f"Successfully wrote data.")
        
    if len(data) > 1:
        h = calculate_hours(data)
        # print(f"work: {str(timedelta(seconds=h[1]))} | leisure: {str(timedelta(seconds=h[0]))}")
        make_piechart(h, filename_prefix)
    
    make_graph(data, filename_prefix)

win = Tk()
w = win.winfo_screenwidth()
h = win.winfo_screenheight()
icon = PhotoImage(file="assets\\icon.png")
win.wm_iconphoto(True, icon)

win.title('Productivity Tracker')
# Put it on bottom right of screen(0.8, 0.7)
win.geometry(f"280x270+{int(w*0.8)}+{int(h*0.55)}")
win.resizable(0, 0)

BG_COLOR = "#232f42"
BG_COLOR2 = "#23ef42"
FONT_COLOR = "#ebecf5"
win.configure(background=BG_COLOR)

is_on = True
curr_activity = "Undefined"

label = Label(win, 
              text="Idle/Leisure", 
              bg=BG_COLOR, 
              fg=FONT_COLOR, 
              font=("Poppins bold", 22))

label.pack(pady=20)

todays_data = [] # [timestamp, state, activity_name] state->0(leisure), 1(work)
activities = ["Undefined"]

def button_mode():
    global is_on
    global curr_activity

    if is_on:
        # print("is_on ", curr_activity)
        if curr_activity not in ["Undefined", "N.A."]:
            on_.config(image=off)
            label.config(text="Working", fg=FONT_COLOR)
            is_on = False
            activity_combo.configure(state="disabled")
            # print("Starting work...")
        else:
            print("Please choose or create activity >_<")
    else:
        on_.config(image=on)
        label.config(text="Idle/Leisure", fg=FONT_COLOR)
        is_on = True
        activity_combo.current(0) # Reset to undefined
        activity_combo.configure(state="readonly")
        curr_activity = "Undefined"
        # print("Pausing work...")

     # is_on will be flipped!
    todays_data.append([get_timestamp(), 
                        (0 if is_on else 1), 
                        curr_activity])
    if curr_activity != todays_data[-2][2]:
        print(f"Started activity: {curr_activity}")


delay = 5*60*1000 # 5 minutes
SESSION_LOAD_ATTEMPTED = False

def autosave():
    save_activities(activities)
    win.after(delay, autosave)

def activity_selected(event):
    global curr_activity
    curr_activity = activity_combo.get()
    print(f"{curr_activity} selected")

def activity_added(event):
    global curr_activity
    print(activities)
    curr_activity = activity_combo.get()
    if curr_activity and curr_activity not in activities:
        activities.append(curr_activity)
        activity_combo.configure(values=activities)
        print(f"curr:{curr_activity}, ", activity_combo['values'])
        set_combo_state(0)

def set_combo_state(s):
    if is_on: # in Idle mode
        if s == 0:
            activity_combo.configure(state="readonly")
        elif s == 1:
            activity_combo.configure(state="normal")
    else:
        print("Can't add new activities in work mode.")

def remove_current_activity():
    global activities
    global curr_activity
    
    a = activity_combo.get()
    if not is_on and a == curr_activity:
        print("Can't remove activity you're currently working on!")
        return
    
    if a and a not in ["Undefined", "N.A."]:
        activities = list(filter((a).__ne__, activities)) # Not sure why I'm doing this since there will just be one occurrance anyway
        activity_combo.configure(values=activities)
        activity_combo.current(0)
        curr_activity = "Undefined" # Don't do this. Make a variable and use that dum-dum
        print(f"removed {a}")
        print(activity_combo['values'])

def clear_activities():
    if is_on: # currently in Idle mode
        global activities
        global curr_activity
        
        activities = ["Undefined"]
        activity_combo.configure(values=activities)
        activity_combo.current(0)
        curr_activity = "Undefined"
        print(activity_combo['values'])
    else:
        print("Can't clear activities while in working mode!")

def load_activities():
    global SESSION_LOAD_ATTEMPTED
    # Check for existing file
    session_filename = "activities.txt"
    act_list = []
    if os.path.isfile(session_filename):
        # Load list into python list
        with open(session_filename) as f:
            for line in f.readlines():
                act_list.append(line.rstrip())
        
    SESSION_LOAD_ATTEMPTED = True
    # Return the list
    return act_list

def save_activities(a):
    # Currently, this overwrites every time, which is not ideal.
    # Instead, we need to check if there's already a file and combine this with that.
    # If there isn't already a file, then just write.
    # Actually, this is only a problem if we save without ever calling load() during
    # a session, which shouldn't really happen.
    if SESSION_LOAD_ATTEMPTED:
        activities_list = sorted(list(filter(("Undefined").__ne__, a)))
        if activities_list:
            with open("activities.txt", 'w') as f:
                for activity in activities_list:
                    f.write(f"{activity}\n")
            print("Activities from current session saved..")
    else:
        print("There may be activities saved from a previous session(load() wasn't called). Aborting...")



activities += load_activities()

on = PhotoImage(file=os.path.join("assets", "toggle_green.png"))
off = PhotoImage(file=os.path.join("assets", "toggle_red.png"))
plus = PhotoImage(file=os.path.join("assets", "plus.png"))
minus = PhotoImage(file=os.path.join("assets", "minus.png"))

on_ = Button(win, 
             image=on, 
             bg=BG_COLOR, 
             bd=0, 
             activebackground=BG_COLOR, 
             command=button_mode)

on_.pack(pady=0)

activity_combo = ttk.Combobox(win, values=activities, state='readonly')
activity_combo.pack(pady=10)
activity_combo.bind("<<ComboboxSelected>>", activity_selected)
activity_combo.bind("<Return>", activity_added)

buttons = Frame(win, bg=BG_COLOR)
buttons.pack(pady=10)

plus_ = Button(buttons, 
               image=plus, 
               bg=BG_COLOR, 
               bd=0, 
               activebackground=BG_COLOR, 
               command= lambda: set_combo_state(1))
plus_.pack(padx=14, side='left')

minus_ = Button(buttons, 
                image=minus, 
                bg=BG_COLOR, 
                bd=0, 
                activebackground=BG_COLOR, 
                command=remove_current_activity)
minus_.pack(padx=14, side="right")

clear_ = Button(buttons,
                text="Clear",
                width=6,
                height=2,
                bg=BG_COLOR2, 
                bd=0, 
                activebackground=BG_COLOR2, 
                command=clear_activities)
clear_.pack()

activity_combo.current(0)
todays_data.append([get_timestamp(), 0, curr_activity]) # Starting off with leisure
win.after(delay, autosave)
win.mainloop()
print("Exiting...")

# print(todays_data)
# save_data(todays_data)
save_activities(activities)