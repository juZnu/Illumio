# README for Flow Log Analyzer

## Overview
This program parses a flow log file containing network flow data and maps each row to a tag based on a lookup table provided in a CSV file format. The output includes the count of matches for each tag and the count of matches for each port/protocol combination.

## Features
- Parses flow logs with a defined format.
- Matches flow logs against a lookup table to categorize them with tags.
- Generates two output files: one for tag counts and another for port/protocol combination counts.

## Input Files
1. **Flow Log File**: Contains the flow logs to be analyzed. The logs must be in a specific format as outlined below.
2. **Lookup Table File**: A CSV file containing mappings of `dstport`, `protocol`, and `tag`. This file is used to determine the tags applied to the flow logs.

### Example Flow Log Entry

