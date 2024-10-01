# Illumio Technical Assessment

## Assumptions

- The input log file strictly follows the AWS Flow Logs format.
- Each log entry contains necessary fields until the status field, which marks the end of relevant data for processing.
- The analysis focuses exclusively on logs with version 2; other versions will not be considered.
- The program ignores case sensitivity for the action and protocol entries.
- Future enhancements may include more robust error handling for input files, ensuring invalid or incorrectly formatted log entries are logged and skipped gracefully.
- The analyzer has been tested with sample logs, including handling of other versions and accounting for blank spaces in log entries.
- Tested with case-insensitive lookups using `lookup.csv` and `lookup.txt`, demonstrating that both file types can be utilized as the code does not rely on the CSV library.

## Future Assumptions
- Input File Handling: Future enhancements may include:
- Implementing more robust error handling and validation for input files.
- Logging any invalid or incorrectly formatted log entries for review.
- Supporting additional log formats or versions as needed.

## Features

- **Filtering Accepted Logs**: The analyzer can be configured to filter only accepted logs, allowing you to focus on successful connections.
- **Output Generation**: Generates two CSV files:
  - **Tag Count**: Contains the count of occurrences for each tag found in the logs.
  - **Port/Protocol Count**: Contains the count of occurrences for each port/protocol combination.
- **Flexible Input**: You can easily specify the file paths for log files, lookup tables, and output files in a dedicated `variables.py` file.
- **No External Libraries**: The code is implemented without using additional libraries, ensuring compatibility and simplicity.

## Code Explanation

### Core Functions

1. **createProtocolList(protocol_file)**:
   - Reads a protocol mapping file and creates a list of protocols indexed by their decimal values (0-255).
   - The protocol mapping CSV file is downloaded from the AWS log link provided in the assignment.
   - Returns a list, which provides direct access to protocols without the overhead of a hashmap.

2. **createLookupMap(lookup_file)**:
   - Reads the lookup file and creates a mapping of port/protocol combinations to tags.
   - This mapping is stored in a dictionary for quick access during log analysis.

3. **createLogMap(log_str)**:
   - Parses a log entry and creates a dictionary mapping each field to its respective value.
   - This function allows for flexibility in analyzing other aspects in the future. Instead of just focusing on ports and protocols, we can expand the `analyzeLogs` function to accommodate additional log-related data.

4. **createOutputFile(filepath, output, header)**:
   - Writes the output data to a specified CSV file, including an optional header.

5. **analyzeLogs(log_file, protocol_file, lookup_file, tag_output_file, port_protocol_file, skip)**:
   - The main analysis function that:
     - Reads log entries.
     - Filters based on specified criteria (version and action).
     - Updates counts for tags and port/protocol combinations.
     - Calls the `createOutputFile` function to generate the output files.

## Input and Output
### Input:

- Log file containing flow logs.
- Lookup table for port/protocol mappings (supports both CSV and TXT formats).
- Protocol mapping file.

### Output:

- tag_count_output.csv: Contains tag counts.
- port_protocol_output.csv: Contains port/protocol combination counts.

### Usage

1. **Setup**: Ensure that you have Python installed on your machine.

2. **File Locations**: Specify the following variables in  `file_location.py` and `variables.py`:
   - LOG_FILE: Path to the AWS flow log file.
   - LOOKUP_FILE: Path to the CSV or TXT file containing the lookup table.
   - PROTOCOL_FILE: Path to the CSV file containing protocol mappings.
   - TAG_COUT_OUTPUT: Path where the tag count CSV will be saved.
   - PORT_PROTOCOL_OUTPUT: Path where the port/protocol count CSV will be saved.
   - SKIP: (Optional) Define an action to skip during analysis (e.g., "REJECT").

3. **Run the Analyzer**: Execute the `loganalyzer.py` file. The output files will be generated in the specified locations.

```bash
python loganalyzer.py
```

