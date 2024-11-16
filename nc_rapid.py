import tkinter as tk
from tkinter import filedialog
import re
import json
import os

# Default threshold value
DEFAULT_THRESHOLD = 19

# Function to process the content of the file
def process_file(content, threshold=DEFAULT_THRESHOLD):
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

# Function to load the threshold from a settings file, or return the default value
def load_threshold():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as file:
            data = json.load(file)
            return data.get("threshold", DEFAULT_THRESHOLD)
    return DEFAULT_THRESHOLD

# Function to save the threshold to a settings file
def save_threshold(threshold):
    data = {"threshold": threshold}
    with open("settings.json", "w") as file:
        json.dump(data, file)

# Function to open and select a file using tkinter file dialog
def open_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select a file to process", filetypes=(("Text Files", "*.tap"), ("All Files", "*.*")))

    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()

        # Process the content with the current threshold
        threshold_value = float(threshold_entry.get()) if threshold_entry.get() else DEFAULT_THRESHOLD
        processed_content = process_file(content, threshold_value)
        
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

# GUI setup
def setup_gui():
    global threshold_entry, threshold_label

    root = tk.Tk()
    root.title("Set Z safe height")

    # Load the saved threshold value (or use default)
    current_threshold = load_threshold()

    # Create and place the threshold label
    threshold_label = tk.Label(root, text=f"Previous safe height: {current_threshold} mm (set new in case you need)")
    threshold_label.pack(pady=20)

    # Create and place the threshold entry box (numerical input)
    threshold_entry = tk.Entry(root)
    threshold_entry.insert(0, str(current_threshold))  # Set the current threshold value in the input box
    threshold_entry.pack(pady=20)

    # Create and place the "Open File" button
    open_button = tk.Button(root, text="Open File", command=open_file)
    open_button.pack(pady=10)

    # Create and place the "Save Threshold" button
    save_button = tk.Button(root, text="Save Threshold", command=save_threshold_button)
    save_button.pack(pady=10)

    # Run the GUI
    root.mainloop()

# Function to save the threshold when the button is pressed
def save_threshold_button():
    try:
        # Get the threshold value from the entry field and convert it to a float
        new_threshold = float(threshold_entry.get())
        save_threshold(new_threshold)  # Save the threshold value
        threshold_label.config(text=f"Threshold: {new_threshold}")  # Update the label
        print(f"Threshold value {new_threshold} saved.")
    except ValueError:
        print("Invalid threshold value entered. Please enter a valid number.")

if __name__ == "__main__":
    setup_gui()
