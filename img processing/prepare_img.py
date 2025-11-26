from PIL import Image
import numpy as np

# 1. Settings
INPUT_IMAGE = "./img processing/img.jpeg"
OUTPUT_FILE = "img_data.bin"
WIDTH = 225  # Keep it small for radio testing!
HEIGHT = 225

# 2. Open and Resize
img = Image.open(INPUT_IMAGE)
img = img.resize((WIDTH, HEIGHT))
img = img.convert('RGB')  # Force 3 channels (Red, Green, Blue)

# 3. Convert to Raw Bytes
# This creates a flat array: R, G, B, R, G, B...
raw_data = np.array(img).tobytes()

# 4. Save to .bin file
with open(OUTPUT_FILE, "wb") as f:
    f.write(raw_data)

print(f"Done! File size: {len(raw_data)} bytes.")
print(f"REMEMBER THESE DIMENSIONS: {WIDTH}x{HEIGHT}")