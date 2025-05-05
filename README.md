
# **Python Multi-Tool Framework**  
*A customizable TUI (Terminal User Interface) framework for organizing and running Python scripts.*  

---

## **📖 Table of Contents**  
1. [Features](#-features)  
2. [Installation](#-installation)  
3. [Configuration](#-configuration)  
4. [Creating Modules](#-creating-modules)  
5. [Running the Tool](#-running-the-tool)  
6. [Example Modules](#-example-modules)  
7. [Troubleshooting](#-troubleshooting)  
8. [Contributing](#-contributing)  

---

## **✨ Features**  
✅ **Customizable TUI Interface** – Navigate with keyboard (↑↓←→)  
✅ **Modular Design** – Easily add new tools as Python modules  
✅ **Secure Encryption** – Built-in file encryption/decryption modules  
✅ **YAML Configuration** – Customize columns and module categories  
✅ **Curses-Based UI** – Works in most terminal environments  

---

## **📥 Installation**  

### **Prerequisites**  
- Python **3.8+**  
- `pip` (Python package manager)  

### **Steps**  
1. **Clone the repository**  
   ```sh
   git clone https://github.com/888kr/Python-Multitool-Framework.git
   cd Python-Multitool-Framework
   ```

2. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the tool**  
   ```sh
   python main.py
   ```

---

## **⚙️ Configuration**  

### **`config.yaml` Setup**  
Edit `config.yaml` to define your tool categories:  
```yaml
columns:
  - name: "Network Tools"
    folder: "network_tools"
    description: "Tools for network operations"
  - name: "File Operations"
    folder: "file_ops"
    description: "File management utilities"
  - name: "System Info"
    folder: "system_info"
    description: "System monitoring tools"
```

### **Folder Structure**  
```
📦 python-multitool
├── 📂 modules/
│   ├── 📂 network_tools/   # First column
│   │   ├── ping_tool.py    # Example module
│   ├── 📂 file_ops/        # Second column
│   │   ├── encrypt_file.py # Encryption module
│   │   ├── decrypt_file.py # Decryption module
│   └── 📂 system_info/     # Third column
│       └── cpu_monitor.py  # Example module
├── 📜 main.py              # Main application
└── 📜 config.yaml          # User configuration
```

---

## **🛠 Creating Modules**  

### **Module Template**  
Each module **must** contain:  
- `MODULE_NAME` (Display name)  
- `MODULE_DESCRIPTION` (Short description)  
- `run()` (Main function)  

Example (`modules/file_ops/example_module.py`):  
```python
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
```

### **Best Practices**  
✔ **Use `curses.endwin()`** before running CLI operations  
✔ **Handle errors gracefully** inside `run()`  
✔ **Keep descriptions short** (1 line recommended)  

---

## **🚀 Running the Tool**  

### **Keyboard Controls**  
| Key | Action |  
|-----|--------|  
| **↑ / ↓** | Navigate modules |  
| **← / →** | Switch columns |  
| **ENTER** | Run selected module |  
| **q** | Quit |  
---

## **📂 Example Modules**  

### **1. File Encryption (`encrypt_file.py`)**  
```python
MODULE_NAME = "Encrypt File"
MODULE_DESCRIPTION = "Securely encrypt files (AES-256-CBC)"

def run():
    # rest of code
```

### **2. Network Ping (`ping_tool.py`)**  
```python
MODULE_NAME = "Ping Tool"
MODULE_DESCRIPTION = "Check host connectivity"

def run():
    # rest of code
```

---

## **🛠 Troubleshooting**  

| Issue | Solution |  
|-------|----------|  
| **Curses errors** | Ensure terminal supports curses (try `TERM=xterm`) |  
| **Module not loading** | Check folder name matches `config.yaml` |  
| **Encryption fails** | Install `pycryptodome` (`pip install pycryptodome`) |  


## **📜 License**  
MIT © 2025 888kr  
