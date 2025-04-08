import serial
import matplotlib.pyplot as plt
import numpy as np
import time
from mock_serial import MockSerial  # if it's in another file

# Configure serial connection (adjust 'COM3' to your Arduino port, e.g., '/dev/ttyACM0' on Linux)
#ser = serial.Serial('COM5', 9600, timeout=1)
ser = MockSerial()
time.sleep(2)

# Set up polar plot
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.set_rmax(500)  # Maximum range in cm (adjust as needed)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)

fade_time = 1  # Time in seconds for a point to fade completely
data_points = []  # List to store tuples: (angle_rad, distance, timestamp)

while True:
    try:
        # Read serial line and parse data
        line = ser.readline().decode().strip()
#        print(line)
        if ',' in line:
            angle_str, dist_str = line.split(',')
            angle = int(angle_str)
            distance = int(dist_str)
            angle_rad = np.radians(angle)
            timestamp = time.time()
            # Append new data point (angle in radians, distance, timestamp)
            data_points.append((angle_rad, distance, timestamp))
        
        # Remove points older than fade_time seconds
        current_time = time.time()
        data_points = [pt for pt in data_points if current_time - pt[2] <= fade_time]
        
        # Extract lists for plotting
        angles = [pt[0] for pt in data_points]
        distances = [pt[1] for pt in data_points]
        ages = [current_time - pt[2] for pt in data_points]  # Age of each point
        
        # Compute RGBA colors: Using green (0, 1, 0) and adjusting the alpha
        colors = [(0, 1, 0, max(0, 1 - (age / fade_time))) for age in ages]

        # Redraw the polar plot
        ax.clear()
        ax.set_rmax(100)
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.scatter(angles, distances, c=colors, s=50)
        plt.pause(0.001)
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")

ser.close()
