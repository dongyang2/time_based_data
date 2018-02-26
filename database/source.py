# handle the data format
class Source(object):
    json_body1 = [      # 'list' type
        {
            "measurement": "students",
            # "hostname": "server0",
            "tags": {
                "a1": "s123",
            },
            "fields": {
                "time_stamp": 0
            }
        }
    ]

    json_body2 = [
        {
            "measurement": "students",
            # "hostname": "server0",
            "tags": {
                "a1": "s120",

            },
            "fields": {
                "time_stamp": 1
            }
        }
    ]

    def __init__(self):
        self.__name = ''

    @staticmethod
    def turn_col_to_list(arr1, name):     # 注意，write_points不是需要JSON类型的数据，而是用JSON格式写出来的list类型
        len_row = len(arr1[0])
        arr2 = []
        i = 0
        # print(len_row)
        count = 0
        while i < len_row:
            temp = {}
            k = 1
            for j in arr1:
                # print(' i = ', i, ' k = ', k)
                tmp_str = 'sample' + str(k)
                if i < len(j):
                    temp[tmp_str] = j[i]
                else:
                    count += 1
                    temp[tmp_str] = 'null'
                k += 1
            str_dic = {'measurement': name, 'tags': temp, "fields": {"time_stamp": i}}
            arr2.append([str_dic])
            del temp
            del str_dic
            i += 1
        if count != 0:
            print('the number of null ', count)
        return arr2

    @staticmethod
    def turn_set_to_row(st):
        """Turn a query output to a 2-dimensional list

        :param st: a output of query
        :type st::class:'influxdb.resultset.ResultSet'

        :return: a 2-dimensional list
        :rtype: list
        """
        arr2 = []
        for i in st:
            for j in i:
                k = 0
                arr1 = []
                while k < len(j)-2:
                    str_key = 'sample'+str(k+1)
                    # arr1.append(float(j[str_key]))
                    if isinstance(j[str_key], str) and j[str_key] != 'null':
                        arr1.append(float(j[str_key]))
                    else:
                        print('An abnormal number. Type ', type(j[str_key]), ' sample ', k+1)
                        arr1.append(float('inf'))
                    k += 1
                arr2.append(arr1)
        arr2 = Source.list_transpose(arr2)
        # print(arr2)
        return arr2

    @staticmethod
    def list_transpose(arr1):
        """
        矩阵的转置
        :param arr1: 待转置的二维矩阵
        :type arr1: list
        :return: 转置好的矩阵
        """
        k1 = len(arr1)      # arr1的行数
        k2 = len(arr1[0])  # arr1的列数
        arr2 = []
        i = 0
        while i < k2:
            j = 0
            arr3 = []
            while j < k1:
                arr3.append(arr1[j][i])
                j += 1
            arr2.append(arr3)
            i += 1
        return arr2

    @staticmethod
    def str_match(str1, str2):
        """查看str2是不是在str1里，对于查找来说就是str2是否在此数据库中有对应的TEST和TRAIN表

            :param str1: the real table name
            :type str1: str

            :param str2: the input name
            :type str2: str
        """
        str3 = str2 + '_'
        ind = str1.find(str3)
        # print(ind)
        if ind == 0:
            return True
        else:
            return False


if __name__ == '__main__':
    src = Source
    # Source.is_rectangle('../resource/UCR_TS_Archive_2015/StarLightCurves_change/StarLightCurves_TEST8')
    print(src.str_match('50words_TEST', '50words'))


