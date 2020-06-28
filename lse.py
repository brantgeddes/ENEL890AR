import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Target sample rate
sample_rate = 660
# Target frequency
input_frequency = 60
# Maximum allowable condition
max_condition = 10
# Data source path
data_source = 'Q3Data.csv'

# Change data_source variable to load different dataset
data = pd.read_csv(data_source, sep=",", skiprows=2, usecols=["Qn"]).to_numpy()


# calculates real coefficients
def real_coef(dt):
    return math.sin(2 * math.pi * input_frequency * dt * (1/sample_rate))
# calculates imaginary coefficients
def imag_coef(dt):
    return math.cos(2 * math.pi * input_frequency * dt * (1/sample_rate))
# Builds coefficient matrix based on required window
def build_matrix(window):
    matrix = np.empty((0, 4))
    for i in range(int(-window/2), int(window/2) + 1, 1):
        matrix = np.vstack((matrix, [real_coef(i), imag_coef(i), 1, -i]))
    return matrix
# Start with window of size 5
A = build_matrix(5)
# If size=5 window doesn't have required condition, loop until condition is less than max_condition, 
# or until the size of the window is equal to the length of the input data
i = 7
while np.linalg.cond(A) > max_condition and i < len(data):
    A = build_matrix(i)
    i += 2
print("Window Size: " + str(i))
FL = len(A)
A = np.linalg.pinv(A)
print("Condition: " + str(np.linalg.cond(A)))


# initialize empty arrays
real = np.array([])
imag = np.array([])
dc = np.array([])
decay = np.array([])

# Pad dataset with zeros
data = np.append([0] * FL, data)
# Loop through and perform a dot product between the coefficient matrix and the data window
for n in range(int(FL/2), len(data) - int(FL/2) + 1):
    if (n + int(FL/2) + 1 <= len(data)):
        real = np.append(real, A[0] @ data[n - int(FL/2) : n + int(FL/2) + 1])
        imag = np.append(imag, A[1] @ data[n - int(FL/2) : n + int(FL/2) + 1])
        dc = np.append(dc, A[2] @ data[n - int(FL/2) : n + int(FL/2) + 1])
        decay = np.append(decay, A[3] @ data[n - int(FL/2) : n + int(FL/2) + 1])

# Lambdas to calculate amplitude and phase
amplitude = list(map(lambda x,y: (x**2 + y**2)**(1/2), real, imag))
phase = list(map(lambda x,y: math.atan(y/x), real, imag))

# Save coefficients as csv for easy import into excel
np.savetxt('Q_coeff.csv', A, delimiter=",")

# Plot function, amplitude and phase, dc component, and decay component
plt.subplot(2, 2, 1)
plt.title('Signal')
plt.plot(range(len(data)), data)
plt.subplot(2, 2, 3)
plt.title('Amplitude/Phase')
plt.plot(range(len(amplitude)), amplitude)
plt.plot(range(len(phase)), phase)
plt.subplot(2, 2, 2)
plt.title('DC Component')
plt.plot(range(len(dc)), dc)
plt.subplot(2, 2, 4)
plt.title('Decaying DC Component')
plt.plot(range(len(decay)), decay)
plt.show()