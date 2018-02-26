# database operations
from influxdb import InfluxDBClient
from database import source
import numpy


def show_names(c):     # show all the name of tables in database c
    arr1 = []
    result = c.query('show measurements;')  # 显示数据库中的表
    for i in result:
        # print(i[0]['name'])
        for j in i:
            arr1.append(j['name'])
    return arr1


def query_by_name(db, file_name):
    """获得对db数据库的一个叫file_name表查询的最后结果

    :param db: database
    :param file_name: table name
    :type file_name: str
    :return: a 3-dimensional list or False
    """
    arr1 = show_names(db)
    arr2 = []
    bool_file_name = 0
    src = source.Source()
    for i in arr1:
        if src.str_match(i, file_name):
            arr2.append(i)
            bool_file_name = 1
    if bool_file_name == 1:
        arr3 = []
        for i in arr2:
            output = db.query('select * from ' + i)
            matrix = src.turn_set_to_row(output)
            arr3.append(numpy.array(matrix))
        return arr3
    else:
        print('No such file name')
        return False


def initialize(db_name):
    """Get a database named db_name, if it not exist, create one.
        :type db_name: str
    """
    client = InfluxDBClient('localhost', 8086, '', '')
    client.create_database('ucr_2015')
    db = InfluxDBClient('localhost', 8086, '', '', db_name)
    return db


def get_all_data_set_name(db):
    output = show_names(db)
    ca = ''
    arr1 = []
    for i in output:
        li_name = i.split('_')[:-1]
        set_name = li_name[0]
        j = 1
        while j < len(li_name):
            set_name = set_name + '_' + li_name[j]
            j += 1
        if set_name != ca:
            arr1.append(set_name)
            ca = set_name
    return arr1


if __name__ == '__main__':
    test_db = initialize('ucr_2015')
    # print(show_names(test_db))
    print(get_all_data_set_name(test_db))
