import json
import os
import sys
import csv
from variables import LOG_KEYS, PROTOCOL_JSON, UNTAGGED, OUTPUT_PATH, PORT_PROTOCOL_COUNT_HEADER, TAG_COUNT_HEADER
import logging

logging.basicConfig(level=logging.INFO)

def loadProtocolJSON(json_file):
    """
    Loads a JSON file containing protocol mappings into a dictionary.
    
    This function checks whether the specified JSON file exists and reads its contents. 
    If the file does not exist, an error message is printed, and the function returns None. 
    It uses the json library to parse the JSON file into a Python dictionary. 
    The dictionary maps protocol numbers (as keys) to protocol names (as values). 
    If there is an issue while reading or parsing the JSON, an error message is printed, 
    and the function also returns None.

    Args:
        json_file (str): Path to the JSON file containing protocol mappings.

    Returns:
        dict: A dictionary mapping protocol numbers to protocol names or None if loading fails.
    """
    
    if not os.path.isfile(json_file):
        print(f"Error: JSON file '{json_file}' not found.")
        return None

    try:
        with open(json_file, mode='r') as file:
            protocol_list = json.load(file) 
        return protocol_list
    except Exception as e:
        print(f"Error reading JSON file '{json_file}': {e}")
        return None

def createLookupMap(lookup_file):
    """
    Creates a mapping of port/protocol combinations to tags from a CSV file.
    
    This function reads a CSV file that specifies how different ports and protocols should be tagged. 
    It expects each row in the CSV to contain at least three columns: port, protocol, and tag. 
    The function initializes an empty dictionary to hold the mappings. It reads the CSV file using 
    the csv module, skipping the header row. For each row, it validates that all required columns 
    are present and that the port is a valid integer. If any validations fail, appropriate error 
    messages are logged, and the invalid row is skipped. For valid entries, it constructs a key 
    using the port and protocol (formatted as 'port_protocol') and assigns the corresponding tag to that key.

    Args:
        lookup_file (str): Path to the CSV lookup file containing port/protocol mappings.

    Returns:
        dict: A dictionary mapping 'port_protocol' keys to tags.
    """
    
    Map = dict()
    
    try:
        with open(lookup_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for parts in reader:
                if len(parts) < 3:
                    logging.warning(f"Skipping row due to insufficient columns: {parts}")
                    continue
                
                port = parts[0].strip()
                protocol = parts[1].strip().lower()
                tag = parts[2].strip()
                
                if not tag:
                    logging.error(f"Tag is empty for port={port}, protocol={protocol}. Skipping this entry.")
                elif not protocol:
                    logging.error(f"Protocol is empty for port={port}, protocol={protocol}. Skipping this entry.")
                elif not port.isdigit():
                    logging.error(f"Port '{port}' for Protocol={protocol} is not valid. Skipping this entry.")
                else:
                    key = f'{port}_{protocol}' 
                    if key in Map:
                        logging.error(f"Duplicate found for port={port}, protocol={protocol}. Skipping Tag {tag}.")
                    else:
                        Map[key] = tag
                
    except Exception as e:
        print(f"Error reading lookup file '{lookup_file}': {e}")
        sys.exit(1)

    return Map


def createLogMap(log_str, log_number):
    """
    Parses a single log entry string into a dictionary mapping log keys to values.
    
    This function takes a single log entry as a string and splits it into individual components 
    based on whitespace. It initializes an empty dictionary to hold the key-value pairs for 
    the log entry. The function first checks if the number of components matches the expected 
    number of log keys (defined in the LOG_KEYS variable). If the number of fields is incorrect, 
    an error message is logged, and the function returns None. 

    Next, it iterates through the components, mapping them to their corresponding keys in the 
    LOG_KEYS list. It also checks that each value is not empty. If any values are empty or if 
    the port numbers or protocol are invalid (not integers or out of expected ranges), 
    error messages are logged, and None is returned. If everything is valid, the function returns 
    the dictionary representing the log entry.

    Args:
        log_str (str): A single log entry as a string.
        log_number (int): The log entry number for logging errors.

    Returns:
        dict: A dictionary mapping log keys to values or None if parsing fails.
    """
    
    parts = log_str.split(' ')
    Map = dict()
  
    if len(parts) < len(LOG_KEYS):
        logging.error(f"Log entry {log_number} has incorrect number of fields: expected {len(LOG_KEYS)}, got {len(parts)}")
        return None 
    
    for key, value in zip(LOG_KEYS, parts):
        Map[key] = value.strip()  

        if not value.strip(): 
            logging.error(f"Log entry {log_number} is missing required field: {key} (value is empty)")
            return None
    
    if len(Map) < len(LOG_KEYS):
        logging.error(f"Log entry {log_number} is missing some fields")   
    elif not Map['srcport'].isdigit() or not Map['dstport'].isdigit():
        logging.error(f"Log entry {log_number} has invalid port number: srcport={Map['srcport']}, dstport={Map['dstport']}. They should be integers.")
    elif not Map['protocol'].isdigit() or not (0 <= int(Map['protocol'].strip()) < 256):
        logging.error(f"Log entry {log_number} has invalid protocol: {Map['protocol']}. It should be a valid Protocol.")
    else:
        return Map
    
    return None


def createOutputFile(filepath, output, header=''):
    """
    Writes the output dictionary to a CSV file.
    
    This function takes a file path and a dictionary of data that should be written to a CSV file. 
    It first opens the specified file in write mode. If a header string is provided, it writes 
    that header to the first line of the file. The function then iterates over the key-value pairs 
    in the output dictionary, formatting each pair as a CSV line. Each line is written to the file. 
    If there is an error during the writing process, an error message is printed, and the program 
    terminates.

    Args:
        filepath (str): Path to the output CSV file.
        output (dict): Dictionary to write to the CSV.
        header (str): Header to include in the CSV file.
    """

    try:
        with open(filepath, mode='w') as file:
            file.write(header+'\n')

            for key,value in output.items():
                row = f'{key},{value}'
                file.write(row + '\n')
    except Exception as e:
        print(f"Error writing to output file '{filepath}': {e}")
        sys.exit(1)


def analyzeLogs(log_file, lookup_file, filter=''):
    """
    Analyzes log entries to generate counts of tags and port/protocol combinations.

    The function loads protocol mappings from a JSON file and creates a lookup map 
    from a CSV file. It processes the log file line by line, parsing each entry and 
    updating counts based on the destination port, protocol, and associated tags. 
    Entries matching the filter are skipped.

    After processing, it logs the total counts and creates output CSV files for tag 
    counts and port/protocol counts.

    Args:
        log_file (str): Path to the log file.
        lookup_file (str): Path to the CSV file with port/protocol mappings.
        filter (str): Optional action filter (e.g., 'ACCEPT', 'REJECT').
    """
    
    protocolsMap = loadProtocolJSON(PROTOCOL_JSON)
    lookupMap = createLookupMap(lookup_file)
    
    tagMap = dict()
    portProtocolMap = dict()
    
    log_count = 0
    error_logs = 0
    
    try:
        with open(log_file, mode='r') as file:
            for line in file:
                
                line = line.strip()
    
                if not line:
                    continue
                
                log_count += 1
                
                logMap = createLogMap(line,log_count)
                
                if logMap is None :
                    error_logs += 1
                    continue
                elif logMap['action'] == filter:
                    continue
                
                port = logMap['dstport']
                protocol = protocolsMap[logMap['protocol']]

                lookupkey = f'{port}_{protocol}'

                key = lookupMap.get(lookupkey, UNTAGGED)
                tagMap[key] = tagMap.get(key, 0) + 1
                
                portProtocolKey = f"{port},{protocol}"
                portProtocolMap[portProtocolKey] = portProtocolMap.get(portProtocolKey, 0) + 1
                
        logging.info(f"Processed {log_count} log entries, with {error_logs} errors.")
        
        log_filename_raw =  os.path.splitext(os.path.basename(log_file))[0]
        tag_output_file = f'{OUTPUT_PATH}{log_filename_raw}_tag_count.csv'
        port_protocol_file = f'{OUTPUT_PATH}{log_filename_raw}_port_protocol_count.csv'
        
        createOutputFile(tag_output_file, tagMap, TAG_COUNT_HEADER)
        createOutputFile(port_protocol_file, portProtocolMap, PORT_PROTOCOL_COUNT_HEADER)
        
    except Exception as e:
        print(f"Error processing log file '{log_file}': {e}")
        sys.exit(1)


def main():
    """
    The main entry point of the log analyzer program.
    
    This function checks the command line arguments to ensure the user has provided the necessary 
    file paths for the log file and lookup file. It also handles optional filtering of log entries. 
    The function validates that the log file exists and has a correct file extension ('.txt') 
    and that the lookup file exists and is in CSV format. If any validation fails, appropriate error 
    messages are logged, and the program exits. Finally, the analyzeLogs function is called to 
    process the logs based on the provided parameters.

    Returns:
        None
    """
    
    if len(sys.argv) < 3:
        print("Usage: python script.py <log_file> <lookup_file> [FILLTER]")
        sys.exit(1)

    log_file = sys.argv[1]
    lookup_file = sys.argv[2]

    filter_action = sys.argv[3] if len(sys.argv) > 5 else ''
    
    if not os.path.isfile(log_file):
        logging.error(f"Log file '{log_file}' not found.")
        sys.exit(1)
    if not log_file.lower().endswith( '.txt'):
        logging.error(f"Log file '{log_file}' does not have a valid extension. It must be '.txt'.")
        sys.exit(1)
        
    if not os.path.isfile(lookup_file) or not lookup_file.lower().endswith('.csv'):
        logging.error(f"Lookup file '{lookup_file}' is either not found or not in CSV format.")
        sys.exit(1)

    if filter_action not in ['', 'ACCEPT', 'REJECT']:
        print("Error: Invalid filter action. It must be 'ACCEPT', 'REJECT', or empty.")
        sys.exit(1)

    analyzeLogs(log_file, lookup_file, filter_action)

if __name__ == "__main__":
    main()