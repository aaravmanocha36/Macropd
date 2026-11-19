import time

import board
import keypad
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode as Media
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode as Key


# Edit these eight lines to change what the buttons do.
# Use a tuple for keys, e.g. (Key.F13,) or (Key.COMMAND, Key.S).
# Use Media.PLAY_PAUSE for a media button, "hello" to type on a US layout,
# or None to leave a button blank. For Windows/Linux, use Key.CONTROL instead.
actions = (
    (Key.COMMAND, Key.C),    # SW1: copy
    (Key.COMMAND, Key.V),    # SW2: paste
    (Key.COMMAND, Key.Z),    # SW3: undo
    (Key.COMMAND, Key.A),    # SW4: select all
    Media.MUTE,              # SW5
    Media.VOLUME_DECREMENT,  # SW6
    Media.VOLUME_INCREMENT,  # SW7
    Media.PLAY_PAUSE,        # SW8
)

# SW1 through SW8 connect GP0 through GP7 to ground when pressed.
pins = (
    board.GP0, board.GP1, board.GP2, board.GP3,
    board.GP4, board.GP5, board.GP6, board.GP7,
)
switches = keypad.Keys(pins, value_when_pressed=False, pull=True)
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
media = ConsumerControl(usb_hid.devices)

while True:
    event = switches.events.get()
    if event is None:
        time.sleep(0.005)
        continue
    if not event.pressed:
        continue

    action = actions[event.key_number]
    if isinstance(action, tuple):
        keyboard.send(*action)
    elif isinstance(action, str):
        layout.write(action)
    elif action is not None:
        media.send(action)
