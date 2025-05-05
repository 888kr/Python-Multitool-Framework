MODULE_NAME = "Ping Tool"
MODULE_DESCRIPTION = "Ping a host to check connectivity"

def run():
    import subprocess
    import curses
    
    stdscr = curses.initscr()
    curses.echo()
    
    try:
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter host to ping: ")
        host = stdscr.getstr().decode('utf-8')
        
        stdscr.clear()
        stdscr.addstr(0, 0, f"Pinging {host}... (Press any key to stop)")
        stdscr.refresh()
        
        process = subprocess.Popen(
            ['ping', host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Non-blocking read of ping output
        while True:
            if stdscr.getch() != -1:
                process.terminate()
                break
            
            line = process.stdout.readline()
            if not line:
                break
                
            stdscr.addstr(2, 0, line.strip())
            stdscr.refresh()
            
            if process.poll() is not None:
                break
                
    finally:
        curses.endwin()