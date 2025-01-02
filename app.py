from tkinter import Tk
from gui_elements import setup_gui

# Initialize the GUI
root = Tk()
root.title("OCR Scanner")
root.geometry("1200x600")  # Adjust the window size

# Setup GUI layout and functionality
setup_gui(root)

# Run the application
root.mainloop()
