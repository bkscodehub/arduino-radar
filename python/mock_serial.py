import random
import time
import math

class MockSerial:
    def __init__(self, port=None, baudrate=9600, timeout=None):
        self.angle = 0
        self.direction = 1  # 1 for forward, -1 for backward

    def readline(self):
        # Simulate angle sweep from 0 to 180 and back
        if self.angle >= 180:
            self.direction = -1
        elif self.angle <= 0:
            self.direction = 1

        self.angle += self.direction

        # Simulate distance: e.g., a sine wave + some noise
        distance = 20 + 300 * math.sin(math.radians(self.angle)) + random.uniform(-3, 3)
        distance = max(1, min(500, int(distance)))

        data_str = f"{self.angle},{distance}\n"
        time.sleep(0.03)  # Simulate delay
        return data_str.encode()  # Return bytes like real serial

    def close(self):
        pass
