import tkinter as tk
from tkinter import messagebox

def modify_fetch_code():
    try:
        # Get the input fetch code from the text box
        fetch_code = fetch_code_input.get("1.0", tk.END).strip()
        
        if not fetch_code:
            messagebox.showwarning("Warning", "Please enter fetch code before modifying.")
            return

        # Replace ONLY the old productId with the new one
        modified_code = fetch_code.replace('9N5QMZNW4BT1', '9PLKMR36KR4Z')

        # Replace the word "include" with "omit"
        modified_code = modified_code.replace('include', 'omit')

        # Display the modified code in the output text box
        fetch_code_output.delete("1.0", tk.END)
        fetch_code_output.insert(tk.END, modified_code)
        
        messagebox.showinfo("Success", "Fetch code modified successfully!")
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def copy_to_clipboard():
    try:
        output_text = fetch_code_output.get("1.0", tk.END).strip()
        if not output_text:
            messagebox.showwarning("Warning", "No modified code to copy.")
            return
            
        root.clipboard_clear()
        root.clipboard_append(output_text)
        messagebox.showinfo("Success", "Modified code copied to clipboard!")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")

def clear_input_box():
    try:
        fetch_code_input.delete("1.0", tk.END)
        fetch_code_output.delete("1.0", tk.END)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to clear input: {str(e)}")

def clear_output_box():
    try:
        fetch_code_output.delete("1.0", tk.END)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to clear output: {str(e)}")

# Create the main application window
root = tk.Tk()
root.title("Fetch Code Modifier")
root.geometry("900x700")
root.resizable(True, True)

# Configure grid weights for responsive design
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)

# Input Label
input_label = tk.Label(root, text="Original Fetch Code:", font=("Arial", 12, "bold"))
input_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

# Input Text Box
fetch_code_input = tk.Text(root, height=10, width=100, wrap=tk.WORD)
fetch_code_input.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

# Buttons Frame
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, pady=10)

# Modify Button
modify_button = tk.Button(button_frame, text="Modify Fetch Code", command=modify_fetch_code, 
                         bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=20)
modify_button.grid(row=0, column=0, padx=5)

# Clear Input Button
clear_input_button = tk.Button(button_frame, text="Clear Input", command=clear_input_box,
                              bg="#f44336", fg="white", font=("Arial", 10, "bold"), padx=20)
clear_input_button.grid(row=0, column=1, padx=5)

# Output Label
output_label = tk.Label(root, text="Modified Fetch Code:", font=("Arial", 12, "bold"))
output_label.grid(row=3, column=0, sticky="w", padx=10, pady=(20, 5))

# Output Text Box
fetch_code_output = tk.Text(root, height=10, width=100, wrap=tk.WORD, bg="#f0f0f0")
fetch_code_output.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)

# Output Buttons Frame
output_button_frame = tk.Frame(root)
output_button_frame.grid(row=5, column=0, pady=10)

# Copy Button
copy_button = tk.Button(output_button_frame, text="Copy to Clipboard", command=copy_to_clipboard,
                       bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=20)
copy_button.grid(row=0, column=0, padx=5)

# Clear Output Button
clear_output_button = tk.Button(output_button_frame, text="Clear Output", command=clear_output_box,
                               bg="#FF9800", fg="white", font=("Arial", 10, "bold"), padx=20)
clear_output_button.grid(row=0, column=1, padx=5)

# Instructions Label
instructions = tk.Label(root, text="Instructions: 1. Paste your fetch code above 2. Click 'Modify Fetch Code' 3. Copy the result",
                       font=("Arial", 9), fg="gray")
instructions.grid(row=6, column=0, pady=(10, 10))

# Start the GUI
if __name__ == "__main__":
    root.mainloop()