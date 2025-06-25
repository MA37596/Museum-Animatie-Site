from gpiozero import Button
from pynput.keyboard import Controller, Key
import time

# Pin nummers (BCM) - PAS DEZE AAN NAAR JOUW AANSLUITINGEN
BUTTON_PIN_Z = 17  # GPIO17
BUTTON_PIN_X = 27  # GPIO27
BUTTON_PIN_C = 22  # GPIO22

keyboard = Controller()

# Knopobjecten
btn_z = Button(BUTTON_PIN_Z, bounce_time=0.05)
btn_x = Button(BUTTON_PIN_X, bounce_time=0.05)
btn_c = Button(BUTTON_PIN_C, bounce_time=0.05)

def press_key(key_char):
    """Drukt een toets in en laat deze direct los."""
    keyboard.press(key_char)
    keyboard.release(key_char)
    print(f"Gedrukt: {key_char}")

# Event handlers
btn_z.when_pressed = lambda: press_key('z')
btn_x.when_pressed = lambda: press_key('x')
btn_c.when_pressed = lambda: press_key('c')

# Main loop
try:
    print("Klaar! Druk op de knoppen...")
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nScript gestopt.")
