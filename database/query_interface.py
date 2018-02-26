from database import db_op
import datetime


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    do = db_op
    db1 = do.initialize('ucr_2015')
    str0 = 'ElectricDevices'
    str9 = 'Adiac'
    arr = do.query_by_name(db1, str0)
    for l in arr:
        print(l)
    end_time = datetime.datetime.now()
    print(end_time-start_time)
