import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Target sample rate
sample_rate = 480
# Data source path
data_source = 'Q1Data.csv'

# Change data_source variable to load different dataset
data = pd.read_csv(data_source, sep=",", skiprows=2, usecols=["Qn"]).to_numpy()

# Number of data points
N = len(data)
# Empty arrays
real = np.array([])
imag = np.array([])

# Loop through all buckets
for k in range(N):
    realV = 0
    imagV = 0
    # Perform a correlation for each bucket
    for n in range(N):
        realV += (1 / N) * data[n] * math.cos(2 * math.pi * n * k / N)
        imagV += (1 / N) * data[n] * math.sin(2 * math.pi * n * k / N)
    # Append correllation coefficients to the current bucket
    real = np.append(real, realV) 
    imag = np.append(imag, imagV)

print(real[0])
# Lambdas to solve amplitude and phase
amplitude = list(map(lambda x,y: 2 * (x**2 + y**2)**(1/2), real, imag))
phase = list(map(lambda x,y: math.atan(y/x), real, imag))

plt.subplot(3, 1, 1)
plt.title('Function')
plt.plot(range(N), data)
# Scale DFT buckets to Fs/2 frequency range
f_axis = list(range(int(N/2) + 1))
f_axis = list(map(lambda x: (x/N) * sample_rate, f_axis))
plt.subplot(3, 1, 2)
plt.title('Amplitude')
plt.plot(f_axis, amplitude[:int(N/2) + 1])
plt.subplot(3, 1, 3)
plt.title('Phase')
plt.plot(f_axis, phase[:int(N/2) + 1])
plt.show()
