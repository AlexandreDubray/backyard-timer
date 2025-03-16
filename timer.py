import tkinter as tk
from tkinter import Label, ttk, StringVar
import time
from datetime import datetime
from winsound import Beep
import threading

fontText=("Arial", 25)
fontCount=("Arial", 200)
root = tk.Tk()

# Text that will show the countdown until/from the start of the race
clockLabel = Label(root, text="00:00:00", font=fontCount)

# epoch at which the race starts
startTime = 0
# How much time before the next "beeps" and loop
nextBeep = 0
nextBeepBeep = 0
nextBeepBeepBeep = 0
nextLoop = 0

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

# Starts the timer of the race. Set the next beeps to be after 57, 58, and 59 minutes. The new loop starts in one hour.
# Also launch the loop that update the clock label
def startTimer():
    global nextBeep, nextBeepBeep, nextBeepBeepBeep, nextLoop
    nextBeep = 57*60
    nextBeepBeep = 58*60
    nextBeepBeepBeep = 59*60
    nextLoop = 3600
    clockLabel.after(10, updateClockLabel)

# Updates the clock label. Get the current epoch and computes how much hours, minutes, and seconds have elapsed since the begining of the race.
def updateClockLabel():
    global nextBeep, nextBeepBeep, nextBeepBeepBeep, nextLoop
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
    if elapsed >= nextBeep:
        nextBeep += 3600
        threading.Thread(target=beep).start()
    if elapsed >= nextBeepBeep:
        nextBeepBeep += 3600
        threading.Thread(target=beepBeep).start()
    if elapsed >= nextBeepBeepBeep:
        nextBeepBeepBeep += 3600
        threading.Thread(target=beepBeepBeep).start()
    if elapsed >= nextLoop:
        nextLoop += 3600
        threading.Thread(target=newLoop).start()
    clockLabel.after(10, updateClockLabel)

# Starts the countdown until the start of the race.
def startCountDown():
    # Computes the remaining time; if less than 0 then starts the race. Otherwise, computing the hours, minutes, and second remaining and updates the clock label.
    remaining = startTime - int(time.time())
    if remaining <= 0:
        threading.Thread(target=newLoop).start()
        startTimer()
    else:
        hours = int(remaining / 3600)
        minutes = int(remaining / 60) % 60
        seconds = remaining % 60
        clockLabel.configure(text='{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds))
        clockLabel.after(10, startCountDown)

# Initialise the starting time given the choice in the dropdown lists.
# Removes all widgets and put the clock label on screen.
def initialise():
    global startTime
    startH = int(startHour.get())
    startM = int(startMinute.get())

    l.grid_forget()
    l2.grid_forget()
    hourChoice.grid_forget()
    minuteChoice.grid_forget()
    startButton.grid_forget()

    currentTime = datetime.now()
    startTime = int(datetime(currentTime.year, currentTime.month, currentTime.day, startH, startM, 0).timestamp())
    clockLabel.pack(expand=True, fill='both')
    clockLabel.after(10, startCountDown)

# Initial layout for the application. Give the user a way to select the start time of the race and a big button to launch the countdown.
# This is not supposed to be "good looking". The goal is to be functionnal with as few overhead as possible.
l = Label(root, text="Start time (HH:MM):", font=fontText)
l.grid(row=0, column=0)

startHour = StringVar()
hourChoice = ttk.Combobox(root, textvariable=startHour)
hourChoice['values'] = ['{:02d}'.format(x) for x in range(24)]
hourChoice.current(9)
hourChoice.grid(row=0,column=1)

l2 = Label(root, text=":")
l2.grid(row=0, column=2)

startMinute = StringVar()
minuteChoice = ttk.Combobox(root, textvariable=startMinute)
minuteChoice['values'] = ['{:02d}'.format(x) for x in range(60)]
minuteChoice.current(0)
minuteChoice.grid(row=0,column=3)

startButton = tk.Button(root, text="START", font=fontText, command=initialise, bg='green')
startButton.grid(row=1, column=0, columnspan=4)
root.state("zoomed")
root.mainloop()
