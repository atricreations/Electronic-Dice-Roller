from neopixel import Neopixel
from char_set import char_set
import time
from machine import Pin,ADC,Timer
import random
from config import ones_color, tens_color,sel_color

random.seed()

battery_voltage = ADC(Pin(26))

roll_btn = Pin(4, Pin.IN, machine.Pin.PULL_UP)

switch_btn = Pin(22, Pin.IN, machine.Pin.PULL_UP)

vref = 2.5

n_pixels = 35

pixels = Neopixel(35, 0, 0, "GRB")
pixels_2 = Neopixel(35, 1, 1, "GRB")
pixels_3 = Neopixel(7, 2, 2, "GRB")

# start the timer
start = time.ticks_ms()
debounce_timer = time.ticks_ms()
display_timer = time.ticks_ms()
event_triggered = False

#Display interrupt 60hz/16ms:
def interruption_handler(timer):
    pixels.show()
    pixels_2.show()
    pixels_3.show()
    
show_display = Timer(mode=Timer.PERIODIC, period=16, callback=interruption_handler)
    

#display_vars:
ones = "0"
tens = "0"
value = 0
sel = 0
sleeping = False
display_update = True

button_pressed = None
d_list = [4,6,8,10,12,20,100]

#state_vars:
mode = "roller"
def animation_speckle(n_frames,max_brightness):
    
    for x in range(n_frames):
        for i in range(n_pixels):
            brightness = max_brightness * random.random() 
            pixels.set_pixel(i,[random.random() * brightness,random.random() * brightness,random.random() * brightness])
            pixels_2.set_pixel(i,[random.random() * brightness,random.random() * brightness,random.random() * brightness])
            #pixels.show()
            #pixels_2.show()
def mode_roller(button_pressed):
    global sel
    global ones
    global tens

    if button_pressed==22:
        sel = sel+1
        if sel > 6:
            sel=0
    if button_pressed==4:
        animation_speckle(25,15)
        value =  random.randrange(1, d_list[sel]+1)
        if value == 100:
            value=0
        ones=chr(value%10 +48)
        tens=chr(int(value/10)+48)
def mode_life_counter(button_pressed):
    global value
    global ones
    global tens
    if button_pressed==22:
        value=value+1
    if button_pressed==4:
        value=value-1
    print(value)
    ones=chr(value%10 +48)
    tens=chr(int(value/10)+48)
def process_button(button_pressed):
    global start
    global d_list
    global mode
    
    print("hi")
    print(button_pressed)

    #look for double click
    delta = time.ticks_diff(time.ticks_ms(), start)
    start = time.ticks_ms() # get millisecond counter
    if delta < 300:
        double_click=True
        
    if mode == "roller":
        mode_roller(button_pressed)
    if mode == "life_counter":
        mode_life_counter(button_pressed)
    # Update display:
    draw_char(ones, pixels,ones_color)
    draw_char(tens, pixels_2,tens_color)
        
    pixels_3.clear()
    pixels_3.set_pixel(sel,sel_color)
    print("hi")
    
    
def button_callback(p):
    global debounce_timer
    global button_pressed

    #Disable interrupts and start debounce timer.
    button_pressed = None
    debounce_timer = time.ticks_ms()

    roll_btn.irq(handler=None)
    switch_btn.irq(handler=None)


def draw_char(char, display,color):
    for i,line in enumerate(char_set[char]):
        for pixel in range(5):
            if (line >> (4 - pixel%5) & 0x1) == 0x1:
                display.set_pixel(pixel + i*5,color)
            else:
                display.set_pixel(pixel+ i*5,[0,0,0])
    #display.show()



while(1):
    sample_button = time.ticks_diff(time.ticks_ms(), debounce_timer)
    if sample_button > 2000:
        if switch_btn.value() == 0:
            debounce_timer = time.ticks_ms()
            if mode == "roller":
                value = 39
                mode = "life_counter"
            else:
                mode = "roller"
            process_button(22)
    #Sample the button after debounce expires.       
    if sample_button > 30:     
        if switch_btn.value() == 0:
            button_pressed = 22
        elif roll_btn.value() == 0:
            button_pressed = 4
        #on rising edge, reenable interrupts
        elif switch_btn.value() == 1 or roll_btn.value() == 1:
            roll_btn.irq(trigger=Pin.IRQ_FALLING, handler=button_callback)
            switch_btn.irq(trigger=Pin.IRQ_FALLING, handler=button_callback)
            button_pressed = None
            event_triggered = False
            
        if button_pressed != None and not event_triggered:
            process_button(button_pressed)
            event_triggered = True
            sleeping = False
            
            
    if sample_button > 8000 and button_pressed == None and sleeping == False:
        print("sleepy time")
        pixels.clear()
        pixels_2.clear()
        pixels_3.clear()
        sleeping = True
        

def display_test():
    for x in range(100):
        pot_value = battery_voltage.read_u16() # read value, 0-65535 across voltage range 0.0v - 3.3v
        voltage = vref/65535 * pot_value * 2
        print(pot_value)
        print(voltage)
        ones=chr(x%10 +48)
        tens=chr(int(x/10)+48)
        draw_char(ones, pixels,[2,7,4])
        draw_char(tens, pixels_2,[5,5,0])
        time.sleep(.1)            
