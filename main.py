import curses
import yaml
import importlib
import os
from pathlib import Path

class MultiTool:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.config = self.load_config()
        self.columns = self.config['columns']
        self.current_column = 0
        self.current_row = 0
        self.module_cache = {}
        
        # Initialize curses
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.highlight_color = curses.color_pair(1)
        self.normal_color = curses.A_NORMAL
        self.ascii_art_color = curses.color_pair(2)
        self.desc_color = curses.color_pair(3)
        
        self.load_current_column_modules()
    
    def load_config(self):
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    
    def load_current_column_modules(self):
        column = self.columns[self.current_column]
        folder = column['folder']
        
        if folder in self.module_cache:
            return self.module_cache[folder]
        
        modules = []
        module_dir = Path(__file__).parent / 'modules' / folder
        
        for file in module_dir.glob('*.py'):
            if file.name == '__init__.py':
                continue
                
            module_name = file.stem
            module_path = f"modules.{folder}.{module_name}"
            
            try:
                module = importlib.import_module(module_path)
                modules.append({
                    'name': getattr(module, 'MODULE_NAME', module_name),
                    'description': getattr(module, 'MODULE_DESCRIPTION', 'No description'),
                    'run': getattr(module, 'run', lambda: None)
                })
            except Exception as e:
                modules.append({
                    'name': module_name,
                    'description': f"Error loading: {str(e)}",
                    'run': None
                })
        
        self.module_cache[folder] = modules
        return modules
    
    def draw_ascii_art(self, start_y):
        ascii_art = [
            " █████╗  █████╗  █████╗ ███████╗",
            "██╔══██╗██╔══██╗██╔══██╗╚══███╔╝",
            "╚█████╔╝╚█████╔╝╚█████╔╝  ███╔╝ ",
            "██╔══██╗██╔══██╗██╔══██╗ ███╔╝  ",
            "╚█████╔╝╚█████╔╝╚█████╔╝███████╗",
            " ╚════╝  ╚════╝  ╚════╝ ╚══════╝"
        ]
        
        for i, line in enumerate(ascii_art):
            self.stdscr.addstr(start_y + i, (curses.COLS - len(line)) // 2, line, self.ascii_art_color)
    
    def draw_divider(self, y_pos, width):
        self.stdscr.addstr(y_pos, 0, "─" * width, curses.A_BOLD)
    
    def draw_menu(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        
        # Calculate layout positions
        art_height = 6
        art_start_y = 2
        info_start_y = art_start_y + art_height + 1
        desc_start_y = info_start_y + 4
        
        # Draw ASCII art
        self.draw_ascii_art(art_start_y)
        
        # Draw Discord info
        discord_info = "discord.gg/888z"
        dev_info = "developed by @320.888 @349.888 @369.888"
        self.stdscr.addstr(info_start_y, (width - len(discord_info)) // 2, discord_info, curses.A_BOLD)
        self.stdscr.addstr(info_start_y + 1, (width - len(dev_info)) // 2, dev_info, curses.A_DIM)
        
        # Draw top divider before description
        self.draw_divider(desc_start_y, width)
        
        # Draw description section
        current_module = self.get_current_module()
        desc_title = "DESC:"
        self.stdscr.addstr(desc_start_y + 1, 2, desc_title, curses.A_BOLD | self.desc_color)
        
        if current_module:
            # Split description into multiple lines if too long
            desc_lines = []
            desc = current_module['description']
            max_line_length = width - 4
            
            while len(desc) > max_line_length:
                space_pos = desc.rfind(' ', 0, max_line_length)
                if space_pos == -1:
                    space_pos = max_line_length
                desc_lines.append(desc[:space_pos])
                desc = desc[space_pos+1:]
            desc_lines.append(desc)
            
            for i, line in enumerate(desc_lines):
                if desc_start_y + 2 + i >= height - 6:  # Leave space for menu
                    break
                self.stdscr.addstr(desc_start_y + 2 + i, 2, line, self.desc_color)
        
        # Draw bottom divider after description
        self.draw_divider(desc_start_y + 3 + len(desc_lines), width)
        
        # Draw menu options below description section
        menu_start_y = desc_start_y + 5 + len(desc_lines)
        col_width = width // len(self.columns)
        
        for idx, column in enumerate(self.columns):
            x_pos = idx * col_width + 2
            color = self.highlight_color if idx == self.current_column else self.normal_color
            self.stdscr.addstr(menu_start_y, x_pos, column['name'], color)
            
            if idx == self.current_column:
                modules = self.load_current_column_modules()
                for i, module in enumerate(modules):
                    row_pos = menu_start_y + 2 + i
                    if row_pos >= height - 2:
                        break
                        
                    color = self.highlight_color if i == self.current_row else self.normal_color
                    self.stdscr.addstr(row_pos, x_pos, f" {module['name']} ", color)
        
        # Draw footer at the actual bottom
        footer = "↑/↓: Navigate | ←/→: Switch columns | ENTER: Select | q: Quit"
        self.stdscr.addstr(height - 1, 0, footer[:width-1], curses.A_DIM)
        
        self.stdscr.refresh()
    
    def get_current_module(self):
        modules = self.load_current_column_modules()
        if modules and 0 <= self.current_row < len(modules):
            return modules[self.current_row]
        return None
    
    def run_module(self, module):
        """Run a module and return to menu when done"""
        self.stdscr.clear()
        self.stdscr.refresh()
        
        try:
            # Some modules might need curses initialized
            curses.endwin()
            
            # Run the module function
            if module['run']:
                module['run']()
            
        except Exception as e:
            # Restore curses window to show error
            self.stdscr = curses.initscr()
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, f"Error in module: {str(e)}", curses.A_BOLD | curses.color_pair(1))
            self.stdscr.refresh()
            self.stdscr.getch()
        
        # Always return to curses mode
        self.stdscr = curses.initscr()
        curses.curs_set(0)
    
    def run(self):
        while True:
            self.draw_menu()
            key = self.stdscr.getch()
            
            modules = self.load_current_column_modules()
            
            if key == curses.KEY_DOWN and self.current_row < len(modules) - 1:
                self.current_row += 1
            elif key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_RIGHT and self.current_column < len(self.columns) - 1:
                self.current_column += 1
                self.current_row = 0
                self.load_current_column_modules()
            elif key == curses.KEY_LEFT and self.current_column > 0:
                self.current_column -= 1
                self.current_row = 0
                self.load_current_column_modules()
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if modules and self.current_row < len(modules):
                    selected_module = modules[self.current_row]
                    self.run_module(selected_module)
            elif key == ord('q'):
                break

def main(stdscr):
    app = MultiTool(stdscr)
    app.run()

if __name__ == "__main__":
    curses.wrapper(main)