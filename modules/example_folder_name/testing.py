MODULE_NAME = "Example Tool"
MODULE_DESCRIPTION = "Demonstrates module structure"

def run():
    import curses
    stdscr = curses.initscr()
    curses.echo()
    
    try:
        stdscr.addstr(0, 0, "Hello, World!")
        stdscr.getch()
    finally:
        curses.endwin()