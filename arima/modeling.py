from arima import para_est_skl as pes
import numpy as np
# from ARIMA import detect_op as ado
# import copy


def difference_cal(li, d):
    n = len(li)
    if d >= n:
        return False
    if d == 0:
        return li

    i = 1
    arr = []
    while i < n:
        arr.append(li[i] - li[i - 1])
        i += 1
    return difference_cal(arr, d - 1)


def diff_cal_l(li, d, la):
    """差分运算

    :param li: 待差分的列表
    :param d: 差分次数
    :param la: 每次差分前的列表的最后一项组成的列表，依次是第一次差分的最后项，第二次差分的项······
    """
    n = len(li)
    if d >= n:
        return False
    if d == 0:
        return li, la

    la.append(li[-1])

    i = 1
    arr = []
    while i < n:
        arr.append(li[i] - li[i - 1])
        i += 1
    return diff_cal_l(arr, d - 1, la)


def turn_to_np_float_64(li, d):
    """让列表中每个元素变为float64的"""
    np_f64 = []
    if d == 1:
        for i in li:
            np_f64.append(np.float64(i))
        return np_f64
    if d == 2:
        for i in li:
            tmp = []
            for j in i:
                tmp.append(np.float64(j))
            np_f64.append(tmp)
        return np_f64


def ar(q, li):
    """得到q阶AR模型的参数"""
    if q == 0:
        return 0
    i = q
    n = len(li)
    li_x = []
    li_y = []
    while i >= 0:  # 将Y(t-q)先放入li_x,再依次放入Y(t-q+1)······Y(t)
        tmp_arr = li[q - i:n - i]
        # print(tmp_arr)
        if i != 0:
            tmp_x = []
            for j in tmp_arr:
                tmp_x.append(j)
            li_x.append(tmp_x)
        else:
            for j in tmp_arr:
                li_y.append(j)
        i -= 1  # 此while循环一共执行q+1次
    # print('lx = ',li_x,'ly = ',li_y)
    para = pes.get_para_least_sq(li_x, li_y)  # 第一项是Y(t-q)前面的参数，最后一项是Y(t-1)的参数
    return para


def ma():
    pass


def predict_ar(para, li, res=1):
    """预测X(t+1)的值"""
    if res == 1:
        epsilon = para[-1]
    else:
        epsilon = 0
    x_t = 0
    for i, j in enumerate(para[:-1]):
        x_t += j * li[-1 - i]
    return x_t + epsilon


def get_stationary_time_series():
    pass


if __name__ == '__main__':
    # generate_code()
    li2 = []
    li1 = [6, 1, 2, 7, 4, 5]
    # print(diff_cal_l(li1, 2, li2))
    # print(li1[:3], li1[3:])

    li3 = [1, 5, 13, 29, 61, 125]
    print(ar(1, li3), ar(1, li3)[:-1])
