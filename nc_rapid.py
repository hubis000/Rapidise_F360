import tkinter as tk
from tkinter import filedialog
import re

# Function to process the content of the file
def process_file(content, threshold=19):
    lines = content.splitlines()
    processed_lines = []
    add_g0 = False  # Flag to add G0 when Z crosses the threshold
    add_g1 = False  # Flag to add G1 when Z drops below the threshold

    for i, line in enumerate(lines):
        # If the line starts with 'G', skip modification
        if line.startswith('G'):
            processed_lines.append(line.strip())
            continue
        
        # Check if the line contains 'Z' and extract Z value
        z_match = re.search(r'Z([-+]?[0-9]*\.?[0-9]+)', line)
        if z_match:
            z_value = float(z_match.group(1))

            if z_value >= threshold:
                # When Z crosses above the threshold, insert G0 before the next line
                if not add_g0:
                    # Add G0 before the next line (if it's not already added)
                    add_g0 = True

                # Add the current line
                processed_lines.append(line.strip())

                continue  # Skip processing further and move to the next line
        
        # If we're past the threshold, and we haven't yet added G0, do it now
        if add_g0:
            processed_lines.append(f"G0 {line.strip()}")
            add_g0 = False  # Reset the G0 flag to avoid adding it again

        else:
            # If the line doesn't need any G0 or G1 adjustments, add it as is
            processed_lines.append(line.strip())
            
    return "\n".join(processed_lines)

# Function to open and select a file using tkinter file dialog
def open_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select a file to process", filetypes=(("Text Files", "*.tap"), ("All Files", "*.*")))
    
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()

        # Process the content
        processed_content = process_file(content)
        
        # Save the processed content to a new file
        save_file(processed_content)

# Function to save the processed content to a new file
def save_file(content):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    save_path = filedialog.asksaveasfilename(title="Save processed file", defaultextension=".tap", filetypes=(("Text Files", "*.tap"), ("All Files", "*.*")))
    
    if save_path:
        with open(save_path, 'w') as file:
            file.write(content)
        print(f"Processed file saved to: {save_path}")

if __name__ == "__main__":
    open_file()
