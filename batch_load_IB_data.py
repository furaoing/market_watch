import traceback
from database import MySQLUpdater
from common import generate_content_hash, get_formated_time
from read_IB_data import read_IB_data
from sqlalchemy import desc
from market_watch_logger import root_logger


def get_time_integer(datetime):
    def zero_padding(one_int):
        if one_int < 10:
            one_str = "0" + str(one_int)
        else:
            one_str = str(one_int)
        return one_str

    year = datetime.year
    month = datetime.month
    day = datetime.day
    hour = datetime.hour
    minute = datetime.minute
    second = datetime.second

    datetime_str = str(year) + zero_padding(month) + zero_padding(day) + zero_padding(hour) + zero_padding(minute) + zero_padding(second)
    return int(datetime_str)


def load_helper(mysql_updater, file_path, IBShortDataTable):
    try:
        IB_data_path = file_path
        IB_data = read_IB_data(IB_data_path)

        record_datetime = IB_data.get("file_record_datetime")
        records = IB_data.get("records")
        for x in records:
            SYM = x[0]
            CUR = x[1]
            NAME = x[2]
            CON = x[3]
            ISIN = x[4]
            REBATERATE = x[5] if x[5] != "NA" else "0"
            FEERATE = x[6] if x[6] != "NA" else "0"
            AVAILABLE = x[7]
            datetime_formated = str(record_datetime)
            datetime_integer = int(record_datetime.strftime("%Y%m%d%H%M%S"))
            hash_item_list = [CON, CUR, datetime_integer]
            hash_str = generate_content_hash(hash_item_list)
            IB_data_record = IBShortDataTable(Id=hash_str,
                                            SYM=SYM,
                                            CUR=CUR,
                                            NAME=NAME,
                                            CON=CON,
                                            ISIN=ISIN,
                                            REBATERATE=REBATERATE,
                                            FEERATE=FEERATE,
                                            AVAILABLE=AVAILABLE,
                                            DateTimeFormated=datetime_formated,
                                            DateTimeInteger=datetime_integer)
            # if use db service side handling code: .order_by(desc(IBShortDataTable.DateTimeInteger)).first()
            records = mysql_updater.session.query(IBShortDataTable).filter_by(CON=CON)
            records_list = []
            for record in records:
                records_list.append(record)
            if len(records_list) > 0:
                records_list.sort(key=lambda x: x.DateTimeInteger)
                recent_record = records_list[-1]
                recent_record_available = recent_record.AVAILABLE
                recent_record_hash = recent_record.Id
                if hash_str != recent_record_hash:
                    # same record for the same asset not exist in DB
                    if AVAILABLE != recent_record_available:
                        # new orders found, insert into db
                        mysql_updater.session.add(IB_data_record)
                        mysql_updater.session.commit()
            else:
                # no previous records for this con exist
                mysql_updater.session.add(IB_data_record)
                mysql_updater.session.commit()

    except Exception:
        msg = "IB Record DB (%s) Insert Exception, Time (Beijing Time) is: %s" % (IBShortDataTable.__tablename__, get_formated_time())
        root_logger.error(msg)
        raise Exception(msg)


def load_batch_records(file_path, IBShortDataTable):
    mysql_updater = MySQLUpdater()
    load_helper(mysql_updater, file_path, IBShortDataTable)
    mysql_updater.clean_up()


def batch_load(file_path, IBShortDataTable):
    try:
        load_batch_records(file_path, IBShortDataTable)
    except Exception:
        root_logger.error(traceback.format_exc())


if __name__ == "__main__":
    f_path = "data/usa.txt"
    from data_model import IBShortDataUS
    batch_load(f_path, IBShortDataUS)
