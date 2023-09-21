#wersja trzecia podpisu cyfrowego
import hashlib
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import imageio
from PIL import Image
from PIL import ImageGrab
import time
from Crypto import Random
from Crypto.PublicKey import RSA

import os
import tkinter as tk
from tkinter import filedialog


import trueRNG


def generate_rsa_keys_from_file(bin_file_path):
    
    trueRNG.generate_new_TRNG(bin_file_path)

    with open(bin_file_path, 'rb') as file:
        # Generate the private key
        private_key = RSA.generate(2048, file.read)

        private_pem = private_key.export_key()
        public_pem = private_key.publickey().export_key()

        with open('private_key.pem', 'wb') as private_file:
            private_file.write(private_pem)

        with open('public_key.pem', 'wb') as public_file:
            public_file.write(public_pem)

        print("RSA keys generated and saved successfully.")

        return private_key



# Funkcja realizująca podpisanie wybranego pliku

def sign_pdf_with_rsa_sha3(private_key_file_path, pdf_file_path, signature_file_path):
    # Load the private key from file
    with open(private_key_file_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    with open(pdf_file_path, 'rb') as pdf_file:
        # Read the PDF file
        pdf_data = pdf_file.read()

        # Calculate the SHA-3 (256-bit) hash of the PDF data
        sha3_hash = hashlib.sha3_256(pdf_data).digest()

        # Sign the hash using RSA private key
        signature = private_key.sign(
            sha3_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA3_256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA3_256()
        )

        # Save the signature to a file
        with open(signature_file_path, 'wb') as signature_file:
            signature_file.write(signature)

        print(f"PDF file signed successfully. Signature saved to: {signature_file_path}")



#Funkcja weryfikująca poprawnosć podpisu cyfrowego

def verify_signature_with_rsa_sha3(public_key_file_path, pdf_file_path, signature_file_path):
    try:
        with open(public_key_file_path, 'rb') as public_key_file, \
                open(pdf_file_path, 'rb') as pdf_file, \
                open(signature_file_path, 'rb') as signature_file:
            # Load the public key from file
            public_key = serialization.load_pem_public_key(
                public_key_file.read(),
                backend=default_backend()
            )

            # Read the PDF file and signature
            pdf_data = pdf_file.read()
            signature = signature_file.read()

            # Calculate the SHA-3 (256-bit) hash of the PDF data
            sha3_hash = hashlib.sha3_256(pdf_data).digest()

            # Verify the signature using RSA public key
            try:
                public_key.verify(
                    signature,
                    sha3_hash,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA3_256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA3_256()
                )

                print("Signature is valid. PDF file has not been tampered with.")

                return "Signature is valid. PDF file has not been tampered with."

            except Exception:
                print("Invalid signature. The PDF file may have been modified.")

                return "Invalid signature. The PDF file may have been modified."

    except IOError:
        print(f"Error reading file: {public_key_file_path}, {pdf_file_path}, or {signature_file_path}")



