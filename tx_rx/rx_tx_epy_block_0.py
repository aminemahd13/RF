import numpy as np
from gnuradio import gr
import struct

class packet_framer(gr.basic_block):
    def __init__(self):
        gr.basic_block.__init__(self,
            name='Custom Packet Framer',
            in_sig=[np.uint8],
            out_sig=[np.uint8])
        
        # 1. CONSTANTS
        self.payload_size = 256  # Must match your "Stream to Tagged Stream"
        # Preamble (4 bytes 0x55) + Sync (4 bytes) + Length (4 bytes)
        # 0x1D0F3E9A
        self.header_bytes = [0x55, 0x55, 0x55, 0x55, 
                             0x1D, 0x0F, 0x3E, 0x9A] 
        
        # We pre-calculate the length bytes since your packet size is fixed at 256
        # 256 in hex is 0x00000100
        self.len_bytes = list(struct.pack('>I', self.payload_size))
        
        self.full_header = self.header_bytes + self.len_bytes
        self.header_len = len(self.full_header)
        self.total_packet_len = self.header_len + self.payload_size

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        # We need enough input to make a payload, and enough output space to write the full packet
        if len(in0) >= self.payload_size and len(out) >= self.total_packet_len:
            
            # 1. Write Header
            out[:self.header_len] = self.full_header
            
            # 2. Write Payload (Copy 256 bytes from input)
            out[self.header_len : self.total_packet_len] = in0[:self.payload_size]
            
            # 3. Tell GNU Radio what we did
            self.consume(0, self.payload_size) # We ate 256 bytes
            return self.total_packet_len       # We produced 268 bytes
            
        # If we don't have enough data yet, do nothing and wait for more
        return 0