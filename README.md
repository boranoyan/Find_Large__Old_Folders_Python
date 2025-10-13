# Find Large & Old/New Folders Utility

A user-friendly desktop application for Windows to find folders that are larger than a specified size and are either older or newer than a given date. This tool helps users identify large, forgotten folders or recently modified large directories to better manage disk space.



---

## 🌟 Features

-   **Combined Functionality**: Merges the logic of finding both old and recent large folders into a single application.
-   **Intuitive GUI**: A clean and simple interface built with Tkinter, eliminating the need for command-line arguments.
-   **Flexible Criteria**:
    -   Select any target folder to scan recursively.
    -   Use a calendar to easily pick a reference date.
    -   Specify a minimum folder size in Megabytes (MB).
    -   Choose to find folders **older** or **newer** than the reference date.
-   **Real-Time Feedback**: A results panel displays findings as they occur, and a status bar shows the current activity.
-   **Responsive & Stoppable**: The scanning process runs in a separate thread to keep the UI from freezing, and a "Stop Scan" button allows you to cancel the process at any time.
-   **Save Results**: Easily save the scan results to a `.txt` file for later review.
-   **Help & About**: Built-in documentation explains how to use the app and provides important disclaimers.

---

## 🛠️ Setup and Usage

### Prerequisites

-   Python 3.x
-   Windows Operating System (The script relies on Windows-specific path-handling, especially regarding long path names).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/boranoyan/Find_Large__Old_Folders_Python.git(https://github.com/boranoyan/Find_Large__Old_Folders_Python.git)
    cd your-repo-name
    ```

2.  **Install the required Python library:**
    The application uses `tkcalendar` for the date-picker widget. Install it using pip:
    ```bash
    pip install tkcalendar
    ```

### Running the Application

Execute the script from your terminal:

```bash
python folder_scanner_app.py
