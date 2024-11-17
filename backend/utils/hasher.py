import hashlib

class CustomHasher:
    @staticmethod
    def truncate_hash(password: str, length: int = 8) -> str:
        """Truncating method - takes first n characters of hash"""
        full_hash = hashlib.sha256(password.encode()).hexdigest()
        return full_hash[:length]
    
    @staticmethod
    def folding_hash(password: str, chunk_size: int = 4) -> str:
        """Folding method - splits string into chunks and combines them"""
        full_hash = hashlib.sha256(password.encode()).hexdigest()
        chunks = [full_hash[i:i+chunk_size] for i in range(0, len(full_hash), chunk_size)]
        folded = 0
        for chunk in chunks:
            if chunk:
                folded ^= int(chunk, 16)
        return hex(folded)[2:]
    
    @staticmethod
    def open_hash(password: str, attempt: int = 0) -> str:
        """Open hashing method - adds attempt number to handle collisions"""
        return hashlib.sha256(f"{password}{attempt}".encode()).hexdigest()