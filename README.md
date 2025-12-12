# 📁 Folder Capacity Scanner

**Folder Capacity Scanner** is a powerful, user-friendly Python utility designed to help you audit your disk usage efficiently. It specializes in finding **large folders** that are either **old/dormant** (candidates for deletion/archival) or **recently added** (checking what's eating up space now).

![Python Version](https://img.shields.io/badge/python-3.x-blue)
![License](https://img.shields.io/badge/license-GPLv3-green)

---

## 🚀 Key Features

*   **Task-Based Scanning:** Choose between finding "Dormant Data" (old) or "Recent Additions" (new).
*   **Split-Pane Interface:** Watch the real-time activity log on the left while your "Hit List" of found folders populates on the right.
*   **Smart Optimization:** Uses a "Short-Circuit" algorithm. Once a folder exceeds your size limit (e.g., 1GB), the scanner stops counting and flags it immediately. This makes scanning large drives significantly faster.
*   **Interactive HTML Reports:** Export your results to a beautiful HTML file with "Copy Path" buttons, making it easy to paste folder paths directly into Windows Explorer.
*   **Quick Selects:** preset dropdowns for common timeframes (e.g., "6 Months", "1 Year") and sizes (e.g., "500 MB", "5 GB").

---

## 🛠️ Installation

1.  **Install Python:** Ensure you have Python installed (Version 3.6 or higher).
2.  **Clone/Download:** Download this repository or script to your computer.
3.  **Install Dependencies:**
    You need the `tkcalendar` library for the date picker.
    ```bash
    pip install tkcalendar
    ```

---

## 📖 How to Use

1.  **Launch the App:**
    ```bash
    python folder_scanner_app.py
    ```

2.  **Select Target:**
    Click **"Browse..."** to pick the drive or folder you want to scan (e.g., `D:\` or `C:\Users\Name\Documents`).

3.  **Choose Your Mission:**
    *   **Find Dormant Data:** Select this to find old projects or archives you haven't touched in ages. (Checks *Modification Date*).
    *   **Find Recent Additions:** Select this to see what you've downloaded or installed recently. (Checks *Creation Date*).

4.  **Set Criteria:**
    *   **Time Horizon:** How far back/forward to look (e.g., "Older than 1 Year").
    *   **Minimum Size:** Folders smaller than this will be ignored.

5.  **Start Scan:**
    Click **🚀 Start Scan**.
    *   **Left Pane:** Shows what the scanner is doing.
    *   **Right Pane:** Shows the folders that match your criteria.

6.  **Export Results:**
    *   **💾 Save Text Report:** A simple `.txt` list.
    *   **🌐 Save HTML Report:** A web-based report with "Copy Path" buttons (Recommended).

---

## 💡 Tips
*   **"Truncated" Sizes:** If you see a result like `> 1000 MB (Limit Reached)`, it means the folder is *at least* that big. The scanner stopped counting to save you time.
*   **Windows Permissions:** If the scanner skips a folder (e.g., `C:\Windows\System32`), it's usually because it requires Administrator permissions. Run your terminal as Administrator if you need to scan system files.

---

## 📜 License
This project is licensed under the GNU General Public License v3.0.
Original concept by Bora Noyan.
Refactored and enhanced by Google's Gemini.
