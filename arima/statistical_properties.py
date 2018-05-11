# 包含了求均值，方差，自协方差和自相关系数的函数。
import math
import numpy
import copy


def mean(li):
    """平均值"""
    s = 0
    for i in li:
        s += i
    return s / len(li) * 1.0  # 返回结果保留小数点后15位


def variance(li, bias=0):
    """
    方差
    :param li:数列
    :param bias: 有偏或无偏。=1有偏，分母为n，=0无偏，分母为n-1
    """
    li_mean = mean(li)
    s = 0
    for i in li:
        s += (i - li_mean) * (i - li_mean)
    return s / (len(li) - 1 + bias) * 1.0


def auto_cov(li, k, bias=0):
    """
    自协方差函数
    :param li:数列
    :param k:滞后系数,k = 0 时就是和方差结果一样
    :param bias:有偏或无偏。=1有偏，分母为n，=0无偏，分母为n-1
    """
    n = len(li)
    mean1 = mean(li[:n - k])
    mean2 = mean(li[k:])
    s = 0
    i = 0
    while i < n - k:
        s += (li[i] - mean1) * (li[i + k] - mean2)
        i += 1
    return s / (n - 1 + bias) * 1.0


def acf(li, k):
    """
    自相关系数（自相关函数）
    Autocorrelation Function
    """
    if k == 0:
        return 1.0
    ac = auto_cov(li, k)
    n = len(li)
    dt = variance(li[:n - k])
    ds = variance(li[k:])
    return ac / math.sqrt(dt * ds) * 1.0


def p_acf(li, kk):
    """偏自相关系数"""
    k = 0
    rou = []
    while k <= kk:
        rou.append(acf(li, k))
        # rou.append('p' + str(k))
        k += 1
    i = 0
    d = []
    while i < kk:
        j = 1
        row = []
        k = i
        while k >= 0:
            row.append(rou[k])
            k -= 1
        while j < kk - i:
            row.append(rou[j])
            j += 1
        d.append(row)
        i += 1
    # print(d)
    # dk = d
    dk = copy.deepcopy(d)  # 深复制，不然会让d跟着dk一起变
    i = 0
    while i < kk:
        dk[i][kk - 1] = rou[i + 1]
        i += 1
    # print(d, det(d))
    # print(dk, det(dk))
    # return det(dk)/det(d)
    try:
        return det(dk) / det(d)
    except ZeroDivisionError:
        print(d)


def det(m):
    """
    求行列式的值
    :param m: 行列式， 二维数列
    :return: 行列式的值
    """
    length = len(m)
    if length == 1:
        return m[0][0]
    else:
        s = 0
        i = 0
        while i < length:
            n = [[row[a] for a in range(length) if a != i] for row in m[1:]]
            s += m[0][i] * det(n) * (-1) ** (i % 2)
            i += 1
        return s


def acf_list(li, lag=-1):
    if lag == -1 or lag > len(li):
        n = len(li)
    else:
        n = lag
    arr_acf = []
    for i in range(n):
        arr_acf.append(acf(li, i))
    return arr_acf


def test_find_triangle():
    li4 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
           [1, 1, 1, 0, 0, 0, 0, 0, 0, 0]]
    subscript = [len(li4), len(li4[0])]
    for j, i in enumerate(li4):
        standard = 0.5
        k = len(i) - 1
        tmp_ss = [j, k]
        while k >= 0:
            if abs(i[k]) > standard:
                tmp_ss[1] = k + 1
                print(tmp_ss, 'oh!')
                break
            k -= 1
        if tmp_ss[1] < subscript[1]:
            subscript = tmp_ss
    print(subscript)


if __name__ == '__main__':
    li1 = [1, 4, 9]
    li2 = [2, 3, 4, 3, 7]
    li3 = [0, 1, 2, 3, 4]

    cov1 = numpy.cov([li2[:4], li2[1:]])
    # print(cov1)
    # print(variance(li2[:4]), acf(li2, 1))
    # print(acf(li2, 0), acf(li2, 2), acf(li2, 3))
    # print(-18/185*1.0, 23/370*1.0, -14/185*1.0)

    # print(mean(li1))
    # print(li3[1:5])
    # arr = [[1]]
    # print(det(arr))
    # pf1 = p_acf(li2, 3)
    # print(pf1)
