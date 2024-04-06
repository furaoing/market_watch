from batch_load_IB_data import batch_load
import time
from data_model import IBShortDataUS, IBShortDataHK
from download_tickers import download_IB_files
import os
from market_watch_logger import root_logger
import traceback


if __name__ == "__main__":
    dest_dir_path = "data"
    short_data = [
        {"file_name": "usa.txt",
         "db": IBShortDataUS},
        {"file_name": "hongkong.txt",
         "db": IBShortDataHK}
    ]
    file_names = [x.get("file_name") for x in short_data]

    while True:
        try:
            download_IB_files(dest_dir_path, file_names)
        except TimeoutError:
            root_logger.error("IB Ftp Connection Timeout")
            root_logger.error(traceback.format_exc())
            time.sleep(1*60)
            continue
        except ConnectionError:
            root_logger.error("IB Ftp Connection Error")
            root_logger.error(traceback.format_exc())
            time.sleep(1*60)
        except:
            root_logger.error(traceback.format_exc())
            time.sleep(1*60)
            continue
        root_logger.info("Downloading IB Files")
        for short in short_data:
            file_name = short.get("file_name")
            db = short.get("db")
            file_path = os.path.join(dest_dir_path, file_name)
            root_logger.info("Data Load Begins")
            batch_load(file_path, db)
            root_logger.info("Data Load Completed")
        # Run every 15 mins
        root_logger.info("Sleep ...")
        time.sleep(15*60)
