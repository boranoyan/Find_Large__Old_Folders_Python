# 🛠️ Development Documentation

This document provides a technical overview of the **Folder Capacity Scanner** architecture, design decisions, and guidelines for future contributors.

## 🏗️ Architecture Overview

The application is built using **Python** and **Tkinter** (for the GUI). It follows a monolithic structure within a single file (`folder_scanner_app.py`) for ease of deployment, but logically separates concerns into:
1.  **UI Layer:** Handles widget layout, user input, and event dispatching.
2.  **Logic/Worker Layer:** Executes the file system traversal in a separate thread to ensure the UI remains responsive.
3.  **Reporting Layer:** Formats and exports data to Text or HTML.

### Key Libraries
*   `tkinter` & `ttk`: Native GUI framework.
*   `threading`: For asynchronous scanning.
*   `os` & `time`: For file system traversal and metadata retrieval.
*   `tkcalendar`: For the date picker widget.

---

## 🧠 Core Logic & Algorithms

### 1. The "Short-Circuit" Optimization
Scanning deep directory trees on slow HDDs can be time-consuming. We mitigate this using a **size threshold cutoff**.

**Implementation:** `get_folder_size(folder_path, limit_bytes)`
*   The function iterates through files in a directory recursively.
*   It maintains a running `total_size` accumulator.
*   **Crucial Step:** In every iteration, it checks: `if limit_bytes and total_size > limit_bytes: return total_size, True`.
*   **Result:** Calculating the size of a 100GB folder when the user only cares about ">1GB" takes milliseconds instead of minutes.

### 2. Date Comparison Logic
The tool switches logic based on the user's "Scan Mode":
*   **Dormant Mode:** Uses `os.path.getmtime(path)`. Logic: `folder_date < reference_date`.
*   **Recent Mode:** Uses `os.path.getctime(path)`. Logic: `folder_date > reference_date`.
*   *Note:* Timestamps are compared as Unix Epoch floats for speed.

### 3. Threading Model
*   **Main Thread:** Manages the Tkinter `mainloop`.
*   **Worker Thread:** The `start_scan` method spawns a `threading.Thread` targeting `process_folders_thread`.
*   **Communication:**
    *   The worker thread **cannot** directly modify UI widgets (it's not thread-safe).
    *   We use `self.root.after(0, func, arg)` to schedule UI updates (like `update_log`) back onto the Main Thread safely.
*   **Stop Signal:** A `threading.Event` (`self.stop_event`) is checked periodically inside the scan loops. If set, the loops break immediately.

---

## 🖥️ UI Structure (Tkinter)

The UI is divided into a standard `pack` layout:
1.  **Configuration Frame:** `ttk.LabelFrame` groupings for "Target" and "Logic".
2.  **Split View:** A `tk.PanedWindow` (Horizontal) containing:
    *   **Left:** `ScrolledText` for logs.
    *   **Right:** `ScrolledText` for findings.
3.  **Status Bar:** A simple `ttk.Label` updated rapidly via `root.after`.

---

## 🌐 HTML Report Generation
The HTML generator is embedded directly in the class.
*   **Mechanism:** It constructs a raw Python string with an f-string template.
*   **JavaScript Integration:** Includes a raw JS block (`r'''...'''`) to handle clipboard operations.
*   **Escaping:** Special care is taken to escape Windows paths (backslashes) for both the HTML display and the JavaScript string literals.

---

## 🚀 Future Roadmap / Todo
*   [ ] **Multiprocessing:** Use `multiprocessing` instead of `threading` for true parallel disk I/O (though GIL impact is minimal on I/O bound tasks).
*   [ ] **File Type Analysis:** Add a chart showing *what* kind of files are taking up space (e.g., .mp4 vs .log).
*   [ ] **Delete Action:** Add a context menu to delete folders directly from the "Found Items" pane (Requires strict "Are you sure?" safety checks).
