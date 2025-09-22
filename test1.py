import time
import random
import binascii # For hex conversion
from typing import Optional
def encrypt(data: bytes, key: bytes) -> bytes:
    """Encrypt/Decrypt data using XOR with the given key."""
    # XOR is symmetric, so the same function decrypts.
    return bytes(a ^ b for a, b in zip(data, key))

def generate_key(length: int, seed: Optional[float] = None) -> bytes:
    """Generate a random key of given length using the provided seed."""
    if seed is not None:
        random.seed(int(seed)) # The server uses int(seed)
    return bytes(random.randint(0, 255) for _ in range(length))

# The encrypted flag provided
ENCRYPTED_FLAG_HEX = "df1bafa5cf121d7114974356107e866277489c28507e00241ce6d5b2c3ca0dc55e12dac7213b"
ENCRYPTED_FLAG_BYTES = binascii.unhexlify(ENCRYPTED_FLAG_HEX)

FLAG_LENGTH = len(ENCRYPTED_FLAG_BYTES) # Should be 32

# Common flag prefixes to check for
FLAG_PREFIXES = [b'flag{'] # Add any other known prefixes

def solve():
    # Get current timestamp
    # We'll search around this time.
    # The server might have started a bit earlier, or there might be clock skew.
    # So, search a window around the current time.
    now = int(time.time())

    # Search window: e.g., 2 minutes before to 10 seconds after current time
    # Adjust this range if the flag isn't found
    search_start_time = now - 120  # Try timestamps from 2 minutes ago
    search_end_time = now + 10    # To 10 seconds in the future (to account for latency/skew)

    print(f"Searching for flag with key generated around {time.ctime(search_start_time)} to {time.ctime(search_end_time)}")

    for timestamp_candidate in range(search_start_time, search_end_time + 1):
        # Generate the key with the candidate timestamp
        key_candidate = generate_key(FLAG_LENGTH, timestamp_candidate)
        
        # Decrypt the flag with the generated key
        decrypted_flag_attempt = encrypt(ENCRYPTED_FLAG_BYTES, key_candidate)
        
        # Check if the decrypted flag starts with a known prefix
        for prefix in FLAG_PREFIXES:
            if decrypted_flag_attempt.startswith(prefix):
                try:
                    # Attempt to decode to ASCII or UTF-8 if it looks like text
                    # Flags are usually ASCII or UTF-8 compatible
                    print(f"Found flag with timestamp: {timestamp_candidate} ({time.ctime(timestamp_candidate)})")
                    print(f"Decrypted Flag (bytes): {decrypted_flag_attempt}")
                    print(f"Decrypted Flag (text): {decrypted_flag_attempt.decode('utf-8')}")
                    return decrypted_flag_attempt.decode('utf-8')
                except UnicodeDecodeError:
                    print(f"Found flag with timestamp: {timestamp_candidate} ({time.ctime(timestamp_candidate)}) but could not decode to text. Raw bytes: {decrypted_flag_attempt}")
                    return decrypted_flag_attempt
    
    print("Flag not found within the specified timestamp range.")
    return None

if __name__ == "__main__":
    flag = solve()
    if flag:
        print(f"\nFinal Flag: {flag}")
    else:
        print("\nCould not find the flag.")