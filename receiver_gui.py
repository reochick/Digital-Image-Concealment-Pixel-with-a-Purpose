import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import os
from steganography_engine import SteganographyEngine

class ReceiverGUI:
    """GUI for extracting data from stego images"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.stego_image_path = None
        self.extracted_data = None
        self.extracted_type = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the receiver interface"""
        # Title
        title_label = tk.Label(
            self.parent_frame,
            text="RECEIVER MODE - Extract Data from Image",
            font=("Arial", 14, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # Image selection
        image_frame = tk.LabelFrame(self.parent_frame, text="Step 1: Select Stego Image", padx=10, pady=10)
        image_frame.pack(fill="x", padx=10, pady=5)
        
        self.image_label = tk.Label(image_frame, text="No image selected", fg="#7f8c8d")
        self.image_label.pack(side="left", fill="x", expand=True)
        
        tk.Button(
            image_frame,
            text="Browse Stego Image",
            command=self.select_stego_image,
            bg="#3498db",
            fg="white",
            padx=10
        ).pack(side="right")
        
        # Extract button
        tk.Button(
            self.parent_frame,
            text="Extract Hidden Data",
            command=self.extract_data,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        ).pack(pady=10)
        
        # Results frame
        results_frame = tk.LabelFrame(self.parent_frame, text="Extracted Data", padx=10, pady=10)
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Text display
        self.text_display = tk.Text(results_frame, height=10, width=50, wrap="word", state="disabled")
        self.text_display.pack(fill="both", expand=True)
        
        # Buttons frame
        button_frame = tk.Frame(self.parent_frame)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(
            button_frame,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard,
            bg="#27ae60",
            fg="white",
            padx=10
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="Save Extracted File",
            command=self.save_extracted_file,
            bg="#e74c3c",
            fg="white",
            padx=10
        ).pack(side="left", padx=5)
        
        # Status label
        self.status_label = tk.Label(self.parent_frame, text="", fg="#7f8c8d")
        self.status_label.pack(pady=5)
    
    def select_stego_image(self):
        """Select stego image"""
        file_path = filedialog.askopenfilename(
            title="Select Stego Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"), ("All files", "*.*")]
        )
        if file_path:
            self.stego_image_path = file_path
            filename = os.path.basename(file_path)
            self.image_label.config(text=f"Selected: {filename}", fg="#2c3e50")
            self.status_label.config(text="", fg="#7f8c8d")
    
    def extract_data(self):
        """Extract data from stego image"""
        if not self.stego_image_path:
            messagebox.showerror("Error", "Please select a stego image")
            return
        
        extracted_data, data_type, success = SteganographyEngine.extract_data(self.stego_image_path)
        
        if not success or extracted_data is None:
            messagebox.showerror("Error", "Failed to extract data from image")
            return
        
        self.extracted_data = extracted_data
        self.extracted_type = data_type
        
        # Display extracted data
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", "end")
        
        if data_type == 'text':
            self.text_display.insert("1.0", extracted_data)
            self.status_label.config(text="Text extracted successfully!", fg="#27ae60")
        else:
            self.text_display.insert("1.0", f"File Type: {data_type}\n\nFile data extracted successfully!\nUse 'Save Extracted File' to save it.")
            self.status_label.config(text=f"File ({data_type}) extracted successfully!", fg="#27ae60")
        
        self.text_display.config(state="disabled")
    
    def copy_to_clipboard(self):
        """Copy extracted text to clipboard"""
        if self.extracted_type == 'text' and self.extracted_data:
            self.parent_frame.clipboard_clear()
            self.parent_frame.clipboard_append(self.extracted_data)
            messagebox.showinfo("Success", "Text copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No text data to copy. Extract data first or use 'Save Extracted File' for file data.")
    
    def save_extracted_file(self):
        """Save extracted file"""
        if not self.extracted_data or self.extracted_type == 'text':
            messagebox.showwarning("Warning", "No file data to save. Use this for extracted files only.")
            return
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=f".{self.extracted_type}",
            filetypes=[(f"{self.extracted_type.upper()} files", f"*.{self.extracted_type}"), ("All files", "*.*")]
        )
        
        if save_path:
            try:
                SteganographyEngine._binary_to_file(self.extracted_data, save_path)
                messagebox.showinfo("Success", f"File saved successfully!\n\nPath: {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
