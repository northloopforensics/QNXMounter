import customtkinter as ctk
from tkinter import messagebox, filedialog
import subprocess
import os


def work_site():      # Cause script to execute in directory containing script and batch file
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    global pwd
    pwd = os.path.dirname(os.path.abspath(__file__))


def run_batch_script(action): # Run batch script 
    bin_image_path = bin_image_entry.get()
    mount_base_dir = mount_base_entry.get()
    sudo_password = sudo_password_entry.get()

    if not (bin_image_path and mount_base_dir and sudo_password):
        messagebox.showerror("Input Error", "All fields are required!")
        return

    batch_file_path = './mountqnx6.bat'  
    command = f'start cmd /c "{batch_file_path} {action} \"{bin_image_path}\" \"{mount_base_dir}\" \"{sudo_password}\""'
    
    try:
        subprocess.run(command, shell=True, check=True)
        messagebox.showinfo("Success", f"{action.capitalize()} action completed successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Execution Error", f"Error running batch script: {e}")


def select_bin_file():  # File selection dialog for .bin image file
    file_path = filedialog.askopenfilename(title="Select .bin Image", filetypes=[("BIN Files", ("*.bin", ".BIN", "*.img", ".IMG", ".dd", ".DD"))])
    if file_path:
        bin_image_entry.delete(0, ctk.END)
        bin_image_entry.insert(0, file_path)

def select_mount_dir(): # Directory selection dialog for mount base directory

    dir_path = filedialog.askdirectory(title="Select Mount Base Directory")
    if dir_path:
        mount_base_entry.delete(0, ctk.END)
        mount_base_entry.insert(0, dir_path)

# GUI Stuff
ctk.set_appearance_mode("System")  # use system setting for light or dark mode
ctk.set_default_color_theme("blue")  

app = ctk.CTk()
app.title("QNX6 Mounting Tool")
app.geometry("600x250")

# Title Label
title_label = ctk.CTkLabel(app, text="QNX6 Mounting Tool", font=ctk.CTkFont(size=16, weight="bold"))
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# Input for Image 
bin_image_label = ctk.CTkLabel(app, text="Path to Image File:")
bin_image_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

bin_image_entry = ctk.CTkEntry(app, width=250)
bin_image_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

bin_image_button = ctk.CTkButton(app, text="Browse", command=select_bin_file)
bin_image_button.grid(row=1, column=2, padx=5, pady=5)

# Input for Mount Point Directory
mount_base_label = ctk.CTkLabel(app, text="Mount Point Directory:")
mount_base_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

mount_base_entry = ctk.CTkEntry(app, width=250)
mount_base_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

mount_base_button = ctk.CTkButton(app, text="Browse", command=select_mount_dir)
mount_base_button.grid(row=2, column=2, padx=5, pady=5)

# Input for Sudo Password
sudo_password_label = ctk.CTkLabel(app, text="Sudo Password:")
sudo_password_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")

sudo_password_entry = ctk.CTkEntry(app, width=250, show='*')
sudo_password_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Run Button (Mount)
run_button = ctk.CTkButton(app, text="Mount Image", command=lambda: run_batch_script('mount'), fg_color="#1B36A3")
run_button.grid(row=4, column=0, columnspan=2, pady=10)

# Run Button (Unmount)
unmount_button = ctk.CTkButton(app, text="Unmount Image", command=lambda: run_batch_script('unmount'), fg_color="#1B36A3")
unmount_button.grid(row=4, column=1, columnspan=2, pady=10)

work_site()
print(pwd)
app.mainloop()
