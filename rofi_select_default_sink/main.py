from rofi import Rofi
import pulsectl
import re

r = Rofi()
sinks =  []

# init pulseaudio
def init_pulse():
    return pulsectl.Pulse('rofi_sinks')

# detect the sinks (sound_cards)
def detect_sinks():
    pulse = init_pulse()
    pattern = re.compile(u'description=')
    for k in pulse.sink_list():
        k = str(k).split(',')
        desc = re.sub(pattern, '', k[0]).replace("'","") #ghetto sshit
        sinks.append(desc)

# programs id for setting the default output
def get_sink_inputs():
    pulse = init_pulse()
    pattern  = re.compile(u'index=')

    for k in (pulse.sink_input_list()):
        k = str(k).split(',')
        sink_inputs = re.sub(pattern, '', k[0]).replace("'","")
        yield int(sink_inputs)

# select outputs from rofi, return index to set_default_output
def rofi_select():
    outputs = r.select('Pick a sink', sinks)
    return (outputs)

def set_default_output(key):
    pulse = init_pulse()
    key = int(key)
    for ids in  get_sink_inputs():
        # pactl move-sink-input prod_id index_sink
        (pulse.sink_input_move(ids, key))

if __name__ ==  '__main__':
    detect_sinks()
    key, index = rofi_select()
    set_default_output(key)

