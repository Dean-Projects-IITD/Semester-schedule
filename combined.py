import csv
import re
import sys
from collections import OrderedDict
from datetime import datetime, timedelta

# Set default encoding to UTF-8 for Python 2.7
reload(sys)
sys.setdefaultencoding('utf-8')

def format_date(date_str):
    """Convert full date to dd/mm/yy format"""
    try:
        if '/' in date_str:
            # For dates like 14/01/2025
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        else:
            # For dates like January 16
            date_obj = datetime.strptime(date_str + " 2025", '%B %d %Y')
        return date_obj.strftime('%d/%m/%y')
    except ValueError as e:
        print("Error parsing date:", date_str, str(e))
        return None

def parse_timetable_entry(line):
    """Parse lines like 'January 16 (Thursday) will work as per Tuesday timetable.'"""
    match = re.search(r'([A-Za-z]+ \d{1,2}) \([A-Za-z]+\) will work as per ([A-Za-z]+) timetable', line)
    if match:
        date_str, follows_day = match.groups()
        formatted_date = format_date(date_str)
        if formatted_date:
            return [
                "{} : Note : {}".format(formatted_date, follows_day.lower()),
                "{} : Status : {}".format(formatted_date, line.strip())
            ]
    return []

def parse_holiday_entry(holiday):
    """Parse holiday entries like 'Makar Sankranti (Tuesday, 14/01/2025)'"""
    match = re.search(r'(.+?)\s*\(([A-Za-z]+),\s*(\d{2}/\d{2}/\d{4})\)', holiday)
    if match:
        holiday_name, day_name, date_str = match.groups()
        formatted_date = format_date(date_str)
        if formatted_date:
            return [
                "{} : Note : {} + No class day".format(formatted_date, day_name.strip()),
                "{} : Status : {}".format(formatted_date, holiday_name.strip())
            ]
    return []

def process_csv(input_file, output_file):
    try:
        output_lines = []
        
        # Read the file content as a single string first
        with open(input_file, 'rb') as file:
            content = file.read().decode('utf-8-sig')
        
        # Split content into lines and process
        lines = content.splitlines()
        holiday_line = ""
        
        for line in lines[1:]:  # Skip header
            # Handle non-CSV reading for holiday line
            if "Holidays in this period:" in line:
                holiday_line = line
                continue
            
            # Skip empty lines and non-data lines
            if not line.strip() or line.startswith('S.No') or "In case of" in line or "In the event" in line:
                continue
                
            # Handle regular timetable entries
            if "will work as per" in line:
                # Extract the second part after comma (the actual data)
                parts = line.split(',', 1)
                if len(parts) > 1:
                    data = parts[1].strip()
                else:
                    data = line.strip()
                output_lines.extend(parse_timetable_entry(data))
        
        # Process holiday line if found
        if holiday_line:
            # Extract the holiday list part
            holiday_text = holiday_line[holiday_line.index("Holidays in this period:") + len("Holidays in this period:"):].strip()
            # Split by proper holiday pattern
            holidays = re.findall(r'[^,]+ \([^)]+\)', holiday_text)
            
            for holiday in holidays:
                output_lines.extend(parse_holiday_entry(holiday.strip()))
        
        # Write output with explicit UTF-8 encoding
        with open(output_file, 'wb') as file:
            for line in output_lines:
                file.write(line.encode('utf-8') + '\n')
                
        print("Successfully processed the CSV file!")
        
    except Exception as e:
        print("Error processing file:", str(e))

def generate_date_range(start_date, end_date):
    """Generate all dates between start_date and end_date (inclusive)."""
    print(start_date)
    start = datetime.strptime(start_date, "%d/%m/%Y")
    end = datetime.strptime(end_date, "%d/%m/%Y")
    current = start
    while current <= end:
        yield current.strftime("%d/%m/%Y")
        current += timedelta(days=1)

def get_day_of_week(date_str):
    """Returns the day of the week for a given date in DD/MM/YYYY format."""
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    return date_obj.strftime("%A")

def process_calendar(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'a') as outfile:
        reader = csv.DictReader(infile)
        events_by_date = OrderedDict()  # OrderedDict to preserve input order

        for row in reader:
            #print(row)
            #from_date = row.get('From Date', '').strip()
            #to_date = row.get('To Date', '').strip()
            #event = row.get('Event', '').strip()

            from_date = row['From Date']
            to_date = row['To Date']
            event = row['Event']
            
            # If it's a date range (From Date != To Date)
            if from_date != to_date:
                for date in generate_date_range(from_date, to_date):
                    print(date)
                    day = get_day_of_week(date)  # Get day for each date
                    if date not in events_by_date:
                        events_by_date[date] = {'day': day, 'events': [], 'no_class': False}
                    events_by_date[date]['events'].append(event)
                    if "no class" in event.lower():
                        events_by_date[date]['no_class'] = True
            else:
                # Handle single-date events
                day = get_day_of_week(from_date)
                if from_date not in events_by_date:
                    events_by_date[from_date] = {'day': day, 'events': [], 'no_class': False}
                events_by_date[from_date]['events'].append(event)
                if "no class" in event.lower():
                    events_by_date[from_date]['no_class'] = True

        # Write to the output file in the same order as the input
        for date, data in events_by_date.items():
            # Add "No Class Day" to the note if applicable
            note = data['day'] + " + No Class Day" if data['no_class'] else data['day']
            # Join all events for the status
            status = " , ".join(data['events'])
            outfile.write("{} : Note : {}\n".format(date, note))
            outfile.write("{} : Status : {}\n".format(date, status))

def sort_final_output(file_path):
    """
    Reads the final output file, sorts its lines by the date at the beginning of each line,
    and overwrites the file with the sorted content.
    """
    try:
        # Read all lines from the file
        with open(file_path, 'rb') as f:
            lines = f.readlines()

        entries = []
        date_pattern = re.compile(r'^(\d{2}/\d{2}/\d{2,4})')
        for line in lines:
            line = line.strip()
            m = date_pattern.match(line)
            if m:
                date_str = m.group(1)
                try:
                    # Try parsing as dd/mm/yy; if that fails, try dd/mm/YYYY
                    if len(date_str) == 8:
                        dt = datetime.strptime(date_str, "%d/%m/%y")
                    else:
                        dt = datetime.strptime(date_str, "%d/%m/%Y")
                except Exception as e:
                    dt = datetime.max  # fallback in case of parsing error
            else:
                dt = datetime.max
            entries.append((dt, line))

        # Sort the entries by the datetime object
        entries.sort(key=lambda x: x[0])

        # Write the sorted lines back to the file
        with open(file_path, 'wb') as f:
            for dt, line in entries:
                f.write(line + "\n")
        print("Final output sorted and written to", file_path)
    except Exception as e:
        print("Error sorting final output:", str(e))

def main():
    input_file3 = 'Teaching_and_Academic_Activities.csv'
    input_file2 = 'Administrative_Activities.csv'
    input_file1 = 'calender.csv'  # Replace with the actual calendar file name
    output_file = 'outputdc.txt'
    
    # Process the CSV files (timetable adjustments and calendar events)
    process_csv(input_file1, output_file)
    process_calendar(input_file2, output_file)
    process_calendar(input_file3, output_file)
    
    # Now sort the final output file by date
    sort_final_output(output_file)

if __name__ == "__main__":
    main()