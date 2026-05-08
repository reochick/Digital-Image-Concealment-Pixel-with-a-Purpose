import tkinter as tk
from tkinter import ttk
from sender_gui import SenderGUI
from receiver_gui import ReceiverGUI

class SteganographyApp:
    """Main application window"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography - Embed & Extract Data")
        self.root.geometry("700x800")
        self.root.resizable(True, True)
        
        # Configure style
        self.root.configure(bg="#ecf0f1")
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="#2c3e50")
        header_frame.pack(fill="x", pady=(0, 10))
        
        header_label = tk.Label(
            header_frame,
            text="🔐 Image Steganography Tool",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10
        )
        header_label.pack()
        
        # Mode selection
        mode_frame = tk.Frame(main_frame, bg="#ecf0f1")
        mode_frame.pack(fill="x", pady=10)
        
        tk.Label(
            mode_frame,
            text="Select Mode:",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1"
        ).pack(side="left", padx=5)
        
        self.mode_var = tk.StringVar(value="sender")
        
        tk.Radiobutton(
            mode_frame,
            text="Sender (Embed Data)",
            variable=self.mode_var,
            value="sender",
            command=self.switch_mode,
            bg="#ecf0f1",
            font=("Arial", 10)
        ).pack(side="left", padx=5)
        
        tk.Radiobutton(
            mode_frame,
            text="Receiver (Extract Data)",
            variable=self.mode_var,
            value="receiver",
            command=self.switch_mode,
            bg="#ecf0f1",
            font=("Arial", 10)
        ).pack(side="left", padx=5)
        
        # Content frame (will hold sender or receiver GUI)
        self.content_frame = tk.Frame(main_frame, bg="white")
        self.content_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initialize with sender mode
        self.sender_gui = None
        self.receiver_gui = None
        self.switch_mode()
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg="#34495e")
        footer_frame.pack(fill="x", pady=(10, 0))
        
        footer_label = tk.Label(
            footer_frame,
            text="Secure data embedding using LSB steganography | Supports Text & PDF files",
            font=("Arial", 9),
            bg="#34495e",
            fg="white",
            pady=5
        )
        footer_label.pack()
    
    def switch_mode(self):
        """Switch between sender and receiver modes"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        mode = self.mode_var.get()
        
        if mode == "sender":
            self.sender_gui = SenderGUI(self.content_frame)
        else:
            self.receiver_gui = ReceiverGUI(self.content_frame)

def main():
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
