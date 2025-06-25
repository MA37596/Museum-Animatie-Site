#!/usr/bin/env python3
import time
import lgpio
from evdev import UInput, ecodes as e

# ==================================================
# CONFIGURATIE
# ==================================================
BUTTON_PIN_Z = 17
BUTTON_PIN_X = 27
BUTTON_PIN_C = 22
DEBOUNCE_DELAY = 0.2

# ==================================================
# GPIO INITIALISATIE
# ==================================================
h = lgpio.gpio_chip_open(0)  # Open GPIO chip
for pin in [BUTTON_PIN_Z, BUTTON_PIN_X, BUTTON_PIN_C]:
    lgpio.gpio_claim_input(h, pin)

# ==================================================
# MAIN LOOP
# ==================================================
try:
    with UInput({e.EV_KEY: [e.KEY_Z, e.KEY_X, e.KEY_C]}, name="RaspberryPi Arcade Buttons") as ui:
        print("Klaar! Druk op de knoppen (Z/X/C)... (CTRL+C om te stoppen)")

        while True:
            if lgpio.gpio_read(h, BUTTON_PIN_Z) == 0:
                ui.write(e.EV_KEY, e.KEY_Z, 1)
                ui.syn()
                ui.write(e.EV_KEY, e.KEY_Z, 0)
                ui.syn()
                time.sleep(DEBOUNCE_DELAY)

            if lgpio.gpio_read(h, BUTTON_PIN_X) == 0:
                ui.write(e.EV_KEY, e.KEY_X, 1)
                ui.syn()
                ui.write(e.EV_KEY, e.KEY_X, 0)
                ui.syn()
                time.sleep(DEBOUNCE_DELAY)

            if lgpio.gpio_read(h, BUTTON_PIN_C) == 0:
                ui.write(e.EV_KEY, e.KEY_C, 1)
                ui.syn()
                ui.write(e.EV_KEY, e.KEY_C, 0)
                ui.syn()
                time.sleep(DEBOUNCE_DELAY)

            time.sleep(0.01)

except KeyboardInterrupt:
    print("\nStoppen...")
finally:
    lgpio.gpio_chip_close(h)
