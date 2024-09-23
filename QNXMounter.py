import tkinter as tk
from tkinter import messagebox, font
import subprocess


def run_batch_script():
    bin_image_path = bin_image_entry.get()
    mount_base_dir = mount_base_entry.get()
    sudo_password = sudo_password_entry.get()

    if not (bin_image_path and mount_base_dir and sudo_password):
        messagebox.showerror("Input Error", "All fields are required!")
        return

    batch_file_path = 'path_to_your_batch_file.bat'  # Update with your batch file path
    command = f'start cmd /c "{batch_file_path} {bin_image_path} {mount_base_dir} {sudo_password}"'
    
    try:
        subprocess.run(command, shell=True, check=True)
        messagebox.showinfo("Success", "Batch script executed successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Execution Error", f"Error running batch script: {e}")

# Function to change button appearance on hover
def on_enter(e):
    run_button['background'] = '#45a049'

def on_leave(e):
    run_button['background'] = '#4CAF50'

# Set up the GUI
app = tk.Tk()
app.title("QNX6 Mounting Tool")
app.geometry("400x300")
app.configure(bg="#f0f0f0")

# Custom font
custom_font = font.Font(family="Arial", size=10)

# Title Label
title_label = tk.Label(app, text="QNX6 Mounting Tool", font=("Arial", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

# Input for Bin Image Path
tk.Label(app, text="Path to .bin Image:", font=custom_font, bg="#f0f0f0").pack(pady=5)
bin_image_entry = tk.Entry(app, width=50, font=custom_font)
bin_image_entry.pack(pady=5)

# Input for Mount Base Directory
tk.Label(app, text="Mount Base Directory:", font=custom_font, bg="#f0f0f0").pack(pady=5)
mount_base_entry = tk.Entry(app, width=50, font=custom_font)
mount_base_entry.pack(pady=5)

# Input for Sudo Password
tk.Label(app, text="Sudo Password:", font=custom_font, bg="#f0f0f0").pack(pady=5)
sudo_password_entry = tk.Entry(app, width=50, font=custom_font, show='*')
sudo_password_entry.pack(pady=5)

# Run Button
run_button = tk.Button(app, text="Run Script", command=run_batch_script, bg="#4CAF50", fg="black", font=("Arial", 12, "bold"), borderwidth=0)
run_button.pack(pady=20)

# Bind hover events
run_button.bind("<Enter>", on_enter)
run_button.bind("<Leave>", on_leave)

app.mainloop()
