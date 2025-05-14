from typing import Literal, Generator
import packer

class Paxed:
    def __init__(self, path:str, mode:Literal["r", "w"], password:packer.Password|str=None):
        self.stream = open(path, mode+"b")
        self.mode = mode
        self.path = path
        self.password = password
        if password:
            if isinstance(password, str):
                password = packer.Password(password)
        
        f, d = self.count_entries()
        self.entry_count = f+d
        self.file_count = f
        self.dir_count = d

    def close(self) -> None:
        self.stream.close()

    # // Write

    def add_file(self, source_path:str, rel_path:str) -> None:
        self.__check_mode("w")
        packer.pack_file(self.stream, source_path, rel_path, self.password)
        self.file_count += 1

    def pack_dir(self, rel_path:str) -> None:
        self.__check_mode("w")
        packer.pack_dir(self.stream, rel_path)

    def pack_all(self, source_path:str) -> Generator[tuple[str, str], None, None]:
        self.__check_mode("w")

        for path, etype in packer.pack_all(source_path, self.path, self.password):
            yield path, etype
    
    # // Read

    def free_entry(self, where:str) -> tuple[str, str]:
        self.__check_mode("r")
        return packer.free_entry(self.stream, where, self.password)

    def free_all(self, where:str) -> Generator[tuple[str, str], None, None]:
        self.__check_mode("r")
        for path, etype in packer.free_all(self.stream, where, self.password):
            yield path, etype
    
    def count_entries(self) -> tuple[int, int]:
        return packer.count_entries(self.path)


    # // Other

    def is_eof(self) -> bool:
        return packer.is_eof(self.stream)
    
    # // Private

    def __check_mode(self, target_mode:str=Literal["w", "r"], raise_error:bool=True) -> bool:
        
        match target_mode:

            # WRITE
            case "w":
                if self.mode != "w":
                    if raise_error:
                        raise IOError("Not in WRITE mode")
                    return False
                return True
            
            # READ
            case "r":
                if self.mode != "r":
                    if raise_error:
                        raise IOError("Not in READ mode")
                    return False
                return True