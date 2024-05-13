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


from tkinter import Tk, Label, PhotoImage, Button
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

mock_data = [
["2024/05/13, 10:10:00",  0],
["2024/05/13, 13:00:25",  1],
["2024/05/13, 14:55:33",  0],
["2024/05/13, 17:11:10",  1],
["2024/05/13, 21:30:12",  0],
["2024/05/14, 01:13:54",  1],
["2024/05/14, 05:23:03",  0],
["2024/05/14, 10:43:43",  1]
]
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
    y = [d[1] for d in data]
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
        
    h = calculate_hours(data)
    # print(f"work: {str(timedelta(seconds=h[1]))} | leisure: {str(timedelta(seconds=h[0]))}")
    make_piechart(h, filename_prefix)
    make_graph(data, filename_prefix)

win = Tk()
w = win.winfo_screenwidth()
h = win.winfo_screenheight()

win.title('Productivity Tracker')
# Put it on bottom right of screen(0.8, 0.7)
win.geometry(f"280x170+{int(w*0.8)}+{int(h*0.7)}")
win.resizable(1, 1)

BG_COLOR = "#232f42"
FONT_COLOR = "#ebecf5"
win.configure(background=BG_COLOR)

is_on = True

label = Label(win, 
              text="Idle/Leisure", 
              bg=BG_COLOR, 
              fg=FONT_COLOR, 
              font=("Poppins bold", 22))

label.pack(pady=20)

todays_data = [] # [timestamp, state] state->0(leisure), 1(work)

def button_mode():
    global is_on

    if is_on:
        on_.config(image=off)
        label.config(text="Working", fg=FONT_COLOR)
        is_on = False
        # print("Starting work...")
    else:
        on_.config(image=on)
        label.config(text="Idle/Leisure", fg=FONT_COLOR)
        is_on = True
        # print("Pausing work...")

     # is_on will be flipped!
    todays_data.append([get_timestamp(), (0 if is_on else 1)])


# delay = 1000 # 1 sec

# def check_end_of_day():
    # win.after(delay, check_end_of_day)


on = PhotoImage(file="toggle_green.png")
off = PhotoImage(file="toggle_red.png")

on_ = Button(win, 
             image=on, 
             bg=BG_COLOR, 
             bd=0, 
             activebackground=BG_COLOR, 
             command=button_mode)

on_.pack(pady=0)

todays_data.append([get_timestamp(), 0]) # Starting off with leisure
# win.after(delay, check_end_of_day)
win.mainloop()
print("Exiting...")

# print(todays_data)
save_data(todays_data)