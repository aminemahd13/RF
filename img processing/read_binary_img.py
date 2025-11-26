from PIL import Image
import numpy as np
import os

# 1. Settings (MUST MATCH TRANSMITTER EXACTLY)
script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(script_dir, "recv_data.bin") # The file from GNU Radio File Sink
WIDTH = 225
HEIGHT = 225
CHANNELS = 3  # RGB

# 2. Calculate expected size
expected_bytes = WIDTH * HEIGHT * CHANNELS

# 3. Read the Data
with open(INPUT_FILE, "rb") as f:
    data = f.read()

# 4. Handle Data Loss (Padding)
# If we lost packets, the file is too short. We pad it with black pixels so it opens.
# 5. Reconstruct and Show
try:
    img = Image.frombytes('RGB', (WIDTH, HEIGHT), data)
    img.show()
    img.save("img_output.png")
except Exception as e:
    print(f"Error reconstructing: {e}")