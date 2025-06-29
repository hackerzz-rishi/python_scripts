import PyPDF2
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os

def unlock_pdf(input_path, output_path, password):
    """
    Unlocks a password-protected PDF file and saves the unlocked version.

    Args:
        input_path (str): Path to the encrypted PDF file.
        output_path (str): Path to save the unlocked PDF file.
        password (str): Password to unlock the PDF.

    Returns:
        bool: True if unlocking was successful, False otherwise.
    """
    try:
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            # Check if the PDF is encrypted
            if reader.is_encrypted:
                # Try to decrypt with the provided password
                if reader.decrypt(password):
                    writer = PyPDF2.PdfWriter()
                    # Add all pages to the writer
                    for page in reader.pages:
                        writer.add_page(page)
                    # Write the unlocked PDF to output_path
                    with open(output_path, 'wb') as out_file:
                        writer.write(out_file)
                    print(f"Unlocked PDF saved to: {output_path}")
                    return True
                else:
                    print(f"Incorrect password for {input_path}")
                    return False
            else:
                print(f"{input_path} is not encrypted. Skipping.")
                return False
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def main():
    """
    Main function to run the PDF unlocker GUI.
    Allows user to select PDF files and enter a password to unlock them.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    # Prompt user to select one or more PDF files
    file_paths = filedialog.askopenfilenames(
        title="Select PDF files",
        filetypes=[("PDF Files", "*.pdf")],
        multiple=True  # Explicitly allow multiple selection
    )
    if not file_paths:
        print("No files selected.")
        return

    # Prompt user to enter the password
    password = simpledialog.askstring("Password", "Enter PDF password:", show='*')
    if password is None:
        print("No password entered.")
        return

    unlocked_count = 0
    # Process each selected PDF file
    for input_pdf in file_paths:
        # Create output filename by appending '_unlocked' before the extension
        output_pdf = os.path.splitext(input_pdf)[0] + "_unlocked.pdf"
        if unlock_pdf(input_pdf, output_pdf, password):
            unlocked_count += 1

    # Show a message box with the result
    messagebox.showinfo("Done", f"Unlocked {unlocked_count} PDF(s).")

if __name__ == "__main__":
    main()
