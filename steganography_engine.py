import numpy as np
import cv2
import struct
import base64
from typing import Tuple, Optional

class SteganographyEngine:
    """Core steganography engine using LSB (Least Significant Bit) technique"""
    
    @staticmethod
    def _text_to_binary(text: str) -> str:
        """Convert text to binary string"""
        return ''.join(format(ord(char), '08b') for char in text)
    
    @staticmethod
    def _binary_to_text(binary: str) -> str:
        """Convert binary string to text"""
        text = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        return text
    
    @staticmethod
    def _file_to_binary(file_path: str) -> str:
        """Convert file to binary string"""
        with open(file_path, 'rb') as f:
            file_data = f.read()
        return ''.join(format(byte, '08b') for byte in file_data)
    
    @staticmethod
    def _binary_to_file(binary: str, output_path: str) -> None:
        """Convert binary string to file"""
        byte_data = bytearray()
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                byte_data.append(int(byte, 2))
        with open(output_path, 'wb') as f:
            f.write(byte_data)
    
    @staticmethod
    def embed_data(image_path: str, data: str, data_type: str) -> Tuple[np.ndarray, bool]:
        """
        Embed text or file data into image using LSB steganography
        
        Args:
            image_path: Path to the cover image
            data: Data to embed (text content or file path)
            data_type: Type of data ('text' or 'file')
        
        Returns:
            Tuple of (stego_image, success)
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return None, False
            
            # Convert to RGB if needed
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            
            # Flatten image to 1D array
            flat_image = image.flatten()
            
            # Prepare data
            if data_type == 'text':
                binary_data = SteganographyEngine._text_to_binary(data)
                file_extension = 'txt'
                file_size = len(data.encode('utf-8'))
            elif data_type == 'file':
                binary_data = SteganographyEngine._file_to_binary(data)
                file_extension = data.split('.')[-1].lower()
                with open(data, 'rb') as f:
                    file_size = len(f.read())
            else:
                return None, False
            
            # Create header: [data_type_flag(1 bit), file_extension(8 bits), file_size(32 bits)]
            # data_type_flag: 0 for text, 1 for file
            data_type_flag = '0' if data_type == 'text' else '1'
            
            # Encode file extension (max 255 chars)
            ext_binary = format(len(file_extension), '08b') + SteganographyEngine._text_to_binary(file_extension)
            
            # Encode file size (32 bits for up to 4GB)
            size_binary = format(file_size, '032b')
            
            # Combine header and data
            header = data_type_flag + ext_binary + size_binary
            full_binary = header + binary_data
            
            # Check capacity
            if len(full_binary) > len(flat_image):
                return None, False
            
            # Embed data using LSB
            for i, bit in enumerate(full_binary):
                flat_image[i] = (flat_image[i] & 0xFE) | int(bit)
            
            # Reshape back to original image shape
            stego_image = flat_image.reshape(image.shape)
            
            return stego_image.astype(np.uint8), True
        
        except Exception as e:
            print(f"Error embedding data: {e}")
            return None, False
    
    @staticmethod
    def extract_data(image_path: str) -> Tuple[Optional[str], str, bool]:
        """
        Extract hidden data from stego image
        
        Args:
            image_path: Path to the stego image
        
        Returns:
            Tuple of (extracted_data, data_type, success)
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return None, '', False
            
            # Convert to RGB if needed
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            
            # Flatten image
            flat_image = image.flatten()
            
            # Extract header
            # First bit: data type flag
            data_type_flag = str(flat_image[0] & 1)
            
            # Next 8 bits: extension length
            ext_len_binary = ''.join(str(flat_image[i] & 1) for i in range(1, 9))
            ext_len = int(ext_len_binary, 2)
            
            # Next (ext_len * 8) bits: extension
            ext_start = 9
            ext_end = ext_start + (ext_len * 8)
            ext_binary = ''.join(str(flat_image[i] & 1) for i in range(ext_start, ext_end))
            file_extension = SteganographyEngine._binary_to_text(ext_binary)
            
            # Next 32 bits: file size
            size_start = ext_end
            size_end = size_start + 32
            size_binary = ''.join(str(flat_image[i] & 1) for i in range(size_start, size_end))
            file_size = int(size_binary, 2)
            
            # Extract data
            data_start = size_end
            data_end = data_start + (file_size * 8)
            data_binary = ''.join(str(flat_image[i] & 1) for i in range(data_start, data_end))
            
            # Determine data type and extract
            if data_type_flag == '0':
                # Text data
                extracted_data = SteganographyEngine._binary_to_text(data_binary)
                return extracted_data, 'text', True
            else:
                # File data
                return data_binary, file_extension, True
        
        except Exception as e:
            print(f"Error extracting data: {e}")
            return None, '', False
