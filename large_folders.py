#python large_folders.py "F:\IT" "01-01-2021" 2000 --file output-it-folder2.txt

import os
import argparse
import time

def convert_mb_to_bytes(mb):
    bytes = mb * 1024 * 1024
    return bytes
def convert_bytes_to_mb(bytes):
    mb = bytes / (1024 * 1024)
    return mb

def convert_date_to_epoch(date_string):
    try:
        date = time.strptime(date_string, "%d-%m-%Y")
        epoch = time.mktime(date)
        return epoch
    except ValueError:
        print("Invalid date format. Please provide a date in the format dd-mm-yyyy.")
        return None

def convert_epoch_to_date(epoch):
    date = time.strftime("%d-%m-%Y", time.localtime(epoch))
    return date

def process_folder(folder_path, date, size, output_file):
    print("in process folder")
    for root, dirs, files in os.walk(folder_path):
        #print("in 1st for")
        print(dirs)
        if not files or not dirs:
            print("Empty folder")
            continue
        else:
            for dir_name in dirs:
                #print("in 2nd for")
                dir_path = os.path.join(root, dir_name)
                try:
                    folder_date = os.path.getmtime(dir_path)
                except FileNotFoundError:
                    print(f"Error accessing folder: {dir_path}. Skipping...")
                    continue
                #print(convert_epoch_to_date(folder_date))
                if folder_date < date:

                    print("Old Folder Found")
                    print(dir_path)
                    folder_size = get_folder_size(dir_path,size)
                    if folder_size > size:
                        print("Large Folder Found")
                        save_folder_to_file(dir_path, output_file, folder_date, folder_size)
                    else:
                        print(" Skipping Smaller Size...")
                else:
                    print(" Skipping ...")



def get_folder_size(folder_path,size):
    total_size = 0
    for dir_path, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(dir_path, file)
            try:
                total_size += os.path.getsize(file_path)
                #print(total_size)
                print("Calculating Folder Size in MB... " + str(convert_bytes_to_mb(total_size)) , end="\r")
                if total_size > size:
                    #print("After total size " + folder_path)
                    return total_size

            except OSError as e:
                print(f"Error accessing file: {file_path}. {e}")

            #print("2nd for loop " + folder_path)
    return total_size



def save_folder_to_file(folder_path, output_file, folder_date, folder_size):

    try:
        with open(output_file, "a") as file:
            file.write("PATH= " + folder_path + " DATE= " + str(convert_epoch_to_date(folder_date)) +
                       " LARGER THAN = " + str(convert_bytes_to_mb(folder_size)) + "\n")
            print("PATH= " + folder_path + " SAVED")
    except FileNotFoundError:
        with open(output_file, "w") as file:
            file.write("PATH= " + folder_path + " DATE= " + str(convert_epoch_to_date(folder_date)) +
                       " LARGER THAN = " + str(convert_bytes_to_mb(folder_size)) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''
    Programmer: Bora Noyan
    Contact: bora@boranoyan.com
    Website: www.boranoyan.com
    Description: This Python script checks dates and sizes of given folders and sub-folders recursively,
    generates a report as "output.txt".
    Users can provide a different file name for the report.

    IMPORTANT: This script is provided as-is and for informational purposes only.
    The author, Bora Noyan, takes no responsibility for any damage, data loss,
    or any unintended consequences resulting from the use of this script.
    Users are advised to review the code and use it at their own risk.
    If you choose to use this script, you acknowledge that the author will not be liable
    for any issues arising from its use.

    NOTE: Please make sure to have a valid backup of your data before running this script.
    ''', formatter_class=argparse.RawTextHelpFormatter
    )
    parser.usage = "Example usage: python large_folders.py \"F:\IT\" \"01-01-2021\" 2000 --file output-it-folder2.txt"
    parser.add_argument("path", help="The root path to start checking folders recursively")
    parser.add_argument("date", help="The reference date in dd-mm-yyyy format")
    parser.add_argument("size", type=int, help="The minimum size of the folders in bytes")
    parser.add_argument("--file", help="Optional file name to save the results")
    args = parser.parse_args()

    reference_date = convert_date_to_epoch(args.date)
    size_byte = convert_mb_to_bytes(args.size)
    if reference_date is None:
        exit(1)

    output_file = "output.txt" if args.file is None else args.file  # Specify the desired output file name

    process_folder(args.path, reference_date, size_byte, output_file)

    print("Process complete. Results saved in", output_file)
