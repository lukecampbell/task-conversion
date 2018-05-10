#!/usr/bin/env python

__version__ = '0.0.1'

from argparse import ArgumentParser
import csv
import arrow
import re
import uuid
import json


ISO_DATE_FORMAT = 'YYYYMMDDTHHmmss'


def main():
    '''
    Converts a CSV of tasks into the task warrior JSON format
    '''
    parser = ArgumentParser(description=main.__doc__)
    parser.add_argument('-o', '--output', default='stdout', help='Output JSON file')
    parser.add_argument('input', help='csv file')
    args = parser.parse_args()

    tasks = [mapper(row) for row in parse_csv(args.input)]
    if args.output == 'stdout':
        print(json.dumps(tasks, sort_keys=True, indent=4))
    else:
        with open(args.output, 'w') as f:
            f.write(json.dumps(tasks))

    return 0


def mapper(row):
    '''
    Returns a dictionary in the taskwarrior format mapped from a row from
    the CSV file

    :param dict row: A row from the CSV file
    :rtype: dict
    '''
    entered_date = arrow.utcnow().format(ISO_DATE_FORMAT) + 'Z'
    if row['Date']:
        entered_date = convert_date(row['Date'])
    retval = {
        'id': row['id'],
        'uuid': str(uuid.uuid4()),
        'description': row['Name'],
        'annotations': [
            {
                'entry': entered_date,
                'description': row['Description'],
            }
        ],
        'status': 'pending',
        'modified': entered_date,
        'entry': entered_date,
        'urgency': 0,
    }
    if row['Status'] in ('Done', 'OBE'):
        retval['status'] = 'complete'
        completed_date = entered_date

        # Set the completed date if it was entered into the row
        if re.match(r'\d+/\d+/\d+', row['Completed Date']):
            completed_date = convert_date(row['Completed Date'])

        retval['end'] = completed_date
        retval['modified'] = completed_date

        if row['Status'] == 'OBE':
            retval['annotations'].append({
                'entry': completed_date,
                'description': 'OBE'
            })

    return retval


def parse_csv(csvfile):
    '''
    Parses a CSV file and returns a row of dictionaries for each corresponding
    row in the CSV file

    :param str csvfile: Path of the CSV file
    :rtype: list
    '''
    with open(csvfile, 'r') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    i = 0
    for row in rows:
        row['id'] = i
        i += 1
    return rows


def convert_date(datestr):
    '''
    Converts the US format for date into an ISO-8601 like string

    :param str datestr: The US formatted date string
    :rtype: str
    '''
    iso_str = arrow.get(datestr, 'M/D/YYYY').format(ISO_DATE_FORMAT) + 'Z'
    return iso_str


if __name__ == '__main__':
    import sys
    sys.exit(main())
