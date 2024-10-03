# Defines the keys used to parse the log entries. Each key corresponds to a specific field in the log file.

LOG_KEYS = ['version', 'account-id', 'interface-id', 'srcaddr', 'dstaddr','srcport', 
            'dstport', 'protocol', 'packets', 'bytes', 'start', 'end', 'action', 'log-status']

# Path to the CSV file containing protocol mappings. This file is used to look up protocol numbers and their corresponding names.
PROTOCOL_FILE = 'files/protocols.csv'

# Path to the JSON file where the protocol mappings will be saved after being read from the CSV file.
PROTOCOL_JSON = 'files/protocols.json'

# The tag used to represent entries that do not match any defined protocol mapping. This helps in categorizing unmatched logs.
UNTAGGED = 'Untagged'

# Base directory path for saving output files generated during the log analysis process.
OUTPUT_PATH = 'output/'

# Header for the tag count output CSV file, specifying the format of the data stored in that file.
TAG_COUNT_HEADER = 'Tag,Count'

# Header for the port/protocol combination count output CSV file, specifying the format of the data stored in that file.
PORT_PROTOCOL_COUNT_HEADER = 'Port,Protocol,Count'