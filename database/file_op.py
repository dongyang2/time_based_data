# operations about file
# -*- coding: UTF-8 -*-

import os


# 遍历指定目录，显示目录下的所有文件或目录名
def each_file_or_dir_name(path):
    path_dir = os.listdir(path)
    di_fi = []
    for di_or_fi in path_dir:
        each_path = os.path.join('%s/%s' % (path, di_or_fi))
        # print(child.decode('gbk'))  # .decode('gbk')是解决中文显示乱码问题
        # print(di_or_fi)
        di_fi.append(each_path)
    return di_fi


# 读取文件内容
def read_file(filename):
    f_open = open(filename, 'r')
    file_content = []
    for eachLine in f_open:
        # print("读取到得内容如下：",eachLine)
        row1 = eachLine.split(',')      # 用逗号分割
        # print(row1[-1][:-2])
        row1[-1] = row1[-1][:-1]        # 把回车符去掉，不然写不进数据库
        # print(len(row1))
        file_content.append(row1)
    f_open.close()
    return file_content


def is_rectangle(file_path):        # 判断一个文件内容每一行长度是不是一样
    with open(file_path, 'r') as f_c:
        file_content = []
        for each_line in f_c:
            row1 = each_line.split(',')
            row1[-1] = row1[-1][:-1]
            file_content.append(len(row1))
        j = 1
        bool_rectangle = 0
        # print(len(file_content))
        while j < len(file_content):
            if file_content[j] != file_content[j-1]:
                bool_rectangle = 1
                print('The line ', str(j), '(', str(file_content[j]),
                      ') is not equal to the above(', str(file_content[j-1]),  ').')
            j += 1
        if bool_rectangle == 0:
            print('Is rectangle.')


# 输入多行文字，写入指定文件并保存到指定文件夹
# def writeFile(filename):
#     f_open = open(filename, 'w')
#     print("\r请任意输入多行文字"," ( 输入 .号回车保存)")
#     while True:
#         aLine = raw_input()
#         if aLine != ".":
#             f_open.write('%s%s' % (aLine, os.linesep))
#         else:
#             print("文件已保存!")
#             break
#     f_open.close()


if __name__ == '__main__':
    path1 = "../resource/UCR_TS_Archive_2015"
    each_name = each_file_or_dir_name(path1)
    for i in each_name:
        each_file = each_file_or_dir_name(i)
        for j in each_file:
            c = read_file(j)
        break
    for l in c:
        print(l)

