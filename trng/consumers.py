from ctypes import c_uint32
import struct
import collections
from channels.generic.websocket import WebsocketConsumer
from . import logger

class TrngConsumer(WebsocketConsumer):
    buffer: collections.deque[c_uint32] = collections.deque(maxlen=1000000)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # Convert bytes to unsigned int
            random_number: c_uint32 = struct.unpack('<I', bytes_data)[0]
            # Add the random number to the buffer
            TrngConsumer.buffer.appendleft(random_number)
            self.send("Random number received")
        elif text_data:
            logger.info(f"Received text data: {text_data}")
            pass
        else:
            logger.info("Received unidentified data")
            pass