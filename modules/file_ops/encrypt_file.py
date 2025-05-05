import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
import base64

MODULE_NAME = "Encrypt File"
MODULE_DESCRIPTION = "Encrypts files with AES-256-CBC (requires decryption module)"

def get_key(password: str, salt: bytes) -> bytes:
    """Derive a 32-byte encryption key from password and salt"""
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000,  # PBKDF2 iterations
        dklen=32  # 32 bytes = 256 bits
    )

def encrypt_file(input_file: str, output_file: str, password: str) -> None:
    """Encrypt a file using AES-256-CBC with PBKDF2 key derivation"""
    # Generate random salt
    salt = Random.get_random_bytes(16)
    
    # Derive encryption key
    key = get_key(password, salt)
    
    # Generate random IV
    iv = Random.get_random_bytes(16)
    
    # Create cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Read and encrypt file
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    # Pad the data to be multiples of 16 bytes (AES block size)
    padded_data = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    
    # Write salt + iv + ciphertext to output file
    with open(output_file, 'wb') as f:
        f.write(salt)
        f.write(iv)
        f.write(ciphertext)

def run():
    """Main encryption interface"""
    import curses
    import os
    
    # Initialize curses
    stdscr = curses.initscr()
    curses.echo()
    
    try:
        stdscr.clear()
        stdscr.addstr(0, 0, "=== File Encryption ===")
        
        # Get input file
        stdscr.addstr(2, 0, "Enter file to encrypt: ")
        input_file = stdscr.getstr().decode('utf-8')
        
        if not os.path.exists(input_file):
            stdscr.addstr(4, 0, "Error: File not found!", curses.A_BOLD)
            stdscr.getch()
            return
        
        # Get output file
        stdscr.addstr(4, 0, "Enter output filename: ")
        output_file = stdscr.getstr().decode('utf-8')
        
        # Get password
        stdscr.addstr(6, 0, "Enter encryption password: ")
        password = stdscr.getstr().decode('utf-8')
        
        if not password:
            stdscr.addstr(8, 0, "Error: Password cannot be empty!", curses.A_BOLD)
            stdscr.getch()
            return
        
        # Perform encryption
        try:
            encrypt_file(input_file, output_file, password)
            stdscr.addstr(8, 0, f"Success! File encrypted to: {output_file}", curses.A_BOLD)
            stdscr.addstr(10, 0, "IMPORTANT: Remember the password - it's required for decryption!", curses.A_BOLD | curses.color_pair(2))
        except Exception as e:
            stdscr.addstr(8, 0, f"Encryption failed: {str(e)}", curses.A_BOLD)
        
        stdscr.addstr(12, 0, "Press any key to return to main menu...")
        stdscr.getch()
        
    finally:
        curses.endwin()