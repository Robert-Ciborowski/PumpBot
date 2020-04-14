"""
Downloads nasdaqlisted.txt from the official NASDAQ ftp server.
"""

#!/usr/bin/python3

import ftplib
import os

with ftplib.FTP('ftp.nasdaqtrader.com') as ftp:
    file_orig = '/SymbolDirectory/nasdaqlisted.txt'
    file_copy = 'nasdaqlisted.txt'

    try:
        ftp.login()

        with open(file_copy, 'wb') as fp:

            res = ftp.retrbinary('RETR ' + file_orig, fp.write)

            # If the download fails, remove the file!
            if not res.startswith('226 Transfer complete'):
                print('Download failed')

                if os.path.isfile(file_copy):
                    os.remove(file_copy)

    except ftplib.all_errors as e:
        print('FTP error:', e)

        if os.path.isfile(file_copy):
            os.remove(file_copy)