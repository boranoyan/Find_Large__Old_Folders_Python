# Copyright (c) [2023] [Bora Noyan]
# This file is part of [Find_Large_Old_Folders_Python].
# Licensed under the GNU General Public License v3.0
#
# --- MODIFICATIONS by Google's Gemini ---
# - Refactored into "Folder Capacity Scanner"
# - Added "Short-circuit" optimization for faster scanning
# - Implemented "Task-Based" modes (Dormant vs. Recent)
# - Added Quick Select dropdowns for Date and Size
# - Switched to Creation Time for "Recent" scans
# - **NEW**: Split-pane UI (Activity Log vs. Found Items)
# - **NEW**: Dedicated "Save Report" button for Found items
# - **NEW**: Added HTML Export with Copy-to-Clipboard

import os
import time
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkcalendar import Calendar
import threading
from datetime import datetime, timedelta

class FolderScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📁 Folder Capacity Scanner")
        self.root.geometry("1100x750") # Made wider for split view

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.is_running = False
        self.stop_event = threading.Event()

        # --- Variables ---
        self.path_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="dormant")
        self.timeframe_var = tk.StringVar(value="1 Year")
        self.date_var = tk.StringVar(value=datetime.now().strftime("%d-%m-%Y"))
        self.size_dropdown_var = tk.StringVar(value="1 GB")
        self.size_manual_var = tk.StringVar(value="1000")
        self.status_var = tk.StringVar(value="Ready to scan.")

        # --- Menu Bar ---
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="How to Use", command=self.show_help)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About", command=self.show_about)

        # --- Main Layout ---
        main_frame = ttk.Frame(root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Scan Target
        target_frame = ttk.LabelFrame(main_frame, text="1. Scan Target", padding="10")
        target_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(target_frame, text="Folder:").pack(side=tk.LEFT, padx=5)
        self.path_entry = ttk.Entry(target_frame, textvariable=self.path_var)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(target_frame, text="Browse...", command=self.browse_folder).pack(side=tk.LEFT, padx=5)

        # 2. Scan Logic
        logic_frame = ttk.LabelFrame(main_frame, text="2. Scan Logic", padding="10")
        logic_frame.pack(fill=tk.X, pady=5)

        # Mode Selection
        mode_container = ttk.Frame(logic_frame)
        mode_container.pack(fill=tk.X, pady=5)
        ttk.Label(mode_container, text="Scan Mode:", font=('bold')).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(mode_container, text="Find Dormant Data (Old, Unused)", 
                        variable=self.mode_var, value="dormant", command=self.update_date_from_dropdown).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(mode_container, text="Find Recent Additions (New, Fresh)", 
                        variable=self.mode_var, value="recent", command=self.update_date_from_dropdown).pack(side=tk.LEFT, padx=10)

        # Grid for settings
        settings_grid = ttk.Frame(logic_frame)
        settings_grid.pack(fill=tk.X, pady=5)

        # Row 0: Timeframe
        ttk.Label(settings_grid, text="Time Horizon:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.time_combo = ttk.Combobox(settings_grid, textvariable=self.timeframe_var, state="readonly", width=15)
        self.time_combo['values'] = ("1 Week", "2 Weeks", "1 Month", "3 Months", "6 Months", "1 Year", "2 Years", "3 Years", "5 Years", "Custom")
        self.time_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.time_combo.bind("<<ComboboxSelected>>", self.on_timeframe_change)

        ttk.Label(settings_grid, text="Reference Date:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.date_entry = ttk.Entry(settings_grid, textvariable=self.date_var, width=12)
        self.date_entry.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        ttk.Button(settings_grid, text="📅", command=self.pick_date, width=3).grid(row=0, column=4, sticky=tk.W, padx=0, pady=5)

        # Row 1: Size
        ttk.Label(settings_grid, text="Minimum Size:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.size_combo = ttk.Combobox(settings_grid, textvariable=self.size_dropdown_var, state="readonly", width=15)
        self.size_combo['values'] = ("100 MB", "250 MB", "500 MB", "1 GB", "2 GB", "5 GB", "10 GB", "20 GB", "Custom")
        self.size_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.size_combo.bind("<<ComboboxSelected>>", self.on_size_change)

        ttk.Label(settings_grid, text="Size (MB):").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.size_entry = ttk.Entry(settings_grid, textvariable=self.size_manual_var, width=12)
        self.size_entry.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)

        # --- Control Frame ---
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        self.start_button = ttk.Button(control_frame, text="🚀 Start Scan", command=self.start_scan)
        self.start_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.stop_button = ttk.Button(control_frame, text="🛑 Stop Scan", command=self.stop_scan, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # --- Split Results View ---
        # Using a PanedWindow to separate Log and Results
        paned_window = tk.PanedWindow(main_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=4)
        paned_window.pack(fill=tk.BOTH, expand=True, pady=5)

        # Left Pane: Activity Log
        left_frame = ttk.LabelFrame(paned_window, text="Activity Log (Scanned Areas)", padding="5")
        paned_window.add(left_frame, width=450) # Initial width

        self.log_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, height=15, state=tk.DISABLED, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Right Pane: Found Items
        right_frame = ttk.LabelFrame(paned_window, text="Found Items (Matches Criteria)", padding="5")
        paned_window.add(right_frame)

        self.found_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, height=15, state=tk.DISABLED, font=("Consolas", 9))
        self.found_text.pack(fill=tk.BOTH, expand=True)

        # Export Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.save_txt_btn = ttk.Button(btn_frame, text="💾 Save Text Report", command=self.save_results)
        self.save_txt_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        
        self.save_html_btn = ttk.Button(btn_frame, text="🌐 Save HTML Report", command=self.save_html_results)
        self.save_html_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))
        
        # --- Status Bar ---
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=5)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize calculations
        self.update_date_from_dropdown()

    # --- Logic Helpers ---

    def on_timeframe_change(self, event=None):
        val = self.timeframe_var.get()
        if val == "Custom":
            return
        self.update_date_from_dropdown()

    def update_date_from_dropdown(self):
        val = self.timeframe_var.get()
        if val == "Custom": return
        
        days_to_subtract = 0
        if "Week" in val:
            count = int(val.split()[0])
            days_to_subtract = count * 7
        elif "Month" in val:
            count = int(val.split()[0])
            days_to_subtract = count * 30
        elif "Year" in val:
            count = int(val.split()[0])
            days_to_subtract = count * 365
            
        target_date = datetime.now() - timedelta(days=days_to_subtract)
        self.date_var.set(target_date.strftime("%d-%m-%Y"))

    def on_size_change(self, event=None):
        val = self.size_dropdown_var.get()
        if val == "Custom": return
        
        size_mb = 0
        parts = val.split()
        number = int(parts[0])
        unit = parts[1]
        
        if unit == "MB":
            size_mb = number
        elif unit == "GB":
            size_mb = number * 1024
            
        self.size_manual_var.set(str(size_mb))

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.path_var.set(folder_path)

    def pick_date(self):
        def on_date_select():
            cal_val = cal.get_date()
            self.date_var.set(cal_val)
            self.timeframe_var.set("Custom")
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

    def update_log(self, message):
        """Updates the Left Pane (Activity Log)"""
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def update_found(self, message):
        """Updates the Right Pane (Found Items)"""
        self.found_text.configure(state=tk.NORMAL)
        self.found_text.insert(tk.END, message + "\n")
        self.found_text.see(tk.END)
        self.found_text.configure(state=tk.DISABLED)

    def start_scan(self):
        if self.is_running:
            messagebox.showwarning("Busy", "A scan is already in progress!")
            return

        folder_path = self.path_var.get()
        date_str = self.date_var.get()
        size_str = self.size_manual_var.get()
        mode = self.mode_var.get()

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
        
        # Clear both text areas
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.configure(state=tk.DISABLED)
        
        self.found_text.configure(state=tk.NORMAL)
        self.found_text.delete('1.0', tk.END)
        self.found_text.configure(state=tk.DISABLED)
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_var.set("Initializing scan...")
        self.update_log(f"--- Scan Started: {datetime.now().strftime('%H:%M:%S')} ---")
        self.update_log(f"Target: {folder_path}")
        self.update_log(f"Mode: {mode.upper()}")

        scan_thread = threading.Thread(
            target=self.process_folders_thread,
            args=(folder_path, date_str, size_mb, mode)
        )
        scan_thread.start()

    def stop_scan(self):
        if self.is_running:
            self.stop_event.set()
            self.status_var.set("Stopping scan...")
            self.update_log(">>> STOP SIGNAL RECEIVED <<<")

    def scan_finished(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.stop_event.is_set():
            self.status_var.set("Scan stopped by user.")
            self.update_log("\n--- SCAN STOPPED ---")
        else:
            self.status_var.set("Scan complete!")
            self.update_log("\n--- SCAN COMPLETE ---")

    def process_folders_thread(self, folder_path, date_str, size_mb, mode):
        try:
            reference_epoch = time.mktime(time.strptime(date_str, "%d-%m-%Y"))
            limit_bytes = size_mb * 1024 * 1024
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
                
                # Update Status Bar (Rapid)
                self.root.after(0, self.status_var.set, f"Scanning: {dir_path}")
                
                try:
                    is_match = False
                    folder_timestamp = 0
                    
                    if mode == "dormant":
                        folder_timestamp = os.path.getmtime(dir_path)
                        if folder_timestamp < reference_epoch:
                            is_match = True
                            
                    elif mode == "recent":
                        folder_timestamp = os.path.getctime(dir_path)
                        if folder_timestamp > reference_epoch:
                            is_match = True

                    if is_match:
                        # Log that we are calculating size (might take a moment)
                        self.root.after(0, self.update_log, f"Candidate found: {dir_name}...")
                        
                        folder_size, is_truncated = self.get_folder_size(dir_path, limit_bytes)
                        
                        if is_truncated or folder_size > limit_bytes:
                            folder_date_str = time.strftime("%d-%m-%Y", time.localtime(folder_timestamp))
                            
                            size_display = f"{folder_size / (1024*1024):.2f} MB"
                            if is_truncated:
                                size_display = f"> {size_mb} MB (Limit Reached)"
                            
                            type_str = "Modified" if mode == "dormant" else "Created"
                            
                            result_line = f"FOUND! {dir_path} | {type_str}: {folder_date_str} | Size: {size_display}"
                            
                            # Add to Right Pane (Results)
                            self.root.after(0, self.update_found, result_line)
                            # Add brief note to Left Pane (Log)
                            self.root.after(0, self.update_log, f"--> CONFIRMED: {size_display}")

                except FileNotFoundError:
                    self.root.after(0, self.update_log, f"Skipped (Not Found): {dir_path}")
                except PermissionError:
                    self.root.after(0, self.update_log, f"Skipped (Permission): {dir_path}")
                except Exception as e:
                    self.root.after(0, self.update_log, f"Error: {e}")
        
        self.root.after(0, self.scan_finished)
        
    def get_folder_size(self, folder_path, limit_bytes=None):
        total_size = 0
        try:
            for dirpath, _, filenames in os.walk(folder_path):
                if self.stop_event.is_set(): return 0, False
                for f in filenames:
                    if self.stop_event.is_set(): return 0, False
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        try:
                            total_size += os.path.getsize(fp)
                            if limit_bytes and total_size > limit_bytes:
                                return total_size, True
                        except (FileNotFoundError, PermissionError):
                             pass
        except Exception:
             pass
        return total_size, False

    def _generate_report_filename(self, ext="txt"):
        timeframe_raw = self.timeframe_var.get()
        mode_raw = self.mode_var.get()
        size_raw = self.size_manual_var.get()
        
        # Parse timeframe for filename
        timeframe_part = "custom_date"
        if timeframe_raw != "Custom":
            parts = timeframe_raw.split()
            if len(parts) == 2:
                count = parts[0]
                unit = parts[1].lower()
                if unit.startswith("week"):
                    timeframe_part = f"{count}_wk"
                    if int(count) > 1: timeframe_part += "s"
                elif unit.startswith("month"):
                    timeframe_part = f"{count}_mth"
                    if int(count) > 1: timeframe_part += "s"
                elif unit.startswith("year"):
                    timeframe_part = f"{count}_yr"
                    if int(count) > 1: timeframe_part += "s"
        
        # Parse mode for filename
        mode_part = "unknown"
        if mode_raw == "dormant":
            mode_part = "old"
        elif mode_raw == "recent":
            mode_part = "recent"
            
        # Parse size for filename
        size_part = f"{size_raw}mb"
        
        today_date = datetime.now().strftime("%d_%m_%Y")
        
        return f"{timeframe_part}_{mode_part}_{size_part}_folders_from_{today_date}.{ext}"

    def save_results(self):
        # Text Export
        results_content = self.found_text.get("1.0", tk.END).strip()
        if not results_content:
            messagebox.showinfo("Nothing to Save", "No found items to export.")
            return

        initial_filename = self._generate_report_filename("txt")

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile=initial_filename,
            title="Export Text Report"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding='utf-8') as f:
                    # Write a header
                    f.write(f"Folder Capacity Report - {datetime.now().strftime('%d-%m-%Y %H:%M')}\n")
                    f.write(f"Scan Mode: {self.mode_var.get().upper()}\n")
                    f.write(f"Time Horizon: {self.timeframe_var.get()} (Reference Date: {self.date_var.get()})\n")
                    f.write(f"Minimum Size: {self.size_manual_var.get()} MB\n")
                    f.write("-" * 50 + "\n")
                    f.write(results_content)
                messagebox.showinfo("Success", f"Report saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def save_html_results(self):
        # HTML Export
        results_content = self.found_text.get("1.0", tk.END).strip()
        if not results_content:
            messagebox.showinfo("Nothing to Save", "No found items to export.")
            return

        # Parse text results into list of dicts
        # Line format: FOUND! {dir_path} | {type_str}: {folder_date_str} | Size: {size_display}
        rows = []
        lines = results_content.splitlines()
        regex = r"FOUND! (.*?) \| (.*?): (.*?) \| Size: (.*)"
        
        for line in lines:
            match = re.match(regex, line)
            if match:
                path, type_label, date_val, size_val = match.groups()
                rows.append({
                    "path": path,
                    "type": type_label,
                    "date": date_val,
                    "size": size_val
                })

        initial_filename = self._generate_report_filename("html")

        file_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")],
            initialfile=initial_filename,
            title="Export HTML Report"
        )
        
        if file_path:
            try:
                html_content = self._generate_html_content(rows)
                with open(file_path, "w", encoding='utf-8') as f:
                    f.write(html_content)
                messagebox.showinfo("Success", f"HTML Report saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def _generate_html_content(self, rows):
        # Generate HTML table rows dynamically
        table_rows = ""
        for row in rows:
            # Escape single quotes and backslashes in path for JavaScript string literal
            # Double backslash for regex replacement in JS, and single quote for string literal
            clean_path = row['path'].replace("\\", "/").replace("'", "\\'") 
            table_rows += f'''
            <tr>
                <td class="path-cell">
                    <div class="path-text">{row['path']}</div>
                    <button onclick="copyPath('{clean_path}')" class="copy-btn">Copy Path</button>
                </td>
                <td>{row['date']}</td>
                <td>{row['size']}</td>
            </tr>
            '''
        
        # JavaScript for copyPath function. Defined as a raw string literal to avoid
        # Python's backslash escaping rules confusing JS regex.
        js_script_block = r'''
            <script>
                function copyPath(path) {
                    // Fix slashes for Windows clipboard: replace forward slash with backslash
                    // The regex /\//g matches all forward slashes.
                    // The replacement '\\' provides a single backslash.
                    const windowsPath = path.replace(/\//g, '\\');
                    navigator.clipboard.writeText(windowsPath).then(() => {
                        alert("Path copied to clipboard:\n" + windowsPath);
                    }).catch(err => {
                        console.error('Failed to copy: ', err);
                    });
                }
            </script>
        '''

        # Main HTML content string. Using f-string with triple single quotes.
        # This allows embedded double quotes in HTML attributes/CSS without escaping.
        html_content = f'''<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Folder Capacity Report</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f4f4f9; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; }}
                .meta {{ margin-bottom: 20px; padding: 10px; background: #e9ecef; border-left: 5px solid #007bff; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #007bff; color: white; }}
                tr:hover {{ background-color: #f1f1f1; }}
                .path-cell {{ display: flex; justify-content: space-between; align-items: center; }}
                .path-text {{ word-break: break-all; margin-right: 10px; font-family: Consolas, monospace; }}
                .copy-btn {{
                    background-color: #28a745; color: white; border: none; padding: 5px 10px; 
                    border-radius: 4px; cursor: pointer; font-size: 0.85em;
                }}
                .copy-btn:hover {{ background-color: #218838; }}
                .copy-btn:active {{ transform: scale(0.98); }}
            </style>
            {js_script_block}
        </head>
        <body>
            <div class="container">
                <h1>Folder Capacity Report</h1>
                <div class="meta">
                    <p><strong>Generated:</strong> {datetime.now().strftime('%d-%m-%Y %H:%M')}</p>
                    <p><strong>Mode:</strong> {self.mode_var.get().upper()}</p>
                    <p><strong>Criteria:</strong> {self.timeframe_var.get()} | Min Size: {self.size_manual_var.get()} MB</p>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Folder Path</th>
                            <th>Date ({self.mode_var.get() == 'dormant' and 'Modified' or 'Created'})</th>
                            <th>Size</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
        </body>
        </html>'''
        return html_content

    def show_help(self):
        help_text = '''
        Folder Capacity Scanner Help:

        This tool helps you find large folders that are either very old (Dormant) or very new (Recent).

        --- THE INTERFACE ---
        
        1. Scan Configuration:
           - Use "Dormant" to find old stuff to delete.
           - Use "Recent" to see what's filling up your drive now.
           - Pick a Time Horizon (e.g. "1 Year") and a Size Limit (e.g. "1 GB").

        2. The Split View (Center):
           - LEFT PANE (Activity Log): Shows the scanner working, errors, and access warnings.
           - RIGHT PANE (Found Items): Lists ONLY the folders that match your search. This is your "Hit List."

        3. Saving:
           - Save Text Report: A simple list of found folders.
           - Save HTML Report: An interactive web file with "Copy Path" buttons.

        --- TIPS ---
        - The scan stops counting a folder's size once it hits your limit. A result like "> 1000 MB" means it's at least that big.
        - The bottom Status Bar shows the current folder being scanned in real-time.
        '''
        messagebox.showinfo("How to Use", help_text)

    def show_about(self):
        about_text = '''
        Folder Capacity Scanner
        
        Designed for efficient disk auditing.
        
        Version: 3.1 (HTML Export Edition)
        '''
        messagebox.showinfo("About", about_text)


if __name__ == "__main__":
    try:
        import tkcalendar
    except ImportError:
        pass

    root = tk.Tk()
    app = FolderScannerApp(root)
    root.mainloop()
