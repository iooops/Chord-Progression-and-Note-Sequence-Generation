import numpy as np
import random
import sys
import os
import midi

if (len(sys.argv) == 0):
  print("Please specify the input text.")
  sys.exit(0)
else:
  if (sys.argv[1][-4:] != '.txt'):
    print("Please provide a valid text file.")
    sys.exit(0)

path = sys.argv[1]
head, name = os.path.split(path)
name = name[:-4]
text = open(path).read()
generated = text.split(' ')
resolution = 1440

if not os.path.exists("./midi/"):
  os.mkdir("./midi/")
  os.mkdir("./midi/generated/")
elif not os.path.exists("./midi/generated/"):
  os.mkdir("./midi/generated")
file = "./midi/generated/" + name + ".mid"

pattern = midi.Pattern(resolution=resolution)

track = midi.Track()
pattern.append(track)

for chunk in generated:
  chunk_info = chunk.split("_")
  event_type = chunk_info[1]

  if event_type == "no":
    tick = int(chunk_info[0])
    pitch = int(chunk_info[2])
    velocity = int(chunk_info[3])

    e = midi.NoteOnEvent(tick=tick, channel=0, velocity=velocity, pitch=pitch)
    track.append(e)

  elif event_type == "st":
    tick = int(chunk_info[0])
    bpm = int(chunk_info[2])
    mpqn = int(chunk_info[3])
    ev = midi.SetTempoEvent(tick=tick, bpm=bpm, mpqn=mpqn)
    track.append(ev)

  elif event_type == "cc":
    control = int(chunk_info[3])
    value = int(chunk_info[4])
    e = midi.ControlChangeEvent(channel=0, control=control, value=value)
    track.append(e)

end_event = midi.EndOfTrackEvent(tick=1)
track.append(end_event)

midi.write_midifile(file, pattern)