import serial
import time
import random
from python_tools.pixmob_conversion_funcs import bits_to_arduino_string
from python_tools.effect_definitions import base_color_effects, tail_codes, special_effects
import python_tools.config as cfg
import asyncio
from aalink import Link

# This file lets you send a series of light effect commands with customizable timings over IR by way of an Arduino
# connected to this computer running one of the PixMob_Transmitter sketches in the arduino_sender folder. Theoretically
# you could program this to be in sync with a song or something.

# It is recommended you familiar yourself with the "demo_single_effect.py" script before trying this.

# Set the ALL_CAPS parameters below and run the script. Also set ARDUINO_SERIAL_PORT and
# ARDUINO_BAUD_RATE in python_tools/config.py

# List of all effects you want to display, in order. Each entry has the effect name, optional tail code, and
# duration to wait before sending next effect. Note that some effects are long, and the bracelets might not respond
# to an effect until the current one is finished, so don't set your durations to less than the time it takes for the
# bracelets to show the effects.
EFFECTS_TO_SHOW = [
    "RED",
    "GREEN",
    "BLUE",
    "TURQUOISE",
    "YELLOW",
    "MAGENTA",
    "SLOW_ORANGE",
]


#################################

def get_random_effect():
    # return random string from EFFECTS_TO_SHOW
    return random.choice(EFFECTS_TO_SHOW)

arduino = serial.Serial(port=cfg.ARDUINO_SERIAL_PORT, baudrate=cfg.ARDUINO_BAUD_RATE, timeout=.1)
print(arduino)

def send_effect(main_effect, tail_code):
    if main_effect in base_color_effects:
        effect_bits = base_color_effects[main_effect]
        if tail_code:
            if tail_code in tail_codes:
                effect_bits = effect_bits + tail_codes[tail_code]
            else:
                raise Exception("Invalid tail code name. See tail_codes in effect_definitions.py for options.")
    elif main_effect in special_effects:
        effect_bits = special_effects[main_effect]
        if tail_code:
            raise Exception("Tail code effects only supported on simple color effects found in base_color_effects of "
                            "effect_definitions.py. Set TAIL_CODE to None or choose a MAIN_EFFECT from base_color_effects "
                            "(instead of special_effects).")
    else:
        raise Exception("Invalid MAIN_EFFECT. See base_color_effects and special_effects in effect_definitions.py for "
                        "options.")
    arduino_string_ver = bits_to_arduino_string(effect_bits)
    arduino.write(bytes(arduino_string_ver, 'utf-8'))



    # print(f"Sent effect: {main_effect}, {'no tail effect' if not tail_code else 'tail: ' + tail_code}.")

async def main():
    loop = asyncio.get_running_loop()

    link = Link(120, loop)
    link.enabled = True

    while True:
        await link.sync(1)
        effect = get_random_effect()
        send_effect("YELLOW_6", None)

asyncio.run(main())
