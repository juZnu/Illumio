# Illumio Technical Assessment

## Assumptions

- The input log file doesnt need to strictly follows the AWS Flow Logs format and is expected to be in `.txt` format.
- Each log entry contains necessary fields up to the `status` field, which marks the end of relevant data for processing.
- The analysis focuses exclusively on logs with **version 2**; other versions will not be considered.
- The program ignores case sensitivity for the `protocol` entry and `tag`.
- The analyzer has been tested with sample logs, including handling of other versions and accounting for blank spaces in log entries.
- Tested with case-insensitive lookups using `lookup.csv`.
- The `lookup_file` and output files are also expected to be in CSV format.
- Error handling includes:
  - Missing or invalid file paths.
  - Incorrect file formats (e.g., `.txt` for logs, `.csv` for lookup files are expected).
  - Invalid entries in the lookup and log files.
  - Count of Sucess logs and Failure logs
- Before running `log_analyzer.py`, ensure that `protocols.py` has been executed to generate the `protocols.json` file.

## Future Assumptions

- Future enhancements may include:
  - Implementing more robust error handling and validation for input files.
  - Logging any invalid or incorrectly formatted log entries for review not limited to `port` and `protocol`.
  - Supporting additional log formats or versions as needed.

## Features

- **Filtering Accepted Logs**: The analyzer can be configured to filter only accepted logs, allowing you to focus on successful connections or viceversa.
- **Output Generation**: Generates two CSV files:
  - **Tag Count**: Contains the count of occurrences for each tag found in the logs.
  - **Port/Protocol Count**: Contains the count of occurrences for each port/protocol combination.
- **Flexible Input**: Easily specify the file paths for output folder, log keys, protocol path, and headers for output files in a dedicated `variables.py` file.
- **Very Limited External Libraries**: The script relies minimally on external libraries likes `csv`, `logging`, `os` and `json` , keeping it lightweight.

## Code Explanation

### Core Functions

- **loadProtocolJSON(json_file)**: Loads protocol mappings from a JSON file into a dictionary.
- **createLookupMap(lookup_file)**: Creates a mapping of port/protocol combinations to tags from a CSV file.
- **createLogMap(log_str, log_number)**: Parses a single log entry string into a dictionary mapping log keys to values.
- **createOutputFile(filepath, output, header='')**: Writes the output dictionary to a CSV file.
- **analyzeLogs(log_file, lookup_file, filter='')**: Analyzes log entries to generate counts of tags and port/protocol combinations.
- **main()**: The main entry point that handles user input and executes the analysis.

## Input and Output

### Input

- Log file containing flow logs.
- Lookup table for port/protocol mappings (supports CSV).
- Optional filter: 'REJECT' or 'ACCEPT'.

### Output

- `<LOG_FILE_NAME>_tag_count.csv`: Contains tag counts.
- `<LOG_FILE_NAME>_port_protocol_count.csv`: Contains port/protocol combination counts.

## Usage

1. **Setup**: Ensure that you have Python installed on your machine.
2. **Clone the Repository**: 
   ```bash
   git clone https://github.com/juZnu/Illumio.git
   ```
3. **Run Protocol Script**: Execute protocols.py to generate the protocols.json file.
4. **Run the Analyzer**: Execute the log_analyzer.py file. The output files will be generated in the specified locations.
   ```bash
   python log_analyzer.py <logfile> <lookup_file> [filter]
   ```
