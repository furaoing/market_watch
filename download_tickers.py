import ftplib
import os
from config import IBConfig


def download_ftp_files(dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    # Connect to ftp.nasdaqtrader.com
    ftp = ftplib.FTP('ftp.nasdaqtrader.com', 'anonymous', 'anonymous@debian.org')
    # Download files nasdaqlisted.txt and otherlisted.txt from ftp.nasdaqtrader.com
    for ficheiro in ["nasdaqlisted.txt", "otherlisted.txt"]:
            ftp.cwd("/SymbolDirectory")
            dest_path = os.path.join(dest_dir, ficheiro)
            localfile = open(dest_path, 'wb')
            ftp.retrbinary('RETR ' + ficheiro, localfile.write)
            localfile.close()
    ftp.quit()


def download_IB_files(dest_dir, short_file_names):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    # Connect to ftp.nasdaqtrader.com
    ftp = ftplib.FTP('ftp3.interactivebrokers.com', 'shortstock', '')
    for ficheiro in short_file_names:
            ftp.cwd("/")
            dest_file_name = ficheiro
            dest_path = os.path.join(dest_dir, dest_file_name)
            localfile = open(dest_path, 'wb')
            ftp.retrbinary('RETR ' + ficheiro, localfile.write)
            localfile.close()
    ftp.quit()


if __name__ == "__main__":
    dest_dir = "data"
    download_IB_files(dest_dir, IBConfig.short_data_file_names)
