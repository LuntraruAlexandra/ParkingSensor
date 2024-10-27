import time
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER, PEN_P4
from machine import ADC, PWM, Pin, Timer

# DISPLAY

display = PicoGraphics(display=DISPLAY_PICO_EXPLORER, pen_type=PEN_P4)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)
RED = display.create_pen(2500, 0, 0)

# For the blink.
on_off = 0

# Makes everything black.
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()

# Cicle list.
circles=[[120,90,90,"GREEN"],[120,100,90,"BLACK"],[120,110,90,"GREEN"],[120,120,90,"BLACK"],[120,130,90,"GREEN"],[120,140,90,"BLACK"],
        [120,150,90,"YELLOW"],[120,160,90,"BLACK"],[120,170,90,"YELLOW"],[120,180,90,"BLACK"],[120,190,90,"YELLOW"],[120,200,90,"BLACK"], 
        [120,210,90,"RED"],[120,220,90,"BLACK"],[120,230,90,"RED"],[120,240,90,"BLACK"]]

# Display the circles by the dist.

def display_circles(dist):
    # Calculate the index of circles.
    index = 0
    ind = 0
    if dist <=20:
        ind = dist / 2.5
    else:
        ind = 8
    index = 8 - int(ind)
    # Display the circles.
    display.set_pen(BLACK)
    display.rectangle(0,0,240,240)
    for i in range (2 * index, len(circles)):
        if circles[i][3] == "BLACK":
            display.set_pen(BLACK)
        if circles[i][3] == "GREEN":
            display.set_pen(GREEN)
        if circles[i][3] == "YELLOW":
            display.set_pen(YELLOW)
        if circles[i][3] == "RED":
            display.set_pen(RED)
        display.circle(circles[i][0],circles[i][1],circles[i][2])
    
    # Display triangles.
    display.set_pen(BLACK)
    display.triangle(0,0,0,240,120,240)
    display.set_pen(BLACK)
    display.triangle(240,0,120,240,240,240)
    display.update()

def blink(timer):
    global on_off
    global dist
    on_off = 1 - on_off
    if on_off == 0:
        clear()
    else:
        display_circles(dist)

timer = Timer()
trig = Pin(0, Pin.OUT)
echo = Pin(1, Pin.IN)
dist = 0
# timer.init(freq=4, mode=Timer.PERIODIC, callback=blink)

# SOUND

audio = PWM(Pin(3), freq=440, duty_u16=0)
on_off1 = 0

def bip(timer):
    global on_off1
    on_off1 = 1 - on_off1
    if on_off1 == 0:
        audio.duty_u16(30000)
    else:
        audio.duty_u16(0)

def bip_cont():
    audio.duty_u16(30000)


timer1 = Timer()
mode = 0
old_dist = 0

# MAIN
while True:
    trig.off()
    time.sleep_us(10)

    trig.on()
    time.sleep_us(5)

    trig.off()

    while echo.value() == 0:
        pass
        
    start_time = time.ticks_us()
    while echo.value() == 1:
        pass
    finish_time = time.ticks_us()

    time.sleep_ms(100)
    dist = 350 * (finish_time - start_time) / 20000
    display_circles(dist)
    if dist < 2.5 :
        display.set_font("bitmap8")
        display.set_pen(WHITE)                            
        display.text("Too Close!", 10, 10, 240, 4)
        display.set_pen(RED) 
        display.rectangle(105,50,20,120)
        display.rectangle(105, 180,20,20)
        display.update()  
    if abs(dist - old_dist) > 2.5:
        old_dist = dist
        if dist > 20:
            mode = 0
        elif dist > 15 and dist < 20 :
            mode = 1
        elif dist > 10 and dist < 15 :
            mode = 2
        elif dist > 5 and dist < 10 :
            mode = 3
        elif dist < 2.5:
            mode = 3
            

        if mode == 0:
            timer1.deinit()
            time.sleep_ms(100)
            audio.duty_u16(0)
        if mode == 1:
            timer1.init(freq=2.5, mode=Timer.PERIODIC, callback=bip)
        if mode == 2:
            timer1.init(freq=5, mode=Timer.PERIODIC, callback=bip)
        if mode == 3:
            timer1.deinit()
            bip_cont()