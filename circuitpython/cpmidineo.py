# Metro M4 USB Host MIDI is connected to UART Rx

import time
import board
import neopixel
import busio

uart = busio.UART(board.TX, board.RX, baudrate=115200)

# Metro M4 has one LED
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=.2)

red_brightness = 0
green_brightness = 0
blue_brightness = 0

def pixels_update():
    #print(red_brightness, green_brightness, blue_brightness)
    pixels.fill((red_brightness, green_brightness, blue_brightness))
    pixels.show()

pixels_update()

while True:
    data = uart.read(1)
    #print(data)  # this is a bytearray type

    if data is not None:
        # if Change Control message on Channel 1
        if data[0] == 0xB0:
            control = uart.read(1)
            if control is not None:
                intensity = uart.read(1)
                if intensity is not None:
                    brightness = intensity[0] * 2
                    # Control 0 is for red
                    if control[0] == 0:
                        red_brightness = brightness
                        pixels_update()
                    # Control 1 is for green
                    elif control[0] == 1:
                        green_brightness = brightness
                        pixels_update()
                    # Control 2 is for blue
                    elif control[0] == 2:
                        blue_brightness = brightness
                        pixels_update()
