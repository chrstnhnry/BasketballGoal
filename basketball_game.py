from Tkinter import *
import time
import RPi.GPIO as GPIO
from time import sleep
import pygame
pygame.init()
#Libraries
#import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 19

swish = pygame.mixer.Sound("Good Shot.wav")
pygame.mixer.music.load('Good Shot.wav')
cena = pygame.mixer.Sound("Darude.wav")
pygame.mixer.music.load("Darude.wav")
pygame.mixer.Sound.stop(cena)




#pygame.mixer.music.play(-1)


GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)



rootWindow = Tk()
rootWindow.title('Hoops')
rootWindow.wm_attributes('-fullscreen', 'true')
rootWindow.geometry("800x650")
rootWindow.resizable(0,0)


defaultColour = rootWindow.cget("bg")


photo = PhotoImage(file = 'flaming.png')
label = Label(rootWindow, image=photo)
label.grid(row = 1,column = 2, columnspan = 3, sticky = NSEW)




time1 = ''
prevSec = ''

secs = 24

running = False
Time = Label(rootWindow, text = "Time:", font = ('fixed',60, 'bold'), fg = 'chocolate1')
Time.grid(row = 1, column = 0, sticky= W)
Score = Label(rootWindow, text = "Status:", font = ('fixed', 65, 'bold', 'underline'), fg = 'red2')
Score.grid(row = 5, column = 1, sticky = NSEW)




#clock = Label(rootWindow, font=('fixed', 20, 'bold'))
clock = Label(rootWindow, font=('fixed', 50, 'bold'))
clock.grid(row = 1, column = 1, padx = 1, pady = (6,2))
score = Label(rootWindow, font=('fixed', 35, 'italic', 'bold'),fg = 'black')
score.grid(row = 6, column = 1, padx = 5, pady = (5,2))


def distance():
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance



def start_btn():
    global running
    clock.config('bg')
    btn_start.config(state='disabled',background=defaultColour)
    btn_stop.config(state='normal',bg='red2')
    btn_reset.config(state='disabled', bg = defaultColour)
    score.config(text = '')
    running = True

def stop_btn():
    global running
    clock.config('bg')
    btn_start.config(state='normal',bg='green2')
    btn_stop.config(state='disabled',bg=defaultColour)
    btn_reset.config(state='normal', bg = 'turquoise1')
    score.config(text = '')

    running = False

def reset_btn():
    global Score1, prevSec, time1, secs, running
    clock.config(bg=defaultColour)

    secs = 24
    prevSec = ''
    time1 = ''
    running = False
    btn_stop.config(state='disabled',bg=defaultColour)
    btn_start.config(state='normal',bg='green2')
    btn_reset.config(state='disabled', bg = defaultColour)

btn_reset = Button(rootWindow,font=('fixed', 30, 'bold'),state='disabled', text = 'Reset',command = reset_btn)
btn_reset.grid(row = 2, column = 2)
btn_start = Button(rootWindow,font=('fixed', 30, 'bold'), text = 'Start', bg='green2', command = start_btn)
btn_start.grid(row = 2,column = 0, columnspan = 1, sticky = EW)
btn_stop = Button(rootWindow,font=('fixed', 30, 'bold'),state='disabled', text = 'Stop', command = stop_btn)
btn_stop.grid(row = 2, column = 1, sticky = EW)


def tick():
    global Score, prevSec, time1, secs, running, time2
    # get the current local time from the PC
    #time2 = time.strftime('%Y/%m/%d %H:%M:%S')

    if running:

        newSec = time.strftime('%S')
        if __name__ == '__main__':
            dist = distance()


        if dist < 10:
            score.config(text = 'Made It! :)')
            pygame.mixer.Sound.play(swish)
            GPIO.output(20,GPIO.HIGH)
            GPIO.output(21,GPIO.HIGH)
            GPIO.output(22,GPIO.HIGH)
            GPIO.output(23,GPIO.HIGH)
            GPIO.output(24,GPIO.HIGH)
            GPIO.output(25,GPIO.HIGH)
            GPIO.output(26,GPIO.HIGH)
            GPIO.output(27,GPIO.HIGH)









        elif (secs == 0):
            score.config(text = 'Game Over')
            running = False
            GPIO.output(20,GPIO.LOW)
            GPIO.output(21,GPIO.LOW)
            GPIO.output(22,GPIO.LOW)
            GPIO.output(23,GPIO.LOW)
            GPIO.output(24,GPIO.LOW)
            GPIO.output(25,GPIO.LOW)
            GPIO.output(26,GPIO.LOW)
            GPIO.output(27,GPIO.LOW)



        else:
            score.config(text = 'Shoot :o')
            GPIO.output(20,GPIO.LOW)
            GPIO.output(21,GPIO.LOW)
            GPIO.output(22,GPIO.LOW)
            GPIO.output(23,GPIO.LOW)
            GPIO.output(24,GPIO.LOW)
            GPIO.output(25,GPIO.LOW)
            GPIO.output(26,GPIO.LOW)
            GPIO.output(27,GPIO.LOW)






    else:
        newSec = ''
        prevSec = ''


    if newSec != prevSec:
        prevSec = newSec
        secs = secs - 1
        if secs < 0:
            secs = 0
            clock.config(bg='red')
            score.config(text = 'Game Over')


    time2 = '%02d' % (secs)
    time3 = secs
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(200, tick)
pygame.mixer.Sound.play(cena)
tick()

rootWindow.mainloop()
