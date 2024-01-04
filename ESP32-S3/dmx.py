"""SPI based CircuitPython DMX transmitter"""
import busio

import asyncio

BREAK = b'\x00\x00\x00' # 3 x 8 x 4µS = 96µS
MAB = '111' # 3 x 4µs = 12µs
SLOT_0 = '00000000011' # 1 bit start(0), 8 bits (0), 2 stop (1) 


class universe():
    def __init__(self, sck, mosi):
        """DMX SPI initialisation"""
        self.spi = busio.SPI(sck, MOSI=mosi)
        self.background_task = None
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=250000, bits=8)

    def octet(self, byte):
        """Convert a byte to string of digits"""
        binary = bin(byte)[2:]
        while len(binary) < 8:
            binary = '0' + binary
        return binary

    async def background_send(self,msg):
        while True:
            self.spi.write(msg)
            await asyncio.sleep(0.01)
            
    async def start_background_send(self,msg):
        task = asyncio.create_task(self.background_send(msg))
        return task

    async def stop_background_send(self):
        self.background_task.cancel()
        try:
            await self.background_task
        except asyncio.CancelledError:
            pass

    async def send(self, data):
        """Send DMX chanels values from bytes to DMX signal via MOSI"""
        data_bytes_start_stop = ''.join(['0' + self.octet(byte) + '11' for byte in data])
        result = MAB + SLOT_0 + data_bytes_start_stop
        result += '1' * ((8 - len(result) % 8) % 8)  # Ajout de "1" pour obtenir un multiple de 8
        # Convert to bytes
        result_bytes = int(result, 2).to_bytes(len(result) // 8, 'big')
        msg = BREAK + result_bytes
        if self.background_task is not None:
            await self.stop_background_send()
        self.background_task = await self.start_background_send(msg)




