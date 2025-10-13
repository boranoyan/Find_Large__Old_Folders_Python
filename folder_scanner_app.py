# Copyright (c) [2023] [Bora Noyan]
# This file is part of [Find_Large_Old_Folders_Python].
# Licensed under the GNU General Public License v3.0
#
# --- MODIFICATIONS by Google's Gemini ---
# - Merged large_folders.py and find_recent_folders.py
# - Created a Tkinter GUI for user-friendly operation
# - Fixed bug where folder size calculation stopped prematurely
# - Corrected folder traversal logic to ensure full recursive scan
# - Updated error message to be clearer and less alarming
# - Added threading to prevent GUI from freezing during scans
# - Implemented a 'Stop' button and a 'Help' menu
# - Added a calendar widget for easy date selection

import os
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkcalendar import Calendar
import threading
from datetime import datetime

class FolderScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📁 Folder Scanner Pro")
        self.root.geometry("800x600")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.is_running = False
        self.stop_event = threading.Event()

        # --- Menu Bar ---
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="How to Use", command=self.show_help)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About", command=self.show_about)

        # --- Main Frame ---
        main_frame = ttk.Frame(root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Configuration Frame ---
        config_frame = ttk.LabelFrame(main_frame, text="Scan Configuration", padding="10")
        config_frame.pack(fill=tk.X, pady=5)

        # Folder Path
        ttk.Label(config_frame, text="Target Folder:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(config_frame, textvariable=self.path_var, width=60)
        self.path_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        self.browse_button = ttk.Button(config_frame, text="Browse...", command=self.browse_folder)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Date Selection
        ttk.Label(config_frame, text="Reference Date:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%d-%m-%Y"))
        self.date_entry = ttk.Entry(config_frame, textvariable=self.date_var, width=15)
        self.date_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.cal_button = ttk.Button(config_frame, text="📅", command=self.pick_date, width=3)
        self.cal_button.grid(row=1, column=1, sticky=tk.W, padx=(120,0))

        # Size
        ttk.Label(config_frame, text="Minimum Size (MB):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.size_var = tk.StringVar(value="2000")
        self.size_entry = ttk.Entry(config_frame, textvariable=self.size_var, width=15)
        self.size_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Comparison Type
        ttk.Label(config_frame, text="Find Folders:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.compare_var = tk.StringVar(value="older")
        older_radio = ttk.Radiobutton(config_frame, text="Older than date", variable=self.compare_var, value="older")
        older_radio.grid(row=3, column=1, sticky=tk.W, padx=5)
        newer_radio = ttk.Radiobutton(config_frame, text="Newer than date", variable=self.compare_var, value="newer")
        newer_radio.grid(row=3, column=1, sticky=tk.W, padx=(150, 0))

        config_frame.columnconfigure(1, weight=1)

        # --- Control Frame ---
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        self.start_button = ttk.Button(control_frame, text="🚀 Start Scan", command=self.start_scan)
        self.start_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.stop_button = ttk.Button(control_frame, text="🛑 Stop Scan", command=self.stop_scan, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # --- Results Frame ---
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)

        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, height=15, state=tk.DISABLED)
        self.results_text.pack(fill=tk.BOTH, expand=True)

        self.save_button = ttk.Button(main_frame, text="💾 Save Results to File", command=self.save_results)
        self.save_button.pack(pady=10, fill=tk.X)
        
        # --- Status Bar ---
        self.status_var = tk.StringVar(value="Ready!")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=5)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.path_var.set(folder_path)

    def pick_date(self):
        def on_date_select():
            cal_val = cal.get_date()
            self.date_var.set(cal_val)
            top.destroy()

        top = tk.Toplevel(self.root)
        top.title("Select Date")
        try:
            current_date = datetime.strptime(self.date_var.get(), "%d-%m-%Y")
            cal = Calendar(top, selectmode='day', date_pattern='dd-mm-yyyy',
                           year=current_date.year, month=current_date.month, day=current_date.day)
        except ValueError:
             cal = Calendar(top, selectmode='day', date_pattern='dd-mm-yyyy')
        
        cal.pack(pady=20, padx=20)
        ttk.Button(top, text="Ok", command=on_date_select).pack()

    def update_results(self, message):
        self.results_text.configure(state=tk.NORMAL)
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.configure(state=tk.DISABLED)
        self.results_text.see(tk.END)

    def start_scan(self):
        if self.is_running:
            messagebox.showwarning("Busy", "A scan is already in progress!")
            return

        folder_path = self.path_var.get()
        date_str = self.date_var.get()
        size_str = self.size_var.get()

        if not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Please select a valid folder path.")
            return
        try:
            size_mb = int(size_str)
            if size_mb <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid, positive number for the size.")
            return

        self.is_running = True
        self.stop_event.clear()
        self.results_text.configure(state=tk.NORMAL)
        self.results_text.delete('1.0', tk.END)
        self.results_text.configure(state=tk.DISABLED)
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_var.set("Working... This might take a while!")

        # Run the heavy lifting in a separate thread
        scan_thread = threading.Thread(
            target=self.process_folders_thread,
            args=(folder_path, date_str, size_mb, self.compare_var.get())
        )
        scan_thread.start()

    def stop_scan(self):
        if self.is_running:
            self.stop_event.set()
            self.status_var.set("Stopping scan...")

    def scan_finished(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.stop_event.is_set():
            self.status_var.set("Scan stopped by user.")
            self.update_results("\n--- SCAN STOPPED ---")
        else:
            self.status_var.set("Scan complete!")
            self.update_results("\n--- SCAN COMPLETE ---")

    def process_folders_thread(self, folder_path, date_str, size_mb, compare_type):
        try:
            reference_epoch = time.mktime(time.strptime(date_str, "%d-%m-%Y"))
            size_bytes = size_mb * 1024 * 1024
        except ValueError:
            self.root.after(0, lambda: messagebox.showerror("Error", "Invalid date format. Please use dd-mm-yyyy."))
            self.root.after(0, self.scan_finished)
            return

        for root, dirs, _ in os.walk(folder_path):
            for dir_name in dirs:
                if self.stop_event.is_set():
                    self.root.after(0, self.scan_finished)
                    return
                
                dir_path = os.path.join(root, dir_name)
                self.root.after(0, self.status_var.set, f"Checking: {dir_path}")
                
                try:
                    folder_date = os.path.getmtime(dir_path)
                    
                    date_check_passed = False
                    if compare_type == "older" and folder_date < reference_epoch:
                        date_check_passed = True
                    elif compare_type == "newer" and folder_date > reference_epoch:
                        date_check_passed = True

                    if date_check_passed:
                        self.root.after(0, self.update_results, f"Date match found: '{dir_path}'. Calculating size...")
                        folder_size = self.get_folder_size(dir_path)
                        
                        if folder_size > size_bytes:
                            folder_size_mb = folder_size / (1024 * 1024)
                            folder_date_str = time.strftime("%d-%m-%Y", time.localtime(folder_date))
                            result_line = f"FOUND! Path: {dir_path} | Modified Date: {folder_date_str} | Size: {folder_size_mb:.2f} MB"
                            self.root.after(0, self.update_results, result_line)

                except FileNotFoundError:
                    self.root.after(0, self.update_results, f"Warning: Could not access {dir_path}. Skipping.")
                except Exception as e:
                    self.root.after(0, self.update_results, f"An error occurred with {dir_path}: {e}")
        
        self.root.after(0, self.scan_finished)
        
    def get_folder_size(self, folder_path):
        total_size = 0
        try:
            for dirpath, _, filenames in os.walk(folder_path):
                if self.stop_event.is_set(): return 0
                for f in filenames:
                    if self.stop_event.is_set(): return 0
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        try:
                            total_size += os.path.getsize(fp)
                        except FileNotFoundError:
                             self.root.after(0, self.update_results, f"Warning: Could not access {fp}. The path may be too long or the file was moved.")
        except Exception as e:
             self.root.after(0, self.update_results, f"Error getting size for {folder_path}: {e}")
        return total_size

    def save_results(self):
        results_content = self.results_text.get("1.0", tk.END).strip()
        if not results_content or ("--- SCAN COMPLETE ---" not in results_content and "--- SCAN STOPPED ---" not in results_content):
            messagebox.showinfo("Nothing to Save", "There are no results to save. Please run a scan first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile="folder_scan_results.txt",
            title="Save Results As"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding='utf-8') as f:
                    f.write(results_content)
                messagebox.showinfo("Success", f"Results saved successfully to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def show_help(self):
        help_text = """
        Welcome to Folder Scanner Pro! Here's how to get started:

        1.  **Target Folder:** Click "Browse..." to select the main folder you want to scan. The script will look through this folder and all of its sub-folders.

        2.  **Reference Date:** Enter a date or use the calendar (📅) button. This is the date you'll compare folders against.

        3.  **Minimum Size (MB):** Enter a number for the minimum folder size in Megabytes (MB). Folders smaller than this will be ignored.

        4.  **Find Folders:**
            - **Older than date:** Finds folders that were last modified BEFORE the reference date.
            - **Newer than date:** Finds folders that were last modified AFTER the reference date.

        5.  **Start Scan:** Click this to begin! The results will appear in the text box below. You can see the current folder being checked in the status bar at the bottom.

        6.  **Stop Scan:** If a scan is taking too long, you can click this to stop it at any time.

        7.  **Save Results:** Once a scan is complete, click this button to save the contents of the results box to a text file.
        """
        messagebox.showinfo("How to Use", help_text)

    def show_about(self):
        about_text = """
        Folder Scanner Pro

        Original script by: Bora Noyan
        Contact: bora@boranoyan.com
        Website: www.boranoyan.com

        GUI and modifications by Google's Gemini.

        --- IMPORTANT DISCLAIMER (from original author) ---
        This script is provided as-is and for informational purposes only.
        The author, Bora Noyan, takes no responsibility for any damage, data loss,
        or any unintended consequences resulting from the use of this script.
        Users are advised to review the code and use it at their own risk.
        If you choose to use this script, you acknowledge that the author will not be liable
        for any issues arising from its use.

        NOTE: Please make sure to have a valid backup of your data before running this script.
        """
        messagebox.showinfo("About Folder Scanner Pro", about_text)


if __name__ == "__main__":
    # You might need to install tkcalendar: pip install tkcalendar
    try:
        import tkcalendar
    except ImportError:
        print("tkcalendar library not found. Please install it using: pip install tkcalendar")
        exit(1)

    root = tk.Tk()
    app = FolderScannerApp(root)
    root.mainloop()