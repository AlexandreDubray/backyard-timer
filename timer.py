import tkinter as tk
from tkinter import Label, ttk, StringVar
import time
from datetime import datetime
from winsound import Beep
import threading

fontText=("Arial", 25)
fontCount=("Arial", 200)
root = tk.Tk()
root.title('Ultra-backyard timer')

# epoch at which the race starts
startTime = 0
# How much time before the next "beeps" and loop
delayBeep = 0
delayBeepBeep = 0
delayBeepBeepBeep = 0
nextLoop = 0
loopTime = 0
clockLabel = None

# How much time each "beep" should last and their frequency
beepDuration = 300
beepFrequency = 1250

def beep():
    Beep(beepFrequency, beepDuration)

def beepBeep():
    Beep(beepFrequency, beepDuration)
    Beep(beepFrequency, beepDuration)

def beepBeepBeep():
    Beep(beepFrequency, beepDuration)
    Beep(beepFrequency, beepDuration)
    Beep(beepFrequency, beepDuration)

def newLoop():
    Beep(beepFrequency, 1000)

# Updates the clock label. Get the current epoch and computes how much hours, minutes, and seconds have elapsed since the begining of the race.
def updateClockLabel():
    global delayBeep, delayBeepBeep, delayBeepBeepBeep, nextLoop
    # All the time computations are based on the epoch time (i.e., a fixed references to 1st of January 1970, midnight UTC).
    # Each call to time.time() returns the number of seconds since that reference time; hence, the difference between two time.time() call represent a number of elapsed seconds.
    # The timer for the beeps are expressed as a duration of elapsed time.
    elapsed = int(time.time()) - startTime
    hours = int(elapsed / 3600)
    minutes = int(elapsed / 60) % 60
    seconds = elapsed % 60
    clockLabel.configure(text='{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds))
    # If the elapsed time is larger or equal to the beeps epoch, launch the beeps accordingly and update their next time.
    # This updated time is independent from the current time to avoid deviation from the expected beep times.
    # The beeps are launched within threads to avoid "freezing" the timer; it gives a smoother results.
    # In practice, there are not real "overhead" in this code so this is fine.
    if elapsed >= delayBeep:
        delayBeep += loopTime
        threading.Thread(target=beep).start()
    if elapsed >= delayBeepBeep:
        delayBeepBeep += loopTime
        threading.Thread(target=beepBeep).start()
    if elapsed >= delayBeepBeepBeep:
        delayBeepBeepBeep += loopTime 
        threading.Thread(target=beepBeepBeep).start()
    if elapsed >= nextLoop:
        nextLoop += loopTime
        threading.Thread(target=newLoop).start()
    clockLabel.after(10, updateClockLabel)

# Starts the countdown until the start of the race.
def startCountDown():
    # Computes the remaining time; if less than 0 then starts the race. Otherwise, computing the hours, minutes, and second remaining and updates the clock label.
    remaining = startTime - int(time.time())
    if remaining <= 0:
        clockLabel.after(10, updateClockLabel)
    else:
        hours = int(remaining / 3600)
        minutes = int(remaining / 60) % 60
        seconds = remaining % 60
        clockLabel.configure(text='{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds))
        clockLabel.after(10, startCountDown)

def get_int_input(text):
    return [int(x) for x in text.split() if x.isdigit()][0]

def get_seconds_from_time_choice(holders):
    values = [int(x.get().split()[0]) for x in holders]
    return values[0]*3600 + values[1]*60 + values[2]

# Initialise the starting time given the choice in the dropdown lists.
# Removes all widgets and put the clock label on screen.
def initialise():
    global startTime, delayBeep, delayBeepBeep, delayBeepBeepBeep, nextLoop, loopTime, clockLabel
    startH = int(startRaceTime[0].get().split()[0])
    startM = int(startRaceTime[1].get().split()[0])
    startS = int(startRaceTime[2].get().split()[0])

    currentTime = datetime.now()
    startTime = int(datetime(currentTime.year, currentTime.month, currentTime.day, startH, startM, startS).timestamp())

    delayBeep = get_seconds_from_time_choice(delayFirstSignal)
    delayBeepBeep = get_seconds_from_time_choice(delaySecondSignal)
    delayBeepBeepBeep = get_seconds_from_time_choice(delayThirdSignal)
    loopTime = get_seconds_from_time_choice(delayNewLoop)

    for widget in root.winfo_children():
        widget.destroy()
    # Text that will show the countdown until/from the start of the race
    clockLabel = Label(root, text="00:00:00", font=fontCount)

    clockLabel.pack(expand=True, fill='both')
    clockLabel.after(10, startCountDown)


def make_time_choice(text, row, defaultH, defaultM, defaultS):
    l = Label(root, text=text, font=fontText)
    l.grid(row=row, column=0)

    holder = [StringVar(), StringVar(), StringVar()]
    h = ttk.Combobox(root, textvariable=holder[0])
    h['values'] = ['{} heures'.format(x) for x in range(24)]
    h.current(defaultH)
    h.grid(row=row, column=1)

    m = ttk.Combobox(root, textvariable=holder[1])
    m['values'] = ['{} minutes'.format(x) for x in range(60)]
    m.current(defaultM)
    m.grid(row=row, column=2)

    s = ttk.Combobox(root, textvariable=holder[2])
    s['values'] = ['{} secondes'.format(x) for x in range(60)]
    s.current(defaultS)
    s.grid(row=row, column=3)
    return holder

# Initial layout for the application. Give the user a way to select the start time of the race and a big button to launch the countdown.
# This is not supposed to be "good looking". The goal is to be functionnal with as few overhead as possible.
startRaceTime = make_time_choice("Heure du début de la course:", 0, 9, 0, 0)
delayFirstSignal = make_time_choice("Délai signal sonor 1:", 1, 0, 57, 0)
delaySecondSignal = make_time_choice("Délai signal sonor 2:", 2, 0, 58, 0)
delayThirdSignal = make_time_choice("Délai signal sonor 3:", 3, 0, 59, 0)
delayNewLoop = make_time_choice("Nouvelle boucle toute les:", 4, 1, 0, 0)

startButton = tk.Button(root, text="START", font=fontText, command=initialise, bg='green')
startButton.grid(row=5, column=0, columnspan=4)
root.state("zoomed")
root.mainloop()
