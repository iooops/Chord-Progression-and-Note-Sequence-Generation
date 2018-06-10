from keras.models import Sequential
from keras.callbacks import LambdaCallback
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils.data_utils import get_file
import numpy as np
import random
import matplotlib.pyplot as pyplot
import sys, os


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
print('corpus length:', len(text))
print(text[0:100])

chord_seq = text.split(' ')
chars = set(chord_seq)
text = chord_seq
print(chars)

char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))
num_chars = len(char_indices)
print('total chars:', num_chars)

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 20
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
# print('nb sequences:', len(sentences))
print(sentences)


print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1
print(x.shape)
print(y.shape)


# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(512, return_sequences=True, input_shape=(maxlen, num_chars)))
model.add(Dropout(0.2))
model.add(LSTM(512, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(num_chars))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def on_epoch_end(epoch, logs):
    # Function invoked at end of each epoch. Prints generated text.
    print()
    print('----- Generating text after Epoch: %d' % epoch)
    with open(('result' + name + '.txt'), 'w') as f_write:
        start_index = random.randint(0, len(text) - maxlen - 1)
        for diversity in [0.8, 1.0, 1.2]:
            print('----- diversity:', diversity)
            f_write.write('diversity:%4.2f\n' % diversity)

            generated = []
            sentence = text[start_index: start_index + maxlen]
            seed_sentence = sentence
            generated += sentence
            print('----- Generating with seed: ')
            print(' '.join(sentence))

            for i in range(150):
                x_pred = np.zeros((1, maxlen, len(chars)))
                for t, char in enumerate(sentence):
                    x_pred[0, t, char_indices[char]] = 1.

                preds = model.predict(x_pred, verbose=0)[0]
                next_index = sample(preds, diversity)
                next_char = indices_char[next_index]

                generated.append(next_char)
                sentence = sentence[1:]
                sentence.append(next_char)
                print(generated)
                
#                 f_write.write(' '.join(seed_sentence) + '\n')
            f_write.write(' ' .join(generated))
            f_write.write('\n\n')

            sys.stdout.flush()
            print()


print_callback = LambdaCallback(on_epoch_end=on_epoch_end)
history = model.fit(x, y,
          batch_size=128,
          epochs=10,
          callbacks=[print_callback])

pyplot.plot(history.history['loss'])
pyplot.title('model train loss')
pyplot.ylabel('loss')
pyplot.xlabel('epoch')
pyplot.legend(['train'], loc='upper right')
pyplot.show()
