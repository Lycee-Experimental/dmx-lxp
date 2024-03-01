"""SPI based CircuitPython DMX transmitter"""
import busio
import asyncio

BREAK = b'\x00\x00\x00' # 3 x 8 x 4µS = 96µS
MAB = '111' # 3 x 4µs = 12µs
SLOT_0 = '00000000011' # 1 bit start(0), 8 bits (0), 2 stop (1)


class universe():
    def __init__(self, sck, mosi):
        """DMX SPI initialisation"""
        self.spi = busio.SPI(sck, mosi)
        self.data = b'\x00'*512
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=250000, bits=8, polarity=1)
        asyncio.create_task(self.send_dmx())

    def byte_to_string(self, byte):
        """Convert a byte to a string of 8 digits"""
        string = bin(byte)[2:]
        while len(string) < 8:
            string = '0' + string
        return string

    def change_data(self, data):
        """Set the DMX databyte signal from channels values"""
        # MAB+SLOT_0+concatenate channels adding starts (0) and stop (11)
        result = MAB + SLOT_0 + ''.join(['0' + self.byte_to_string(byte) + '11' for byte in data]) 
        # Add 1 to the end to obtain a multiple of 8 digits
        result += '1' * ((8 - len(result) % 8) % 8)  
        # Convert string of digits to bytes
        result_bytes = int(result, 2).to_bytes(len(result) // 8, 'big')
        # Set the new DMX databyte to be sent
        self.data = BREAK + result_bytes

    async def send_dmx(self):
        """Send the DMX message every 100ms"""
        while True:
            self.spi.write(self.data)
            await asyncio.sleep(0.1)
