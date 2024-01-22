# Developed by Alex Zoller 01-22-2024
# Purpose is to take in a CSV file, and generate multiple CSV files into smaller chunks
# Keeps the headers, not tested to keep any logic or custom settings for each of the cells.
# Each chunk file retains the header names. 
#



import csv
import os
from tkinter import Tk, filedialog

def select_csv_file():
    """Open a file dialog to select a CSV file."""
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    root.destroy()
    return file_path


##########EDIT CHUNK SIZE HERE#######
def split_csv_into_chunks(file_path, chunk_size=3500):
    """Split a CSV file into smaller chunks."""
    # Ensure output directory exists
    base_name = os.path.basename(file_path).split(".")[0]
    output_folder = os.path.join(os.path.dirname(file_path), f"Splitted_{base_name}")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(file_path, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)
        file_count = 1
        records = []
        
        for row in reader:
            records.append(row)
            if len(records) == chunk_size:
                write_chunk_to_csv(output_folder, file_count, headers, records)
                records = []
                file_count += 1

        # Write any remaining records
        if records:
            write_chunk_to_csv(output_folder, file_count, headers, records)


def write_chunk_to_csv(output_folder, file_count, headers, records):
    """Write a chunk of records to a new CSV file."""
    output_file = os.path.join(output_folder, f"chunk_{file_count}.csv")
    with open(output_file, 'w', newline='') as chunk_file:
        writer = csv.writer(chunk_file)
        writer.writerow(headers)
        writer.writerows(records)
        
if __name__ == "__main__":
    csv_file_path = select_csv_file()
    if csv_file_path:
        split_csv_into_chunks(csv_file_path)
        print("CSV splitting completed.")
    else:
        print("No file selected.")
