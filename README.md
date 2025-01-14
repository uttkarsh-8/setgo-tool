# Image Steganography Tool

This tool allows users to hide secret messages within images using steganography techniques combined with encryption. It provides both a Flask backend API for handling the steganographic operations and a simple React frontend for user interaction.

## How It Works

The tool uses the Least Significant Bit (LSB) steganography technique combined with Fernet symmetric encryption. Here's how the process works:

1. **Message Hiding Process:**
   - The user's message is first encrypted using a password-derived key
   - The encrypted message is converted to binary form
   - Each bit of the binary message is stored in the least significant bit of image pixels
   - The modified image looks virtually identical to the original but contains the hidden message

2. **Message Extraction Process:**
   - The least significant bits are extracted from the image pixels
   - The binary data is reconstructed into the encrypted message
   - Using the provided password, the message is decrypted
   - The original message is recovered and displayed to the user

## Features

- Secure message hiding using LSB steganography
- Password-based encryption using Fernet
- Support for PNG image formats
- Simple web interface for easy interaction
- Separate hide and extract functionalities
- Error handling for invalid inputs or passwords

## Technical Requirements

- Python 3.x
- Node.js and npm
- Web browser with JavaScript enabled

## Installation

1. Clone the repository:

git clone https://github.com/your-username/steganography-tool.git
cd steganography-tool

2. Set up the Python backend:

cd steganography_api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Set up the React frontend:

cd steganography_api
python app.py

cd stego-frontend
npm start


## Usage

To Hide a Message:

Upload a PNG image
Enter your secret message
Provide a password
Click "Hide Message"
Download the resulting image


## To Extract a Message:

Upload an image containing a hidden message
Enter the correct password
Click "Extract Message"
View the extracted message




## Sample

 ### 1. Hiding text
  Selecting an image, adding a message and encrypting it using a password

![image](https://github.com/user-attachments/assets/b88e64e7-1c61-433a-a594-5d404d99cfeb)

 ### 2. Extracting text

 Choose the newly created image and provide the password

 ![image](https://github.com/user-attachments/assets/ee47dec3-ed38-4b57-b2e0-6141b43e1ed0)




Input Requirements

Images: PNG format only
Message: Any text message that fits within the image capacity
Password: Any string (used for encryption)
