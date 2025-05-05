import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto import Random
import base64

MODULE_NAME = "Decrypt File"
MODULE_DESCRIPTION = "Decrypts files encrypted with the encryption module"

def get_key(password: str, salt: bytes) -> bytes:
    """Derive the 32-byte encryption key from password and salt"""
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000,  # PBKDF2 iterations
        dklen=32  # 32 bytes = 256 bits
    )

def decrypt_file(input_file: str, output_file: str, password: str) -> None:
    """Decrypt a file encrypted with our encryption module"""
    with open(input_file, 'rb') as f:
        # Read salt (first 16 bytes)
        salt = f.read(16)
        
        # Read IV (next 16 bytes)
        iv = f.read(16)
        
        # Read remaining ciphertext
        ciphertext = f.read()
    
    # Derive encryption key
    key = get_key(password, salt)
    
    # Create cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Decrypt and unpad
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    # Write decrypted data
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

def run():
    """Main decryption interface"""
    import curses
    import os
    
    # Initialize curses
    stdscr = curses.initscr()
    curses.echo()
    
    try:
        stdscr.clear()
        stdscr.addstr(0, 0, "=== File Decryption ===")
        
        # Get input file
        stdscr.addstr(2, 0, "Enter file to decrypt: ")
        input_file = stdscr.getstr().decode('utf-8')
        
        if not os.path.exists(input_file):
            stdscr.addstr(4, 0, "Error: File not found!", curses.A_BOLD)
            stdscr.getch()
            return
        
        # Get output file
        stdscr.addstr(4, 0, "Enter output filename: ")
        output_file = stdscr.getstr().decode('utf-8')
        
        # Get password
        stdscr.addstr(6, 0, "Enter decryption password: ")
        password = stdscr.getstr().decode('utf-8')
        
        if not password:
            stdscr.addstr(8, 0, "Error: Password cannot be empty!", curses.A_BOLD)
            stdscr.getch()
            return
        
        # Perform decryption
        try:
            decrypt_file(input_file, output_file, password)
            stdscr.addstr(8, 0, f"Success! File decrypted to: {output_file}", curses.A_BOLD)
        except Exception as e:
            stdscr.addstr(8, 0, f"Decryption failed: {str(e)}", curses.A_BOLD)
            stdscr.addstr(10, 0, "Possible causes: Wrong password or corrupted file", curses.color_pair(2))
        
        stdscr.addstr(12, 0, "Press any key to return to main menu...")
        stdscr.getch()
        
    finally:
        curses.endwin()