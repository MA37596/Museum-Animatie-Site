#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from evdev import UInput, ecodes as e

# ==================================================
# CONFIGURATIE
# ==================================================
BUTTON_PIN_Z = 17  # GPIO17 -> Z
BUTTON_PIN_X = 27  # GPIO27 -> X
BUTTON_PIN_C = 22  # GPIO22 -> C
DEBOUNCE_DELAY = 0.2  # Seconde vertraging na druk

# ==================================================
# GPIO INSTELLEN
# ==================================================
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN_Z, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN_X, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN_C, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ==================================================
# MAIN LOOP
# ==================================================
try:
    with UInput({e.EV_KEY: [e.KEY_Z, e.KEY_X, e.KEY_C]}, name="RaspberryPi Arcade Buttons") as ui:
        print("Klaar! Druk op de knoppen (Z/X/C)... (CTRL+C om te stoppen)")

        while True:
            # Z knop
            if GPIO.input(BUTTON_PIN_Z) == GPIO.LOW:
                ui.write(e.EV_KEY, e.KEY_Z, 1)  # key down
                ui.syn()
                ui.write(e.EV_KEY, e.KEY_Z, 0)  # key up
                ui.syn()
                time.sleep(DEBOUNCE_DELAY)

            # X knop
            if GPIO.input(BUTTON_PIN_X) == GPIO.LOW:
                ui.write(e.EV_KEY, e.KEY_X, 1)  # key down
                ui.syn()
                ui.write(e.EV_KEY, e.KEY_X, 0)  # key up
                ui.syn()
                time.sleep(DEBOUNCE_DELAY)

            # C knop
            if GPIO.input(BUTTON_PIN_C) == GPIO.LOW:
                ui.write(e.EV_KEY, e.KEY_C, 1)  # key down
                ui.syn()
                ui.write(e.EV_KEY, e.KEY_C, 0)  # key up
                ui.syn()
                time.sleep(DEBOUNCE_DELAY)

            time.sleep(0.01)

except KeyboardInterrupt:
    print("\nStoppen... GPIO schoonmaken.")
finally:
    GPIO.cleanup()
