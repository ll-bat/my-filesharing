from functools import cached_property
from .config import Config
from mss import mss
import pickle, zlib, numpy as np


class Helper:
    @staticmethod
    def compress(bytes):
        return zlib.compress(bytes)

    @staticmethod
    def decompress(bytes):
        return zlib.decompress(bytes)


class ScreenshotHelper:
    mss = None 

    def __init__(self):
        self.mss = mss() 
        self.mss.compression_level = 15

    @cached_property 
    def monitor(cls):
        return cls.mss.monitors[0]

    def get_screenshot(self):
        screenshot = self.mss.grab(self.monitor)
        np_array = np.array(screenshot)
        return np_array


class BytesReceiver:
    server = None 

    def __init__(self, server) -> None:
        self.server = server 
        self.delimeter = pickle.dumps(Config.delimeter)
        self.bytes_chunks = [] 

    @property
    def have_one_complete_file_bytes(self):
        if not len(self.bytes_chunks):
            return False 

        return self.delimeter in self.bytes_chunks[-1]

    def get_full_file_bytes(self):
        while not self.have_one_complete_file_bytes:
            bytes_chunk = self.server.receive_bytes() 
            if not bytes_chunk:
                continue
            self.bytes_chunks.append(bytes_chunk)
            
        last_bytes_chunk = self.bytes_chunks.pop() 
        last_bytes_chunk_parts = last_bytes_chunk.split(self.delimeter)
        self.bytes_chunks.append(last_bytes_chunk_parts[0])

        full_bytes = b''.join(self.bytes_chunks)
        self.bytes_chunks = [self.delimeter.join(last_bytes_chunk_parts[1:])]
        return full_bytes

    def __iter__(self):
        return self 

    def __next__(self):
        return self.get_full_file_bytes()  