# Semester Schedule Formatter

## Overview

This Python script converts a semester schedule from a CSV file into a structured text format. The output organizes each date with:

- **Note**: The day of the week or a holiday (if applicable).
- **Status**: Any scheduled event(s) for that day.

## Example Output

```
01/01/2025 : Note : Wednesday + No class day
01/01/2025 : Status : Orientation … , Validation ..
02/01/2025 : Note : Thursday
02/01/2025 : Status : Commencement of Classes
```

## Features

- Parses CSV files containing semester schedules.
- Extracts dates, holidays, and event details.
- Formats the output in a readable structure.
- Ignores empty or irrelevant entries.

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/your-username/semester-schedule-formatter.git
   ```
2. Navigate to the project directory:
   ```sh
   cd semester-schedule-formatter
   ```


## Usage

Run the script with a CSV file as input:

```sh
python format_schedule.py input.csv
```

The script will generate an output text file (`output.txt`) automatically.

## CSV Format

The input CSV should contain the following columns:

- **Serial Number**: A unique identifier for each entry.
- **Status**: Description of scheduled events.
- **From Date**: Start date of the event (in `DD/MM/YYYY` format).
- **From Day**: Day of the week for the start date.
- **To Date**: End date of the event (if applicable, in `DD/MM/YYYY` format).
- **To Day**: Day of the week for the end date.

Example:

```
Serial Number,Status,From Date,From Day,To Date,To Day
1,Orientation,01/01/2025,Wednesday,01/01/2025,Wednesday
2,Commencement of Classes,02/01/2025,Thursday,02/01/2025,Thursday
3,Holiday,03/01/2025,Friday,,
```

## Author

[Hiral Garg]

