import sys, os
import time, random
import wave, argparse, pygame
import math
import numpy as np
from collections import deque
import matplotlib.pyplot as plt 
# from matplotlib import pyplot as plt

# show plot of algorithm in action?
gShowPlot = False

# notes of a Pentatonic Minor scale
# piano C4-E(b)-F-G-B(b)-C5
pmNotes = {'C4': 262, 'Eb': 311, 'F': 349, 'G':391, 'Bb':466}

# Steps for simualtion
# 1. Store the first value from the ring buffer in the samples buffer.
# 2. Calculate the average of the first two elements in the ring buffer.
# 3. Multiply this average value by an attenuation factor (in this case, 0.995).
# 4. Append this value to the end of the ring buffer.
# 5. Remove the first element of the ring buffer.

# write WAVE file
def writeWAVE(fileName, data):
# open file
    file = wave.open(fileName, 'wb')
# WAV file parameters
    nChannels = 1
    sampleWidth = 2
    frameRate = 44100
    nFrames = 44100
# set parameters
    file.setparams((nChannels, sampleWidth, frameRate, nFrames, 'NONE', 'noncompressed'))
    file.writeframes(data)
    file.close()

# now implemeting karplus algorithm
# generate note of given frequency

def generateNote(freq):
    nSamples = 44100
    sampleRate = 44100
    N = int(sampleRate/freq)
# initialize ring buffer
    # line comprehension
    buf = deque([random.random() - 0.5 for i in range(N)]) 
    # plot of flag set 
    if gShowPlot:
        axline, = plt.plot(buf)
# initialize samples buffer
    samples = np.array([0]*nSamples, 'float32')
    for i in range(nSamples):
        samples[i] = buf[0]
        # Multiply value by an attenuation factor (in this case, 0.995) , (0.5 being low pass filter).
        avg = 0.995*0.5*(buf[0] + buf[1])
        buf.append(avg)
        buf.popleft()
        # plot of flag set using plt libraries
        if gShowPlot:
            if i % 1000 == 0:
                axline.set_ydata(buf)
                plt.draw()

# converting samples to 16-bit values and then to a string
# the maximum value is 32767 for 16-bit
    samples = np.array(samples * 32767, 'int16')
    return samples.tostring()

# play a wav file
class NotePlayer:
    # constructor
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        # dictionary of notes
        self.notes = {}
    # add a note
    def add(self, fileName):
        self.notes[fileName] = pygame.mixer.Sound(fileName)
    # play a note
    def play(self, fileName):
        try:
            self.notes[fileName].play()
        except:
            print(fileName + 'not found!')
    def playRandom(self):
        """play a random note"""
        # selects a random integer from the range [0, 4]
        index = random.randint(0, len(self.notes)-1)
        note = list(self.notes.values())[index]
        note.play()
    
# main() function
def main():
    # declare global var
    global gShowPlot

    parser = argparse.ArgumentParser(description="Generating sounds with Karplus String Algorithm.")
    # add arguments
    parser.add_argument('--display', action='store_true', required=False)
    parser.add_argument('--play', action='store_true', required=False)
    parser.add_argument('--piano', action='store_true', required=False)
    args = parser.parse_args()

    # show plot if flag set
    if args.display:
        gShowPlot = True
        plt.ion()

    # create note player
    nplayer = NotePlayer()

    print('creating notes...')
    for name, freq in list(pmNotes.items()):
        fileName = name + '.wav' 
        if not os.path.exists(fileName) or args.display:
            data = generateNote(freq) 
            print('creating ' + fileName + '...')
            writeWAVE(fileName, data) 
        else:
            print('fileName already created. skipping...')
        
        # add note to player
        nplayer.add(name + '.wav')
        
        # play note if display flag set
        if args.display:
            nplayer.play(name + '.wav')
            time.sleep(0.5)
    
    # play a random tune
    if args.play:
        while True:
            try: 
                nplayer.playRandom()
                # rest - 1 to 8 beats
                rest = np.random.choice([1, 2, 4, 8], 1, 
                                        p=[0.15, 0.7, 0.1, 0.05])
                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                exit()

    # random piano mode
    if args.piano:
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.KEYUP):
                    print("key pressed")
                    nplayer.playRandom()
                    time.sleep(0.5)
  
# call main
if __name__ == '__main__':
    main()
