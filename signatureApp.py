import tkinter as tk
from tkinter import filedialog


import trueRNG
import digitalSingaturev04



# Interfejs graficzny aplikacji

def generateKeys():
    digitalSingaturev04.generate_rsa_keys_from_file('TrueRNG.bin')
    output_text.insert(tk.END, f"Keys generated\n")

def process_file(file_path):
    # Process the file based on the given file path
    output_text.insert(tk.END, f"Processing file: {file_path}\n")

def process_sign_input():
    input_text = text_input.get("1.0", tk.END).strip()

    #Process the input text
    private_key_path = 'private_key.pem'
    pdf_file_path = file_entry.get()
    signature_file_path = input_text + '.bin'
    
    digitalSingaturev04.sign_pdf_with_rsa_sha3(private_key_path, pdf_file_path, signature_file_path)

    output_text.insert(tk.END, f"File succesfuly processed with signature: {signature_file_path}\n")

def process_files():
    file_path1 = file_entry1.get()
    file_path2 = file_entry2.get()
    file_path3 = file_entry3.get()

    public_key_path = file_entry3.get()
    pdf_file_path = file_entry1.get()
    signature_file_path = file_entry2.get()


    verificationOutput = digitalSingaturev04.verify_signature_with_rsa_sha3(public_key_path, pdf_file_path,signature_file_path)

    # Process the two file paths
    output_text.insert(tk.END, f"Processing files: {verificationOutput}\n")

root = tk.Tk()
root.title("Digital signature v0.3")

# Left column
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10)

text_button = tk.Button(left_frame, text="Generate your own TRNG and RSA keys", command=generateKeys)
text_button.pack(pady=10)

left_title_label = tk.Label(left_frame, text="Sign your file")
left_title_label.pack()

file_label = tk.Label(left_frame, text="File:")
file_label.pack(pady=10)

file_entry = tk.Entry(left_frame)
file_entry.pack()

def open_file_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(tk.END, file_path)

file_button = tk.Button(left_frame, text="Open File", command=open_file_dialog)
file_button.pack()

text_label = tk.Label(left_frame, text="Enter name of signature file:")
text_label.pack(pady=10)

text_input = tk.Text(left_frame, height=1, width=10)
text_input.pack()

text_button = tk.Button(left_frame, text="Sign your file", command=process_sign_input)
text_button.pack(pady=10)

# Right column
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=10)

file1_label = tk.Label(right_frame, text="Choose file to verify:")
file1_label.pack(pady=10)

file_entry1 = tk.Entry(right_frame)
file_entry1.pack()

def open_file_dialog1():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry1.delete(0, tk.END)
        file_entry1.insert(tk.END, file_path)

file_button1 = tk.Button(right_frame, text="Open file to verify", command=open_file_dialog1)
file_button1.pack()

file2_label = tk.Label(right_frame, text="Choose signature file")
file2_label.pack(pady=10)

file_entry2 = tk.Entry(right_frame)
file_entry2.pack()

def open_file_dialog2():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry2.delete(0, tk.END)
        file_entry2.insert(tk.END, file_path)

file_button2 = tk.Button(right_frame, text="Open signature file", command=open_file_dialog2)
file_button2.pack()

file3_label = tk.Label(right_frame, text="Choose public key file")
file3_label.pack(pady=10)

file_entry3 = tk.Entry(right_frame)
file_entry3.pack()

def open_file_dialog3():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry3.delete(0, tk.END)
        file_entry3.insert(tk.END, file_path)

file_button3 = tk.Button(right_frame, text="Choose public key file", command=open_file_dialog3)
file_button3.pack()

process_button = tk.Button(right_frame, text="Check if file singanure is valid", command=process_files)
process_button.pack(pady=10)

output_frame = tk.Frame(root)
output_frame.pack(pady=10)

output_text = tk.Text(output_frame, height=10, width=50)
output_text.pack()

root.mainloop()