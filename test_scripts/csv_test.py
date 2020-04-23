"""
Shows how to read the nasdaqlisted txt as a csv (even though its seperated
by pipes, not commas)
"""

import csv

data = [[], []]

with open('nasdaqlisted.txt', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter='|')
    line_count = 0

    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1

        data[0].append(row["Symbol"])
        data[1].append(row["Security Name"])

        # Note: we could add more data from nasdaqlisted.txt if we wanted to.
        # (since there are more coloumns)

        line_count += 1

        # There a lot of data in nasdaqlisted, so let's only take the first 20.
        if line_count > 20:
            break

    print(f'Processed {line_count} lines with csv reader.')

print(data)