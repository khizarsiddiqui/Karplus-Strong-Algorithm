import numpy as np
import wave, math

# creating wav file

sRate = 44100
nSamples = sRate * 5
x = np.arange(nSamples)/float(sRate)
vals = np.sin(2.0*math.pi*220.0*x)
data = np.array(vals*32767, 'int16').tostring()
file = wave.open('sine220.wav', 'wb')
file.setparams((1, 2, sRate, nSamples, 'NONE', 'uncompressed'))
file.writeframes(data)
file.close()

# The Minor Pentatonic Scale
# implementing the ring buffer with deque

from collections import deque
from collections import random

d = deque(range(10))
print(d)
deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
d.append(-1)
print(d)
deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -1])
d.popleft()
0
print (d)
deque([1, 2, 3, 4, 5, 6, 7, 8, 9, -1])

# now implemeting karplus algorithm
# generate note of given frequency

def generateNote(freq):
    nSamples = 44100
    sampleRate = 44100
    N = int(sampleRate/freq)
# initialize ring buffer
    buf = deque([random.random() - 0.5 for i in range(N)])
# initialize samples buffer
    samples = np.array([0]*nSamples, 'float32')
    for i in range(nSamples):
        samples[i] = buf[0]
        avg = 0.996*0.5*(buf[0] + buf[1])
        buf.append(avg)
        buf.popleft()
# convert samples to 16-bit values and then to a string
# the maximum value is 32767 for 16-bit
    samples = np.array(samples*32767, 'int16')
    return samples.tostring()