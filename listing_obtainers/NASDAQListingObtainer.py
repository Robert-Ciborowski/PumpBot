# Name: NASDAQListingObtainer
# Author: Robert Ciborowski
# Date: 12/04/2020
# Description: Obtains all listings from the NASDAQ.

# from __future__ import annotations

import pandas as pd
import ftplib
import os
import csv

from listing_obtainers.ListingObtainer import ListingObtainer


class NASDAQListingObtainer(ListingObtainer):
    amount_to_obtain: int

    """
    If amount_to_obtain is negative, then all listings will be obtained.
    You can just not pass it in since it's optional.
    """
    def __init__(self, amount_to_obtain=-1):
        super().__init__()
        self.amount_to_obtain = amount_to_obtain

    def obtain(self) -> pd.DataFrame:
        self._write_listings_to_file()
        self._get_listings_from_file()
        return pd.DataFrame(self.template)

    def _write_listings_to_file(self):
        with ftplib.FTP('ftp.nasdaqtrader.com') as ftp:
            file_orig = '/SymbolDirectory/nasdaqlisted.txt'
            file_copy = 'nasdaqlisted.txt'

            try:
                ftp.login()

                with open(file_copy, 'wb') as fp:

                    res = ftp.retrbinary('RETR ' + file_orig, fp.write)

                    # If the download fails, remove the file!
                    if not res.startswith('226 Transfer complete'):
                        print('NASDAQ listings download failed!!!')

                        if os.path.isfile(file_copy):
                            os.remove(file_copy)

            except ftplib.all_errors as e:
                print('NASDAQ Listings FTP error:', e)

                if os.path.isfile(file_copy):
                    os.remove(file_copy)

    def _get_listings_from_file(self):
        with open('nasdaqlisted.txt', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter='|')
            line_count = 0

            for row in csv_reader:
                if line_count == 0:
                    # print(f'Column names are {", ".join(row)}')
                    line_count += 1

                self.template["Ticker"].append(row["Symbol"])

                # Note: we could add more data from nasdaqlisted.txt if we wanted to.
                # (since there are more coloumns)

                line_count += 1

                # There a lot of data in nasdaqlisted, so let's only take the first 20.
                if 0 < self.amount_to_obtain < line_count:
                    break

            # print(f'Processed {line_count} lines with csv reader.')
