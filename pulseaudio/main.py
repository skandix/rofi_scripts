#! /home/skandix/.local/share/virtualenvs/pulseaudio-CZoqxHDT/bin/python


from rofi import Rofi
import pulsectl
import re

r = Rofi()
sinks =  {}

def init_pulse():
    return pulsectl.Pulse('rofi_sinks')

# detect the sinks (sound_cards)
def detect_sinks():
    pulse = init_pulse()
    pattern = re.compile('description=')

    for sink in pulse.sink_list():
        sink = str(sink).split(',')
        desc = re.sub(pattern, '', sink[0]).replace("'","")
        index = int(sink[1].replace(' index=', ''))
        sinks.update({index:desc})

# programs id for setting the default output
def get_sink_inputs():
    pulse = init_pulse()
    pattern = re.compile('index=')

    for sink in (pulse.sink_input_list()):
        sink = str(sink).split(',')
        sink_inputs = re.sub(pattern, '', sink[0]).replace("'","")
        yield int(sink_inputs)

# select outputs from rofi, return index to set_default_output
def rofi_select():
    index, key = r.select('Pick a sink', sinks.values())
    return (index, key)

# move all active inputs from current output to the one that's choose with rofi
def set_default_output(key):
    pulse = init_pulse()

    for ids in get_sink_inputs():
        pulse.sink_input_move((ids), key)

def name2id(rofi_index):
    for key, value in enumerate(sinks.items()):
        if rofi_index == key:
            return (value[0])

if __name__ ==  '__main__':
    detect_sinks()
    rofi_index, rofi_key = rofi_select()
    key = (name2id(rofi_index))
    set_default_output(key)
