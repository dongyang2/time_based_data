# 遍历一个目录下所有数据文件，将其数据导入InfluxDB
from database import file_op
from influxdb import InfluxDBClient
from database import source


# def turn_file_to_arr(path):
#     arr1 = []
#     arr2 = []
#     each_name = file_operate.each_file_or_dir_name(path)
#     for i in each_name:
#         each_file = file_operate.each_file_or_dir_name(i)
#         for j in each_file:     # 进入最后一层文件夹，里面只有文件
#             # print(j.split('/')[-1])
#             arr1.append(j.split('/')[-1])       # arr1存文件名，一维数组
#             arr2.append(file_operate.read_file(j))      # arr2存文件的内容，三维数组
#         # break
#     return arr1, arr2


def write_file_to_db(path, db_name):
    each_name = file_op.each_file_or_dir_name(path)
    for i in each_name:
        each_file = file_op.each_file_or_dir_name(i)
        for j in each_file:
            arr3 = source.Source.turn_col_to_list(file_op.read_file(j), j.split('/')[-1])
            print('Now write ' + j.split('/')[-1] + ' .')
            # k = 0
            for i2 in arr3:
                # if k % 50 == 0:
                #     print('k = ', k)
                db_name.write_points(i2)
                # k += 1
            print('Done.')
            del arr3
    return


if __name__ == '__main__':
    path1 = '../resource/UCR_TS_Archive_2015'
    path2 = '../resource/2'
    # name, content = turn_file_to_arr(path1)
    # for l in c:
    #     print(l)
    client = InfluxDBClient('localhost', 8086, '', '')
    client.create_database('ucr_2015')
    test_db = InfluxDBClient('localhost', 8086, '', '', 'ucr_2015')

    # 这里写入就有文章啦，一般碰到200行，100行，400行的时候就会报200的错误，超过3000行就会报400的错误，所以其实可以对于文件预处理，再写入
    write_file_to_db(path2, test_db)
    # k = 0
    # for l in name:
    #     arr = source.Source.turn_col_to_list(content[k], l)
    #     for m in arr:
    #         print(m)
    #         test_db.write_points(m)
    #     k += 1
