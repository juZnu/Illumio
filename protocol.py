import csv
import json
import sys
from variables import PROTOCOL_FILE, PROTOCOL_JSON

def createProtocolList(protocol_file, output_json_file):
    """
    Reads a CSV file of protocol mappings and saves them as a JSON file.

    This function initializes an empty dictionary to store protocol mappings. It opens the specified 
    CSV file, skipping the header row, and iterates through each row to extract protocol information. 
    The first column is converted to an integer (the protocol number), and the second column is converted 
    to a lowercase string (the protocol name). Valid entries are added to the dictionary using the 
    protocol number as the key.

    If any errors occur during file operations or data extraction (e.g., missing values, invalid 
    integers), they are caught and handled gracefully.

    After constructing the dictionary, it writes the contents to a specified JSON file, providing a 
    persistent format for the protocol mappings.

    Args:
        protocol_file (str): Path to the CSV file containing protocol mappings.
        output_json_file (str): Path to the output JSON file to save the mappings.
    """
    
    protocol_dict = {}  

    try:
        with open(protocol_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  
            for parts in reader:
                try:
                    decimal = int(parts[0].strip())
                    protocol = parts[1].strip().lower()
                    if not protocol:
                        continue  
                    protocol_dict[decimal] = protocol 
                except (ValueError, IndexError):
                    continue 

    except FileNotFoundError:
        print(f"Error: Protocol file '{protocol_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading protocol file '{protocol_file}': {e}")
        sys.exit(1)

    try:
        with open(output_json_file, mode='w') as json_file:
            json.dump(protocol_dict, json_file)
        print(f"Protocol list saved to '{output_json_file}'")
    except Exception as e:
        print(f"Error writing to protocol JSON file '{output_json_file}': {e}")
        sys.exit(1)

def main():
    createProtocolList(PROTOCOL_FILE, PROTOCOL_JSON)

if __name__ == "__main__":
    main()
