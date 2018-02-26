from influxdb import InfluxDBClient
from database import source
import random
import numpy


def show_names(c):     # show all the name of tables in database c
    result = c.query('show measurements;')  # 显示数据库中的表
    for i in result:
        print(i[0]['name'])
    # print(result)


def query_simple(db, s):
    output = db.query(s)
    # print(output)
    # print(type(output))
    return output


def create_input_arr():
    arr1 = []
    for i in range(4):
        r0 = []
        j = -1
        while j < 4:
            # r0.append(random.random())
            r0.append(random.randint(1,9))
            j += 1
        arr1.append(r0)
    return arr1


if __name__ == '__main__':
    # dic = [{'measurement': 'students', 'tags': {'a1': 's135'}, 'fields': {"time_stamp": 2}}]
    # print(type(dic))
    # dic2 = dict()
    # dic2['a'] = 3
    # print(type(dic[0]))
    # import json
    # needed_json = json.dumps(dic)
    # needed_json = [{format(dic)}]
    # print(needed_json)

    li = create_input_arr()
    print(li)
    arr = source.Source().turn_col_to_list(li, 'Plane_TEST')

    client = InfluxDBClient('localhost', 8086, '', '')  # 初始化

    # print(client.get_list_database())
    client.create_database('test')
    # print(client.get_list_database())
    # client.drop_database('test')
    # print(client.get_list_database())

    test_db = InfluxDBClient('localhost', 8086, '', '', 'test')     # get a database that named 'test'

    # src = source.Source()
    # test_db.write_points(src.json_body1)   # InfluxDB中没有显式建表的语句，只能通过insert数据的方式来建立新表
    # test_db.write_points(src.json_body2)
    # test_db.write_points(dic)
    # query_output = test_db.query('show measurements;')       # SQL
    # print(format(query_output))

    for l in arr:
        test_db.write_points(l)
        # break

    # show_names(test_db)
    result1 = test_db.query('select * from Plane_TEST')
    # print(type(result1))
    print(numpy.array(source.Source.turn_set_to_row(result1)))
    # for l in result1:       # 这里说明查询整个表输出的类型是set，并且只有一个元素
    #     # print(type(l))       # 唯一的那个元素是list类型，就和我插入时一样，形如Source.json_body1
    #     for m in l:
    #         # print(type(m))      # 这里的类型就是dict了
    #         # print(len(m))
    #         print(m)
    test_db.query("drop measurement Plane_TEST")      # 删除表
