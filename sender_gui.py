import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import os
from steganography_engine import SteganographyEngine

class SenderGUI:
    """GUI for embedding data into images"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.image_path = None
        self.data_path = None
        self.data_type = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the sender interface"""
        # Title
        title_label = tk.Label(
            self.parent_frame,
            text="SENDER MODE - Embed Data into Image",
            font=("Arial", 14, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # Image selection
        image_frame = tk.LabelFrame(self.parent_frame, text="Step 1: Select Cover Image", padx=10, pady=10)
        image_frame.pack(fill="x", padx=10, pady=5)
        
        self.image_label = tk.Label(image_frame, text="No image selected", fg="#7f8c8d")
        self.image_label.pack(side="left", fill="x", expand=True)
        
        tk.Button(
            image_frame,
            text="Browse Image",
            command=self.select_image,
            bg="#3498db",
            fg="white",
            padx=10
        ).pack(side="right")
        
        # Data selection
        data_frame = tk.LabelFrame(self.parent_frame, text="Step 2: Select Data to Embed", padx=10, pady=10)
        data_frame.pack(fill="x", padx=10, pady=5)
        
        button_frame = tk.Frame(data_frame)
        button_frame.pack(fill="x")
        
        tk.Button(
            button_frame,
            text="Embed Text",
            command=self.select_text,
            bg="#27ae60",
            fg="white",
            padx=10
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="Embed PDF/File",
            command=self.select_file,
            bg="#e74c3c",
            fg="white",
            padx=10
        ).pack(side="left", padx=5)
        
        self.data_label = tk.Label(data_frame, text="No data selected", fg="#7f8c8d")
        self.data_label.pack(fill="x", pady=5)
        
        # Text input area (for text embedding)
        self.text_frame = tk.LabelFrame(self.parent_frame, text="Text to Embed", padx=10, pady=10)
        self.text_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.text_input = tk.Text(self.text_frame, height=8, width=50, wrap="word")
        self.text_input.pack(fill="both", expand=True)
        
        # Embed button
        tk.Button(
            self.parent_frame,
            text="Embed Data into Image",
            command=self.embed_data,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        ).pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(self.parent_frame, text="", fg="#7f8c8d")
        self.status_label.pack(pady=5)
    
    def select_image(self):
        """Select cover image"""
        file_path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"), ("All files", "*.*")]
        )
        if file_path:
            self.image_path = file_path
            filename = os.path.basename(file_path)
            self.image_label.config(text=f"Selected: {filename}", fg="#2c3e50")
            self.status_label.config(text="", fg="#7f8c8d")
    
    def select_text(self):
        """Select text to embed"""
        self.data_type = 'text'
        self.data_path = None
        self.data_label.config(text="Text mode selected - Enter text below", fg="#27ae60")
        self.text_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    def select_file(self):
        """Select file to embed"""
        file_path = filedialog.askopenfilename(
            title="Select File to Embed",
            filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx *.doc"), ("All files", "*.*")]
        )
        if file_path:
            self.data_type = 'file'
            self.data_path = file_path
            filename = os.path.basename(file_path)
            self.data_label.config(text=f"Selected: {filename}", fg="#e74c3c")
            self.text_frame.pack_forget()
    
    def embed_data(self):
        """Embed data into image"""
        if not self.image_path:
            messagebox.showerror("Error", "Please select a cover image")
            return
        
        if self.data_type == 'text':
            text_data = self.text_input.get("1.0", "end-1c")
            if not text_data.strip():
                messagebox.showerror("Error", "Please enter text to embed")
                return
            data_to_embed = text_data
        elif self.data_type == 'file':
            if not self.data_path:
                messagebox.showerror("Error", "Please select a file to embed")
                return
            data_to_embed = self.data_path
        else:
            messagebox.showerror("Error", "Please select data type (text or file)")
            return
        
        # Embed data
        stego_image, success = SteganographyEngine.embed_data(
            self.image_path,
            data_to_embed,
            self.data_type
        )
        
        if not success or stego_image is None:
            messagebox.showerror("Error", "Failed to embed data. Image might be too small.")
            return
        
        # Save stego image
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if save_path:
            cv2.imwrite(save_path, stego_image)
            messagebox.showinfo("Success", f"Stego image saved successfully!\n\nPath: {save_path}")
            self.status_label.config(text="Data embedded successfully!", fg="#27ae60")
