import matplotlib.pyplot as plt
import numpy as np
import time
import os
from collections import deque
import imageio
import platform

#from serial import Serial
from mock_serial import MockSerial  # Replace with Serial(...) for real data

# Configuration
RANGE_MAX = 500  # cm
THRESHOLD_DISTANCE = 30  # cm for beep
FADE_TIME = 1  # seconds
CAPTURE_FRAMES = True
FRAME_INTERVAL = 0.1  # seconds
frame_images = []

# For sound alert
def play_beep():
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 100)
    else:
        os.system('play -nq -t alsa synth 0.1 sine 880')  # Linux/Mac

# Serial Setup
#ser = Serial('COM5', 9600, timeout=1)
ser = MockSerial()
time.sleep(2)

# Radar Plot Setup
plt.ion()
fig = plt.figure(figsize=(8, 8))
fig.patch.set_facecolor('black')
ax = fig.add_subplot(111, polar=True)
ax.set_facecolor('black')
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_rmax(RANGE_MAX)
ax.grid(color='white')
ax.tick_params(colors='white')

# Data buffer
data_points = deque()

last_frame_time = time.time()

while True:
    try:
        line = ser.readline().decode().strip()
        if ',' in line:
            angle_str, dist_str = line.split(',')
            angle = int(angle_str)
            distance = int(dist_str)
            angle_rad = np.radians(angle)
            timestamp = time.time()

            # Append point
            data_points.append((angle_rad, distance, timestamp))

            # Play beep if within threshold
            if distance < THRESHOLD_DISTANCE:
                play_beep()

            # Console log
            print(f"Angle: {angle}°, Distance: {distance} cm")

            # Cleanup old points
            data_points = deque(
                [pt for pt in data_points if timestamp - pt[2] <= FADE_TIME]
            )

            # Prepare for plotting
            angles = [pt[0] for pt in data_points]
            distances = [pt[1] for pt in data_points]
            ages = [timestamp - pt[2] for pt in data_points]
            
            #colors = [(0, 1, 0, max(0, 1 - (age / FADE_TIME))) for age in ages]
            colors = []
            for i in range(len(data_points)):
                age = ages[i]
                dist = distances[i]
                alpha = max(0, 1 - (age / FADE_TIME))
                if dist < THRESHOLD_DISTANCE:
                    colors.append((1, 0, 0, alpha))  # Red for close objects
                else:
                    colors.append((0, 1, 0, alpha))  # Green otherwise


            # Clear and redraw
            ax.clear()
            ax.set_facecolor('black')
            ax.set_theta_zero_location("N")
            ax.set_theta_direction(-1)
            ax.set_rmax(RANGE_MAX)
            ax.grid(color='white')
            ax.tick_params(colors='white')
            ax.scatter(angles, distances, c=colors, s=50)

            # Sweep line
            ax.plot([angle_rad, angle_rad], [0, RANGE_MAX], color='lime', linewidth=2, alpha=0.5)

            # Optional: Add center dot
            ax.plot(0, 0, 'o', color='white', markersize=4)

            plt.pause(0.001)

            # Save frames for export
            if CAPTURE_FRAMES and (timestamp - last_frame_time >= FRAME_INTERVAL):
                fig.canvas.draw()
                image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
                image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
                frame_images.append(image)
                last_frame_time = timestamp

    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print(f"Error: {e}")

ser.close()

# Save video or GIF
if CAPTURE_FRAMES and frame_images:
    output_file = 'radar_output.gif'
    imageio.mimsave(output_file, frame_images, fps=int(1 / FRAME_INTERVAL))
    print(f"\nSaved radar animation to {output_file}")
