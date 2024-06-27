# Usage Documentation for `large_folders.py`

## Overview
This script is designed to recursively scan a specified directory and its subdirectories, identifying folders that are both older than a specified date and larger than a specified size. The results are saved to an output file.

## Command-line Arguments

- **path**: The root directory to start the scan.
- **date**: The reference date in `dd-mm-yyyy` format. Folders modified before this date will be considered.
- **size**: The minimum size (in megabytes) of the folders to be considered.
- **--file**: (Optional) The name of the file to save the results. If not specified, the default output file is `output.txt`.

## Example Usage

```sh
python large_folders.py "F:\IT" "01-01-2021" 2000 --file output-it-folder2.txt
```

## Detailed Description

- **path**: The script will start scanning from this root directory.
- **date**: The script will convert this date to an epoch time and use it to compare the last modified times of folders.
- **size**: The script will convert this size from megabytes to bytes for comparison.
- **--file**: If provided, the script will save the results to this file. If not provided, it defaults to `output.txt`.

## Functions

### `convert_mb_to_bytes(mb)`
Converts megabytes to bytes.

### `convert_bytes_to_mb(bytes)`
Converts bytes to megabytes.

### `convert_date_to_epoch(date_string)`
Converts a date string in `dd-mm-yyyy` format to epoch time.

### `convert_epoch_to_date(epoch)`
Converts epoch time to a date string in `dd-mm-yyyy` format.

### `process_folder(folder_path, date, size, output_file)`
Recursively processes folders starting from `folder_path`. Checks each folder's last modified date and size. If a folder is older than the given date and larger than the given size, it saves the folder's details to the output file.

### `get_folder_size(folder_path, size)`
Calculates the total size of a folder. If the size exceeds the specified size during calculation, it returns the size immediately.

### `save_folder_to_file(folder_path, output_file, folder_date, folder_size)`
Saves the details of a folder to the output file.

## Script Execution

The script begins by parsing the command-line arguments. It then converts the provided date and size to epoch time and bytes, respectively. If the date conversion fails, the script exits with an error message.

The script then calls `process_folder` with the specified path, reference date, size, and output file. The `process_folder` function handles the recursive scanning and filtering of folders based on the date and size criteria. If a qualifying folder is found, its details are saved to the specified output file.

## Important Notes

- **Backup Warning**: Ensure you have a valid backup of your data before running this script.
- **Disclaimer**: The script is provided as-is. The author takes no responsibility for any damage, data loss, or unintended consequences resulting from its use. Use at your own risk.

## Contact Information

- **Programmer**: Bora Noyan
- **Contact**: bora@boranoyan.com
- **Website**: www.boranoyan.com

## License

This script is licensed under the GNU General Public License v3.0. For the full license text, see the LICENSE file in the project root.

---
