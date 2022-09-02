import numpy as np
import wave, math

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