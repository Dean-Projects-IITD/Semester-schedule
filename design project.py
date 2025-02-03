import csv
from collections import OrderedDict
from datetime import datetime, timedelta

# Input and output file paths
input_file = 'input.csv'  # Replace with the actual input file name
output_file = 'output.txt'

def generate_date_range(start_date, end_date):
    """Generate all dates between start_date and end_date (inclusive)."""
    start = datetime.strptime(start_date, "%d/%m/%Y")
    end = datetime.strptime(end_date, "%d/%m/%Y")
    current = start
    while current <= end:
        yield current.strftime("%d/%m/%Y")
        current += timedelta(days=1)

def process_calendar(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        reader = csv.DictReader(infile)
        events_by_date = OrderedDict()  # OrderedDict to preserve input order

        for row in reader:
            from_date = row['From Date']
            to_date = row['To Date']
            day = row['Day']
            event = row['Event']
            
            # If it's a date range (From Date != To Date)
            if from_date != to_date:
                for date in generate_date_range(from_date, to_date):
                    if date not in events_by_date:
                        events_by_date[date] = {'day': day, 'events': [], 'no_class': False}
                    events_by_date[date]['events'].append(event)
                    if "no class" in event.lower():
                        events_by_date[date]['no_class'] = True
            else:
                # Handle single-date events
                if from_date not in events_by_date:
                    events_by_date[from_date] = {'day': day, 'events': [], 'no_class': False}
                events_by_date[from_date]['events'].append(event)
                if "no class" in event.lower():
                    events_by_date[from_date]['no_class'] = True

        # Write to the output file in the same order as the input
        for date, data in events_by_date.items():
            # Add "No Class Day" to the note if applicable
            note = data['day'] + "+ No Class Day" if data['no_class'] else data['day']
            # Join all events for the status
            status = " , ".join(data['events'])
            outfile.write("{} : Note : {}\n".format(date, note))
            outfile.write("{} : Status : {}\n".format(date, status))

# Call the function
process_calendar(input_file, output_file)
print("Output written to", output_file)
