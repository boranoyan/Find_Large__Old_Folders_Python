📜 License
This project is licensed under the GNU General Public License v3.0. See the LICENSE file for more details.

🙏 Acknowledgements
Original script and concept by Bora Noyan.

GUI, feature enhancements, and bug fixes by Google's Gemini.



### **2. Detailed User Guide (`USER_GUIDE.md`)**

This guide is perfect for end-users who want to understand how to use every feature of your application.


# 📁 Folder Scanner Pro - User Guide

Welcome to the Folder Scanner Pro! This guide will walk you through all the features of the application and help you get started with managing your disk space.




## Table of Contents

1.  [What Does This App Do?](#what-does-this-app-do)
2.  [The Main Window](#the-main-window)
3.  [Step-by-Step: Running Your First Scan](#step-by-step-running-your-first-scan)
    -   [Step 1: Select a Target Folder](#step-1-select-a-target-folder)
    -   [Step 2: Choose a Reference Date](#step-2-choose-a-reference-date)
    -   [Step 3: Set the Minimum Size](#step-3-set-the-minimum-size)
    -   [Step 4: Choose the Comparison Type](#step-4-choose-the-comparison-type)
    -   [Step 5: Start the Scan](#step-5-start-the-scan)
4.  [Understanding the Results](#understanding-the-results)
5.  [Stopping a Scan](#stopping-a-scan)
6.  [Saving the Results](#saving-the-results)
7.  [Troubleshooting](#troubleshooting)


## What Does This App Do?

Folder Scanner Pro helps you find folders on your computer that meet specific size and date criteria. It's perfect for tasks like:
-   Finding large, old folders that are taking up space.
-   Identifying large folders that have been recently modified.
-   Cleaning up and organizing your hard drives.

The application scans a folder and all of its sub-folders recursively to find what you're looking for.


## The Main Window

The interface is divided into three main sections:
1.  **Scan Configuration**: Where you set the criteria for your search.
2.  **Controls**: Where you start and stop the scan.
3.  **Results**: Where you see the output of the scan.



## Step-by-Step: Running Your First Scan

Follow these steps to configure and run a scan.

### Step 1: Select a Target Folder

Click the **`Browse...`** button. A dialog will open, allowing you to navigate to and select the folder you want to scan.

### Step 2: Choose a Reference Date

You can either type a date into the `Reference Date` box (in `dd-mm-yyyy` format) or click the **`📅`** button to open a calendar and select a date visually. This date is the benchmark for your search.

### Step 3: Set the Minimum Size

In the `Minimum Size (MB)` box, enter a number. The scanner will only report folders that are **larger** than this size in megabytes. For example, entering `1000` will find folders larger than 1000 MB (approximately 1 GB).

### Step 4: Choose the Comparison Type

This is a key setting that tells the scanner what to look for:
-   **`Older than date`**: Finds folders that were last modified **BEFORE** the reference date you selected. This is ideal for finding old, forgotten files.
-   **`Newer than date`**: Finds folders that were last modified **AFTER** the reference date. This is useful for finding recent work or recently changed large directories.

### Step 5: Start the Scan

Once you've set your criteria, click the **`🚀 Start Scan`** button. The scan will begin, and the button will be disabled until the scan is complete. The status bar at the bottom will show you which folder is currently being checked.



## Understanding the Results

As the scanner finds folders that match your criteria, they will appear in the **Results** box. Each entry will show you:
-   **Path**: The full location of the folder.
-   **Modified Date**: The date the folder was last changed.
-   **Size**: The total size of the folder and all its contents in MB.

The results box will also show informational messages, such as when it starts calculating the size of a folder or if it encounters any warnings.

---

## Stopping a Scan

If a scan is taking too long or you wish to cancel it, simply click the **`🛑 Stop Scan`** button. The scan will halt, and the status bar will confirm that the scan was stopped by the user.



## Saving the Results

After a scan is complete (or has been stopped), you can save the output for your records.
1.  Click the **`💾 Save Results to File`** button.
2.  A "Save As" dialog will appear.
3.  Choose a location, name your file (e.g., `Old_Folders_Report.txt`), and click **`Save`**.



## Troubleshooting

### Warning: "Could not access [file]. The path may be too long..."

-   **What it means**: The script tried to check a file, but the operating system reported it couldn't be found.
-   **Most Common Cause**: The full path to the file is longer than the default 260-character limit in Windows.
-   **Solution**: You can enable long path support in Windows. See an online guide for enabling "Win32 long paths" via the Registry Editor (`regedit`) or Group Policy Editor.
-   **Is the script deleting files?**: **No.** This warning is purely informational. The script does not modify or delete any of your files.

### The Application Freezes

The application is designed to not freeze, but on very slow systems or network drives, it might become less responsive. If you need to, you can always close the window to terminate the program.



Thank you for using Folder Scanner Pro!
