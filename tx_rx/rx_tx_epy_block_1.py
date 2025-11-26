import numpy as np
from gnuradio import gr
import struct

class packet_deframer(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name='Custom Packet Deframer',
            in_sig=[np.uint8],  # Input: Stream of bits (0 or 1)
            out_sig=None)       # Output: None (We write to file directly)

        # 1. CONSTANTS
        # Sync Word: 0x1D0F3E9A -> Binary: 0001 1101 0000 1111 0011 1110 1001 1010
        self.sync_seq = [0,0,0,1, 1,1,0,1, 0,0,0,0, 1,1,1,1, 
                         0,0,1,1, 1,1,1,0, 1,0,0,1, 1,0,1,0]
        
        self.state = 0 # 0=Searching, 1=Reading Length, 2=Reading Payload
        self.buffer = [] # Holds bits
        self.payload_len_bits = 0
        self.file_out = open("output_image.bin", "wb") # Output file

    def work(self, input_items, output_items):
        in0 = input_items[0]
        
        for bit in in0:
            # === STATE 0: SEARCHING FOR SYNC WORD ===
            if self.state == 0:
                self.buffer.append(bit)
                # Keep buffer only as long as the sync word
                if len(self.buffer) > 32:
                    self.buffer.pop(0)
                
                # Check if buffer matches sync word
                if self.buffer == self.sync_seq:
                    # Found it! Switch to reading length
                    self.state = 1
                    self.buffer = [] # Clear buffer to start collecting length bits
                    print("Sync found! Reading Length...")

            # === STATE 1: READING LENGTH (32 bits) ===
            elif self.state == 1:
                self.buffer.append(bit)
                if len(self.buffer) == 32:
                    # Convert 32 bits -> Integer
                    # We repack bits into bytes
                    length_bytes = self.bits_to_bytes(self.buffer)
                    # Unpack 4 bytes as Big Endian Unsigned Int
                    self.payload_len_bytes = struct.unpack('>I', length_bytes)[0]
                    self.payload_len_bits = self.payload_len_bytes * 8
                    
                    print(f"Packet Length: {self.payload_len_bytes} bytes")
                    
                    self.state = 2
                    self.buffer = [] # Clear buffer to collect payload

            # === STATE 2: READING PAYLOAD ===
            elif self.state == 2:
                self.buffer.append(bit)
                if len(self.buffer) == self.payload_len_bits:
                    # We have the full packet!
                    payload_data = self.bits_to_bytes(self.buffer)
                    
                    # Write to file
                    self.file_out.write(payload_data)
                    self.file_out.flush() # Ensure it saves immediately
                    
                    print(f"Saved {len(payload_data)} bytes.")
                    
                    # Reset to search for next packet
                    self.state = 0
                    self.buffer = []

        return len(in0)

    def bits_to_bytes(self, bits):
        # Helper to turn list of [0,1,0,1...] into bytes
        # Assumes MSB first
        byte_array = bytearray()
        for i in range(0, len(bits), 8):
            chunk = bits[i:i+8]
            val = 0
            for b in chunk:
                val = (val << 1) | b
            byte_array.append(val)
        return byte_array