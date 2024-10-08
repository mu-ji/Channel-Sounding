import serial
import numpy as np
import math
import struct
import matplotlib.pyplot as plt
import binascii

import matplotlib.pyplot as plt
from math import pi, atan2, sqrt
from scipy.linalg import eig

ser = serial.Serial('COM9', 115200)

import cmath

SPEED_OF_LIGHT  = 299792458
num_iterations = 200     # 进行的循环次数
iteration = 0

rawFrame = []

all_data = {
    'I_data': [],
    'Q_data': [],
    'rssi' : [],
    'pattern' : []
}
packet_number_list = []
phase_list = []
num_samples = 88
while True:
    byte  = ser.read(1)        
    rawFrame += byte
    #print(len(rawFrame))
    if rawFrame[-3:]==[255, 255, 255]:
        if len(rawFrame) == 4*num_samples+8:
            received_data = rawFrame[:4*num_samples]
            num_samples = 88

            I_data = np.zeros(num_samples, dtype=np.int16)
            Q_data = np.zeros(num_samples, dtype=np.int16)
            for i in range(num_samples):
                (I) = struct.unpack('>h', bytes(received_data[4*i+2:4*i+4]))
                (Q) = struct.unpack('>h', bytes(received_data[4*i:4*i+2]))
                #print(phase)
                #print((received_data[4*i+2] << 8) | received_data[4*i+3])
                #phase_data[i] = (received_data[4*i+2] << 8) | received_data[4*i+3]
                I_data[i] = I[0]
                Q_data[i] = Q[0]

            I_data = I_data.astype(np.float32)
            Q_data = Q_data.astype(np.float32)

            all_data['I_data'].append(I_data)
            all_data['Q_data'].append(Q_data)
            packet_number = rawFrame[-4]
            packet_number_list.append(packet_number)
            phase_list.append(64*np.arctan(Q_data[0]/I_data[0]))
            print(packet_number)
            if len(packet_number_list) == 20:
                plt.figure()
                plt.plot(packet_number_list,phase_list,marker='*')
                plt.grid()
                plt.ylabel('phase')
                plt.xlabel('packet id')
                plt.savefig('initial_phase.png')
                plt.show()
        rawFrame = []
            
    if len(all_data['I_data']) == num_iterations:
        all_data['I_data'] = np.array(all_data['I_data'])
        all_data['Q_data'] = np.array(all_data['Q_data'])
        all_data['rssi'] = np.array(all_data['rssi'])
        all_data['pattern'] = ['42,43,44,41']

        np.savez('IQ_Raw_data/60_data.npz', **all_data)
        break
