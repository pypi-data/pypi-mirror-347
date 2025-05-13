from typing import BinaryIO, Generator
import os
import htfbox as hbox



class Password:
    def __init__(self, password:str):
        self.password :str = password
        self.bpass :bytes = password.encode()
        self.index = 0

    def reset(self):
        self.index = 0
    
    def next(self) -> int:
        value = self.bpass[self.index]
        self.index = (self.index + 1) % len(self.bpass)
        return value
    
    def roll_next(self, value:int, dir:int=1) -> int:
        return (value + self.next()*dir) % 256



# --- PACKER

def pack_file(pxd_file:BinaryIO, rel_path:str, source_path:str, password:Password=None):

    if password: password.reset()

    # HEADER
    pxd_file.write( f"EF\0".encode()         ) # File
    pxd_file.write( f"{rel_path}\0".encode() ) # Path

    # CONTENT
    source_size = os.path.getsize(source_path)
    pxd_file.write( source_size.to_bytes(8, "big") ) # Source Size

    with open(source_path, "rb") as source:
        for _ in range(0, source_size):
            
            # process byte
            b = source.read(1)[0]
            if password:
                b = password.roll_next(b)

            # write to file
            pxd_file.write(bytes([b]))



def pack_dir(pxd_file:BinaryIO, rel_path:str):
    
    # HEADER
    pxd_file.write( f"ED\0".encode()         ) # Directory
    pxd_file.write( f"{rel_path}\0".encode() ) # Path



def pack_all(path:str, pxd_path:str, password:Password) -> Generator[tuple[str, str], None, None]:
    """Pack everything located in the folder
    Yields: (str)path, (str)type"""

    # INFO
    pxd_file = open(pxd_path, "wb")
    elder = os.path.split(path)[1]
    pack_dir(pxd_file, elder)

    # DIRECTORIES
    for rel in hbox.dirs.walk_rel(path, True, False):

        rel = os.path.join(elder, rel)
        pack_dir(pxd_file, rel)

        yield rel, "dir"
    
    # FILES
    for rel in hbox.dirs.walk_rel(path, False, True):

        source_path = os.path.join(path, rel)
        rel = os.path.join(elder, rel)
        pack_file(pxd_file, rel, source_path, password)

        yield rel, "file"
    
    pxd_file.close()



# FREE

def free_entry(pxd_file:BinaryIO, where:str, password:Password=None, read_only=False) -> tuple[str, str]:

    if password: password.reset()

    # HEADER
    entry_type = read_to_null(pxd_file, True)
    rel_path   = read_to_null(pxd_file, True)
    full_path =  os.path.join(where, rel_path)

    # What is it?
    match entry_type:

        # FILE
        case "EF":

            # READ AND WRITE CONTENT
            content_size = int.from_bytes(pxd_file.read(8))

            if not read_only:
                with open(full_path, "wb") as f:
                    for b in read_max(pxd_file, content_size):
                        if password:
                            b = password.roll_next(b, -1)
                        f.write(bytes([b]))

            else:
                pxd_file.seek(pxd_file.tell() + content_size)
            
            return rel_path, "file"
        
        # DIRECTORY
        case "ED":
            if not read_only:
                os.makedirs(full_path, exist_ok=True)
            return rel_path, "dir"



def free_all(pxd_path:str, where:str, password:Password=None, read_only=False) -> Generator[tuple[str, str], None, None]:

    pxd_file = open(pxd_path, "rb")

    while not is_eof(pxd_file):
        path, etype = free_entry(pxd_file, where, password, read_only)
        yield path, etype
    
    pxd_file.close()



# --- HELPERS

def read_to_null(stream:BinaryIO, to_str:bool=False) -> bytes|str:
    binary = bytearray()

    while True:
        b = stream.read(1)
        if b==b"\0" or not b: break
        binary.append(b[0])
    
    result = bytes(binary)
    if to_str: result = result.decode()
    return result



def read_max(stream:BinaryIO, count:int) -> Generator[int, None, None]:
    for _ in range(count):
        b = stream.read(1)
        if not b: return
        yield b[0]



def is_eof(stream:BinaryIO) -> bool:
    pos = stream.tell()
    eof = not stream.read(1)
    stream.seek(pos)
    return eof



def count_entries(path:str) -> int:
    total = 0
    for _, _ in free_all(path, "", None, True): total += 1
    return total