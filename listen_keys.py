import os
import time
import datetime
# from pynput.keyboard import Key, Listener, KeyCode
import keyboard

table_path = os.path.join('data', 'dog.csv')

# initialize table
line = 'time,key'
if not os.path.exists(table_path):
    with open(table_path, 'w') as table:
        table.write(line)

global releaseListening
keepListening = True

def key_press(key):
    print(key.name)
    if key.name == 'esc':
        # Stop listener
        keepListening = False
    now = datetime.datetime.now()
    if key.name in ['0', '1', '2']:
        with open(table_path, 'a') as table:
            line = ','.join([str(x) for x in [now, key.name]])
            print("added line: ", line)
            table.write('\n'+line)

keyboard.on_press(key_press)

# Collect events until released
while keepListening:
    time.sleep(1)
