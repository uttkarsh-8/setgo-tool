from PIL import Image
import numpy as np
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SimpleImageSteganography:
    def __init__(self):
        self.END_MARKER = "###END###"
    
    def generate_key(self, password):
        salt = b'simple_salt'  
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key)
    
    def encrypt_message(self, message, password):
        f = self.generate_key(password)
        return f.encrypt(message.encode())
    
    def decrypt_message(self, encrypted_message, password):
        f = self.generate_key(password)
        return f.decrypt(encrypted_message).decode()
    
    def text_to_binary(self, text):
        if isinstance(text, str):
            text = text.encode()
        return ''.join(format(byte, '08b') for byte in text)
    
    def binary_to_bytes(self, binary):
        return bytes(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))
    
    def hide_message(self, image_path, message, password, output_path):
        try:
            marked_message = message + self.END_MARKER
            encrypted_message = self.encrypt_message(marked_message, password)
            binary_message = self.text_to_binary(encrypted_message)
            
            img = Image.open(image_path)
            img_array = np.array(img)
            
            if len(binary_message) > img_array.size:
                raise ValueError("Message is too long for this image")
            
            flat_img = img_array.flatten()
            for i in range(len(binary_message)):
                flat_img[i] = (flat_img[i] & 0xFE) | int(binary_message[i])
            
            modified_img = flat_img.reshape(img_array.shape)
            Image.fromarray(modified_img).save(output_path, 'PNG')
            return True
            
        except Exception as e:
            raise ValueError(f"Failed to hide message: {str(e)}")
    
    def extract_message(self, image_path, password):
        try:
            img = Image.open(image_path)
            img_array = np.array(img)
            
            flat_img = img_array.flatten()
            binary_message = ''
            message_bytes = b''
            
            for i in range(0, len(flat_img), 8):
                bits = ''.join(str(pixel & 1) for pixel in flat_img[i:i+8])
                if len(bits) == 8:
                    try:
                        binary_message += bits
                        if len(binary_message) % 8 == 0:
                            message_bytes = self.binary_to_bytes(binary_message)
                            try:
                                decrypted = self.decrypt_message(message_bytes, password)
                                if self.END_MARKER in decrypted:
                                    return decrypted[:-len(self.END_MARKER)]
                            except:
                                continue
                    except:
                        continue
            
            raise ValueError("No valid message found")
            
        except Exception as e:
            raise ValueError(f"Failed to extract message: {str(e)}")