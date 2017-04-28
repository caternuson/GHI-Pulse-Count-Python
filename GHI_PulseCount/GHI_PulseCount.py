import RPi.GPIO as IO
IO.setwarnings(False)
IO.setmode(IO.BCM)

# GPIO Pins
CNT_EN = 22

# MDR0 configuration data - the configuration byte is formed with
# single segments taken from each group and ORing all together.

# Count modes
NQUAD = 0x00          # non-quadrature mode
QUADRX1 = 0x01        # X1 quadrature mode
QUADRX2 = 0x02        # X2 quadrature mode
QUADRX4 = 0x03        # X4 quadrature mode

# Running modes
FREE_RUN = 0x00
SINGE_CYCLE = 0x04
RANGE_LIMIT = 0x08
MODULO_N = 0x0C

# Index modes
DISABLE_INDX = 0x00   # index_disabled
INDX_LOADC = 0x10     # index_load_CNTR
INDX_RESETC = 0x20    # index_rest_CNTR
INDX_LOADO = 0x30     # index_load_OL
ASYNCH_INDX = 0x00    # asynchronous index
SYNCH_INDX = 0x80     # synchronous index

# Clock filter modes
FILTER_1 = 0x00       # filter clock frequncy division factor 1
FILTER_2 = 0x80       # filter clock frequncy division factor 2

# MDR1 configuration data; any of these
# data segments can be ORed together

# Flag modes
NO_FLAGS = 0x00       # all flags disabled
IDX_FLAG = 0x10       # IDX flag
CMP_FLAG = 0x20       # CMP flag
BW_FLAG = 0x40        # BW flag
CY_FLAG = 0x80        # CY flag

# 1 to 4 bytes data-width
BYTE_4 = 0x00         # four byte mode
BYTE_3 = 0x01         # three byte mode
BYTE_2 = 0x02         # two byte mode
BYTE_1 = 0x03         # one byte mode

# Enable/disable counter
EN_CNTR = 0x00        # counting enabled
DIS_CNTR = 0x04       # counting disabled

# LS7366R op-code list
CLR_MDR0 = 0x08
CLR_MDR1 = 0x10
CLR_CNTR = 0x20
CLR_STR = 0x30
READ_MDR0 = 0x48
READ_MDR1 = 0x50
READ_CNTR = 0x60
READ_OTR = 0x68
READ_STR = 0x70
WRITE_MDR1 = 0x90
WRITE_MDR0 = 0x88
WRITE_DTR = 0x98
LOAD_CNTR = 0xE0
LOAD_OTR = 0xE4

class GHI_PulseCount(object):
    """GHI PulseCounter."""

    def __init__(self, spi=None, **kwargs):
        # Configure GPIO
        IO.setup(CNT_EN, IO.OUT)
        IO.output(CNT_EN, IO.HIGH)
        
        # Setup SPI interface.
        if spi is None:
            import spidev
            spi = spidev.SpiDev()
            spi.open(0,0)
        self.spi = spi
    
    def get_cntr(self, ):
        '''Get counts from CNTR.'''
        bytes = self.spi.xfer2([READ_CNTR,0x00,0x00,0x00,0x00])
        return bytes[1]<<24 | bytes[2]<<16 | bytes[3]<<8 | bytes[4]
    
    def get_otr(self, ):
        '''Get counts from OTR.'''
        bytes = self.spi.xfer2([READ_OTR,0x00,0x00,0x00,0x00])
        return bytes[1]<<24 | bytes[2]<<16 | bytes[3]<<8 | bytes[4]
    
    def clear_str(self, ):
        '''Clear the status register.'''
        self.spi.writebytes([CLR_STR])
        
    def clear_cntr(self, ):
        '''Clear the counter.'''
        self.spi.writebytes([CLR_CNTR])
    
    def clear_mdr0(self, ):
        '''Clear MDR0.'''
        self.spi_writebytes([CLR_MDR0])

    def enable_cntr(self, ):
        '''Enable counting.'''
        IO.output(CNT_EN, IO.HIGH)
        
    def disable_cntr(self,):
        '''Disable counting.'''
        IO.output(CNT_EN, IO.LOW)