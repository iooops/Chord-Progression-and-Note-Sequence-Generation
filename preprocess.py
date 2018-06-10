import os, sys
import midi

if (len(sys.argv) == 0):
  print("Please specify the input midi file.")
  sys.exit(0)
else:
  if (sys.argv[1][-4:] != '.mid'):
    print("Please provide a valid midi file.")
    sys.exit(0)

path = sys.argv[1]
head, name = os.path.split(path)
name = name[:-4]
pattern = midi.read_midifile(path)
chunk_str_list = []

chunk_str = "rs_" + str(pattern.resolution)
chunk_str_list.append(chunk_str)

for p in pattern:
  for i, chunk in enumerate(p):

    chunk_str = ""

    if (chunk.name == "Note On"):
      chunk_str = chunk_str + str(chunk.tick) + "_" + "no" + "_" + str(chunk.pitch) + \
                    "_" + str(chunk.velocity)

      chunk_str_list.append(chunk_str)

    elif (chunk.name == "Note Off"):
      chunk_str = chunk_str + str(chunk.tick) + "_" + "noff" + "_" + str(chunk.pitch) + "_" + str(chunk.velocity)
      chunk_str_list.append(chunk_str)

    elif (chunk.name == "Set Tempo"):
      chunk_str = chunk_str + str(chunk.tick) + "_" + "st" + "_" + str(int(chunk.bpm)) + "_" + str(int(chunk.mpqn))
      chunk_str_list.append(chunk_str)

    elif (chunk.name == "Control Change"):
      chunk_str = chunk_str + str(chunk.tick) + "_" + "cc" + "_" + str(chunk.channel)  + "_" + \
                      str(chunk.data[0]) + "_" + str(chunk.data[1])
      chunk_str_list.append(chunk_str)


if not os.path.exists("./miditext/"):
  os.mkdir("./miditext/")
  os.mkdir("./miditext/original/")
elif not os.path.exists("./miditext/original/"):
  os.mkdir("./miditext/original/")

f = open("./miditext/original/" + name + '.txt', 'w')
for elm in chunk_str_list:
  f.write(str(elm) + " ")
f.close()