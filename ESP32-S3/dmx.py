"""SPI based CircuitPython DMX transmitter"""
import busio

BREAK = b'\x00\x00\x00' # 3 x 8 x 4µS = 96µS
MAB = '111' # 3 x 4µs = 12µs
SLOT_0 = '00000000011' # 1 bit start(0), 8 bits (0), 2 stop (1) 


class universe():
    def __init__(self, sck, mosi):
        """DMX SPI initialisation"""
        self.spi = busio.SPI(sck, MOSI=mosi)
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=250000, bits=8)

    def octet(self, byte):
        """transforme un byte en string représentant l'octet"""
        binary = bin(byte)[2:]
        while len(binary) < 8:
            binary = '0' + binary
        return binary

    def send(self, data):
        """Send DMX chanels values from bytes to DMX signal via MOSI"""
        data_bytes_start_stop = ''.join(['0' + self.octet(byte) + '11' for byte in data])
        result = MAB + SLOT_0 + data_bytes_start_stop
        result += '1' * ((8 - len(result) % 8) % 8)  # Ajout de "1" pour obtenir un multiple de 8
        # Convert to bytes
        result_bytes = int(result, 2).to_bytes(len(result) // 8, 'big')
        msg = BREAK + result_bytes
        self.spi.write(msg)




